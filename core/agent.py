# core/agent.py
import ollama
import json 
import re   
from typing import Generator
from core.config import config
from core.memory import ChatMemory
from tools.registry import registry

class AgentEngine:
    def __init__(self):
        self.memory = ChatMemory()
        self.available_tools = registry.get_all_tools()

    def _extract_manual_json_tools(self, text: str) -> list:
        """
        Fallback parser: Sometimes small models output raw JSON code blocks instead
        of using the API's tool_calls array. This attempts to extract them.
        """
        tools_found = []
        # Find everything between ```json and ```
        json_blocks = re.findall(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        for block in json_blocks:
            try:
                data = json.loads(block)
                if "name" in data and "arguments" in data:
                    tools_found.append({
                        "function": {
                            "name": data["name"],
                            "arguments": data["arguments"]
                        }
                    })
            except json.JSONDecodeError:
                continue
        return tools_found

    def chat(self, user_prompt: str) -> Generator[str, None, None]:
        self.memory.add_message("user", user_prompt)

        loop_count = 0          
        max_loops = 5   

        while True:
            if loop_count >= max_loops:
                final_msg = "\n[System] Agent halted: Exceeded maximum tool execution loops."
                self.memory.add_message("assistant", final_msg)
                yield final_msg
                break

            response = ollama.chat(
                model=config.MODEL_NAME,
                messages=self.memory.get_messages(),
                tools=self.available_tools,
                options={
                    "num_ctx": config.NUM_CTX,
                    "temperature": config.TEMPERATURE
                },
                stream=False
            )

            message = response.get("message", {})
            content = message.get("content", "")
            
            raw_api_calls = message.get("tool_calls")
            api_tool_calls = raw_api_calls if raw_api_calls is not None else []
            manual_tool_calls = self._extract_manual_json_tools(content)
            
            all_tools_to_run = api_tool_calls + manual_tool_calls

            if all_tools_to_run:
                self.memory.add_message(
                    role="assistant", 
                    content=content if manual_tool_calls else "", 
                    tool_calls=api_tool_calls if api_tool_calls else None
                )

                for tool_call in all_tools_to_run:
                    func_name = tool_call["function"]["name"]
                    arguments = tool_call["function"]["arguments"]
                    
                    print(f"\n[Agent Engine] 🛠️  Executing tool: {func_name}({arguments})")
                    
                    tool_result = registry.execute(func_name, arguments)
                    
                    formatted_result = f"Result of {func_name}: {str(tool_result)}"
                    self.memory.add_message("tool", formatted_result)
                
                loop_count += 1  
                continue
                
            else:
                self.memory.add_message("assistant", content)

                # TODO := add token-to-token streaming
                chunk_size = 10
                for i in range(0, len(content), chunk_size):
                    yield content[i:i+chunk_size]
                
                break
                
    def clear_session(self):
        self.memory.clear()