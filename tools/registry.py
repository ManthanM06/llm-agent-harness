"""
Manages the registration and mapping of Python functions to LLM tools.
"""

from typing import Callable, Dict, Any, List, Optional, Set

from tools.system_tools import get_current_time, list_files, read_file, write_file

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._sensitive_tools: Set[str] = set()
        self._permission_handler: Optional[Callable[[str, Dict[str, Any]], bool]] = None

        # Register default tools
        self.register(get_current_time)
        self.register(list_files)
        self.register(read_file, requires_permission=True)
        self.register(write_file, requires_permission=True)

    def register(self, func: Callable, requires_permission: bool = False) -> None:
        """Register a tool function, optionally marking it as requiring user permission."""
        name = func.__name__
        self._tools[name] = func
        if requires_permission:
            self._sensitive_tools.add(name)

    def set_permission_handler(self, handler: Optional[Callable[[str, Dict[str, Any]], bool]]) -> None:
        """Set a callback to confirm tool execution when permissions are required."""
        self._permission_handler = handler

    def requires_permission(self, name: str) -> bool:
        """Check if a given tool requires user permission."""
        return name in self._sensitive_tools

    def get_tools(self, name: str) -> Callable | None:
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

        # Permission check
        if self.requires_permission(name) and self._permission_handler is not None:
            try:
                granted = self._permission_handler(name, kwargs)
                if not granted:
                    return f"Execution cancelled: User denied permission to execute '{name}'."
            except Exception as e:
                return f"Execution cancelled: Permission check error for '{name}': {str(e)}"

        try:
            result = tool(**kwargs)
            return str(result)
        except Exception as e:
            return f"Error executing '{name}': {str(e)}"

registry = ToolRegistry()





