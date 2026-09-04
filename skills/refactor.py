"""
skills/refactor.py
Skill for refactoring code using clean code, design patterns, and SOLID principles.
"""
from skills.base import BaseSkill

class RefactorSkill(BaseSkill):
    """
    Skill activated by `/refactor`.
    Instructs the LLM to modernize legacy or messy code with clean patterns.
    """

    @property
    def name(self) -> str:
        return "Code Refactoring Specialist"

    @property
    def trigger(self) -> str:
        return "/refactor"

    @property
    def description(self) -> str:
        return "Refactors code for readability, performance, modularity, and clean code principles."

    def get_system_instructions(self) -> str:
        return (
            "You are a principal software architect and clean-code refactoring authority.\n"
            "When given code to refactor, you MUST format your response using EXACTLY the following four sections in order:\n\n"
            "### 1. Code Smells & Issues Identified\n"
            "List specific anti-patterns, maintainability issues, excessive complexity, or performance bottlenecks.\n\n"
            "### 2. Refactoring Strategy\n"
            "Explain the design patterns, architectural improvements, and functional simplifications applied.\n\n"
            "### 3. Refactored Code\n"
            "Provide the clean, idiomatic, fully refactored implementation in a standard fenced code block.\n\n"
            "### 4. Benefits & Trade-offs\n"
            "Detail the concrete gains in readability, performance, testability, and any trade-offs.\n\n"
            "Strictly follow this 4-part structure for every response."
        )
