"""
skills/docstring.py
Skill for generating type hints, comprehensive docstrings, and usage examples.
"""
from skills.base import BaseSkill

class DocstringSkill(BaseSkill):
    """
    Skill activated by `/docstring`.
    Generates standard docstrings and type annotations for functions or classes.
    """

    @property
    def name(self) -> str:
        return "Documentation & Typing Specialist"

    @property
    def trigger(self) -> str:
        return "/docstring"

    @property
    def description(self) -> str:
        return "Adds comprehensive type hints, standardized docstrings (Google/NumPy/Sphinx), and runnable usage examples."

    def get_system_instructions(self) -> str:
        return (
            "You are a technical documentation engineer and code standards specialist.\n"
            "When given unannotated or undocumented code, you MUST format your response using EXACTLY the following three sections in order:\n\n"
            "### 1. Interface Overview\n"
            "Brief summary of the function/class purpose, inputs, and return values.\n\n"
            "### 2. Fully Typed & Documented Code\n"
            "Provide the complete code enriched with strict type hints and professional Google-style docstrings (including Args, Returns, and Raises sections) in a code block.\n\n"
            "### 3. Usage Example\n"
            "A minimal, working example showing how to call the function/class properly.\n\n"
            "Strictly follow this 3-part structure for every response."
        )
