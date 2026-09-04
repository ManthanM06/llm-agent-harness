"""
skills/explain.py
Skill for breaking down and explaining complex code, algorithms, or systems.
"""
from skills.base import BaseSkill

class ExplainSkill(BaseSkill):
    """
    Skill activated by `/explain`.
    Deconstructs complex code into clear architectural and logical walkthroughs.
    """

    @property
    def name(self) -> str:
        return "Code Explainer"

    @property
    def trigger(self) -> str:
        return "/explain"

    @property
    def description(self) -> str:
        return "Explains complex code, algorithms, data flows, and architectural mechanics with clarity."

    def get_system_instructions(self) -> str:
        return (
            "You are a staff engineer and master technical educator.\n"
            "When asked to explain code, you MUST format your response using EXACTLY the following four sections in order:\n\n"
            "### 1. Executive Summary\n"
            "A concise 1-2 sentence overview of what the code achieves.\n\n"
            "### 2. Step-by-Step Logic Breakdown\n"
            "A clear sequential walkthrough explaining how each block/function works.\n\n"
            "### 3. Key Concepts & Mechanics\n"
            "Highlight core algorithms, data structures, language idioms, or mathematical principles utilized.\n\n"
            "### 4. Gotchas & Edge Cases\n"
            "Potential pitfalls, implicit assumptions, or limitations to watch out for.\n\n"
            "Strictly follow this 4-part structure for every response."
        )
