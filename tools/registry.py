"""
Manages the registration and mapping of Python functions to LLM tools.
"""

from typing import Callable, Dict, Any, List

from tools.system_tools import get_current_time, list_files

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}

        self.register(get_current_time)
        self.register(list_files)

    def register(self,func : Callable) -> None:
        self._tools[func.__name__] = func

    def get_tools(self, name:str) -> Callable | None:
        return self._tools.get(name)

    def get_all_tools(self) -> List[Callable]:
        return list(self._tools.values())

    def execute(self, name: str, arguments: Dict[str, Any] | str | None = None) -> str:
        tool = self.get_tools(name)
        if not tool:
            return f"Error: Tool '{name}' not found in registry."

        # Normalize arguments
        if arguments is None:
            kwargs = {}
        elif isinstance(arguments, str):
            import json
            try:
                kwargs = json.loads(arguments)
                if not isinstance(kwargs, dict):
                    kwargs = {}
            except Exception as e:
                return f"Error parsing arguments for '{name}': {str(e)}"
        elif isinstance(arguments, dict):
            kwargs = arguments
        else:
            kwargs = {}

        try:
            result = tool(**kwargs)
            return str(result)
        except Exception as e:
            return f"Error executing '{name}': {str(e)}"

registry = ToolRegistry()




