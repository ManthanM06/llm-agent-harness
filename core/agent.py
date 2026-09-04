# core/agent.py
import ollama
import json 
import re   
from typing import Generator, Optional, Callable, Dict, Any
from core.config import config
from core.memory import ChatMemory
from tools.registry import registry
from skills.registry import skill_registry

class AgentEngine:
    def __init__(
        self,
        permission_handler: Optional[Callable[[str, Dict[str, Any]], bool]] = None,
        on_skill_activated: Optional[Callable[[Any], None]] = None,
        on_tool_call: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        on_tool_result: Optional[Callable[[str, str], None]] = None,
    ):
        self.memory = ChatMemory()
        self.available_tools = registry.get_all_tools()
        self.on_skill_activated = on_skill_activated
        self.on_tool_call = on_tool_call
        self.on_tool_result = on_tool_result

        if permission_handler is not None:
            registry.set_permission_handler(permission_handler)

    def _extract_manual_json_tools(self, text: str) -> list:
        """
        Fallback parser: Sometimes small models output raw JSON code blocks or tags
        instead of using the API's tool_calls array. This attempts to extract them.
        """
        tools_found = []
        if not text:
            return tools_found

        decoder = json.JSONDecoder()
        pos = 0
        while pos < len(text):
            idx_obj = text.find("{", pos)
            idx_arr = text.find("[", pos)
            
            candidates = [i for i in [idx_obj, idx_arr] if i != -1]
            if not candidates:
                break
            idx = min(candidates)

            try:
                parsed, end_pos = decoder.raw_decode(text[idx:])
                pos = idx + end_pos
                
                items = parsed if isinstance(parsed, list) else [parsed]
                for item in items:
                    if isinstance(item, dict) and "name" in item:
                        args = item.get("arguments", {})
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except Exception:
                                pass
                        tools_found.append({
                            "function": {
                                "name": item["name"],
                                "arguments": args if isinstance(args, dict) else {}
                            }
                        })
            except Exception:
                pos = idx + 1

        return tools_found

    def chat(self, user_prompt: str) -> Generator[str, None, None]:
        skill, content = skill_registry.match_skill(user_prompt)

        if skill:
            if not content:
                # Skill was called with no query, provide helpful usage prompt
                usage_msg = (
                    f"**Skill Activated: {skill.name}** (`{skill.trigger}`)\n\n"
                    f"{skill.description}\n\n"
                    f"**Usage:** `{skill.trigger} <question or problem description>`"
                )
                yield usage_msg
                return

            if self.on_skill_activated:
                self.on_skill_activated(skill)
            else:
                print(f"\n[Agent Engine] 🎯 Skill Activated: {skill.name} ({skill.trigger})")
            self.memory.add_message("system", skill.get_system_instructions())
            self.memory.add_message("user", content)
        else:
            self.memory.add_message("user", user_prompt)

        loop_count = 0          
        max_loops = 5
        last_tool_signature = None

        while True:
            if loop_count >= max_loops:
                final_msg = "\n[System] Agent halted: Exceeded maximum tool execution loops."
                self.memory.add_message("assistant", final_msg)
                yield final_msg
                break

            self.available_tools = registry.get_all_tools()
            response_stream = ollama.chat(
                model=config.MODEL_NAME,
                messages=self.memory.get_messages(),
                tools=self.available_tools,
                options={
                    "num_ctx": config.NUM_CTX,
                    "num_predict": config.NUM_PREDICT,
                    "temperature": config.TEMPERATURE
                },
                stream=True
            )

            content = ""
            api_tool_calls = []
            is_streaming_to_caller = False

            for chunk in response_stream:
                msg = chunk.get("message", {})
                token = msg.get("content", "") or ""
                content += token

                raw_api_calls = msg.get("tool_calls")
                if raw_api_calls:
                    for call in raw_api_calls:
                        if hasattr(call, "function"):
                            name = call.function.name
                            args = call.function.arguments
                            if hasattr(args, "model_dump"):
                                args = args.model_dump()
                            elif isinstance(args, str):
                                try:
                                    args = json.loads(args)
                                except Exception:
                                    pass
                        elif isinstance(call, dict) and "function" in call:
                            name = call["function"]["name"]
                            args = call["function"].get("arguments", {})
                        else:
                            continue
                        api_tool_calls.append({
                            "function": {
                                "name": name,
                                "arguments": args if isinstance(args, dict) else {}
                            }
                        })

                if not is_streaming_to_caller and not api_tool_calls:
                    stripped = content.lstrip()
                    if stripped:
                        # If beginning might be a codeblock, tag, or json, wait for a few chars to inspect
                        if len(stripped) < 7 and (stripped.startswith("`") or stripped.startswith("<") or stripped.startswith("{") or stripped.startswith("[")):
                            pass
                        elif stripped.startswith(("{", "[", "```json", "<tool", "<function")):
                            pass  # Buffer potential manual tool call
                        else:
                            is_streaming_to_caller = True
                            yield content
                elif is_streaming_to_caller:
                    yield token

            manual_tool_calls = self._extract_manual_json_tools(content)
            all_tools_to_run = api_tool_calls if api_tool_calls else manual_tool_calls

            if all_tools_to_run:
                # Cycle detection safeguard
                try:
                    current_sig = [
                        (tc["function"]["name"], json.dumps(tc["function"]["arguments"], sort_keys=True))
                        for tc in all_tools_to_run
                    ]
                except Exception:
                    current_sig = None

                if current_sig is not None and current_sig == last_tool_signature:
                    # Model repeated the exact same tool calls without synthesizing
                    nudge_msg = "You have already executed these tools and received their results. Please synthesize the final answer for the user."
                    self.memory.add_message("user", nudge_msg)
                    loop_count += 1
                    continue

                last_tool_signature = current_sig

                # Store assistant tool invocation in memory
                self.memory.add_message(
                    role="assistant", 
                    content="", 
                    tool_calls=all_tools_to_run
                )

                for tool_call in all_tools_to_run:
                    func_name = tool_call["function"]["name"]
                    arguments = tool_call["function"]["arguments"]
                    
                    if self.on_tool_call:
                        self.on_tool_call(func_name, arguments)
                    else:
                        print(f"\n[Agent Engine] 🛠️  Executing tool: {func_name}({arguments})")
                    
                    tool_result = registry.execute(func_name, arguments)
                    
                    if self.on_tool_result:
                        self.on_tool_result(func_name, str(tool_result))
                    
                    formatted_result = f"Result of {func_name}: {str(tool_result)}"
                    self.memory.add_message("tool", formatted_result, tool_name=func_name)
                
                loop_count += 1  
                continue
                
            else:
                self.memory.add_message("assistant", content)
                if not is_streaming_to_caller:
                    # Flush buffered content if it was not streamed yet
                    yield content
                break
                
    def clear_session(self):
        self.memory.clear()