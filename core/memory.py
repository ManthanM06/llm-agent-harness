"""
core/memory.py
Manages conversation history and sliding-window context truncation.
"""
from typing import List, Dict, Any
from core.config import config

class ChatMemory:
    def __init__(self, system_prompt: str = config.DEFAULT_SYSTEM_PROMPT):
        """
        Initializes the memory with a system prompt.
        The messages array holds standard OpenAI/Ollama dicts:
        {"role": "user|assistant|tool|system", "content": "..."}
        """
        self.system_prompt = system_prompt
        self.messages: List[Dict[str, Any]] = []
        
        self.add_message("system", self.system_prompt)

    def add_message(self, role: str, content: str, **kwargs) -> None:
        msg = {"role": role, "content": content}
        for k, v in kwargs.items():
            if v is not None:
                msg[k] = v
            
        self.messages.append(msg)
        self._enforce_sliding_window()

    def get_messages(self) -> List[Dict[str, Any]]:
        return self.messages

    def _enforce_sliding_window(self) -> None:
        if len(self.messages) > config.MAX_HISTORY_MESSAGES:
            keep_count = config.MAX_HISTORY_MESSAGES
            
            system_msg = self.messages[0]
            recent_msgs = self.messages[-(keep_count - 1):]
            
            self.messages = [system_msg] + recent_msgs

    def clear(self) -> None:
        self.messages = []
        self.add_message("system", self.system_prompt)