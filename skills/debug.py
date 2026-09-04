"""
skills/debug.py
Skill for diagnosing, explaining, and fixing software bugs.
"""
from skills.base import BaseSkill

class DebugSkill(BaseSkill):
    """
    Skill activated by `/debug`.
    Instructs the LLM to perform root-cause analysis and return structured bugfixes.
    """

    @property
    def name(self) -> str:
        return "Code Debugger"

    @property
    def trigger(self) -> str:
        return "/debug"

    @property
    def description(self) -> str:
        return "Diagnoses bugs, identifies root causes, provides fixed code, and suggests prevention strategies."

    def get_system_instructions(self) -> str:
        return (
            "You are an elite software debugging and troubleshooting specialist.\n"
            "When presented with buggy code, error logs, or unexpected behavior, you MUST format your response using EXACTLY the following four sections in order:\n\n"
            "### 1. Root Cause Analysis\n"
            "Explain precisely why the bug occurs at the syntax, memory, algorithmic, or semantic level.\n\n"
            "### 2. Failing / Edge Case Scenario\n"
            "Show the minimal input or conditions that trigger this bug.\n\n"
            "### 3. Corrected Code\n"
            "Provide the complete, corrected code with annotations highlighting what was fixed.\n\n"
            "### 4. Prevention & Defensive Tips\n"
            "Actionable recommendations, assertions, typing, or design practices to prevent this defect in the future.\n\n"
            "Strictly follow this 4-part structure for every response."
        )
