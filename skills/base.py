"""
skills/base.py
Base abstraction for skills in the LLM Agent Harness.
"""
from abc import ABC, abstractmethod

class BaseSkill(ABC):
    """
    Abstract base class for all agent skills.
    A skill encapsulates domain-specific prompting, parsing, or toolsets
    that can be triggered dynamically (e.g., via a slash command like `/leetcode`).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the skill."""
        pass

    @property
    @abstractmethod
    def trigger(self) -> str:
        """Command trigger string, e.g. '/leetcode'."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Short description of what the skill does."""
        pass

    def matches(self, prompt: str) -> bool:
        """Checks if the user prompt activates this skill."""
        cleaned = prompt.strip()
        return cleaned == self.trigger or cleaned.startswith(f"{self.trigger} ")

    def extract_content(self, prompt: str) -> str:
        """Extracts the remaining user prompt after the skill trigger."""
        cleaned = prompt.strip()
        if cleaned == self.trigger:
            return ""
        if cleaned.startswith(f"{self.trigger} "):
            return cleaned[len(self.trigger):].strip()
        return cleaned

    @abstractmethod
    def get_system_instructions(self) -> str:
        """Returns the specialized system instructions to guide model response format and logic."""
        pass
