"""
skills/leetcode.py
Skill for solving LeetCode style algorithmic coding questions with a strict structured format.
"""
from skills.base import BaseSkill

class LeetCodeSkill(BaseSkill):
    """
    Skill activated by `/leetcode`.
    Instructs the LLM to structure algorithmic solutions with:
    - Question Category (Array, Two Pointers, Dynamic Programming, etc.)
    - Intuition
    - Algorithm (English in bullet points)
    - Code (Clean, optimal C++)
    - Time and Space Complexity
    """

    @property
    def name(self) -> str:
        return "LeetCode Assistant"

    @property
    def trigger(self) -> str:
        return "/leetcode"

    @property
    def description(self) -> str:
        return "Solves LeetCode style problems in a structured format with Category, Intuition, Algorithm, C++ code, and Complexities."

    def get_system_instructions(self) -> str:
        return (
            "You are an expert competitive programming and LeetCode algorithmic specialist.\n"
            "When presented with a coding problem, you MUST format your response using EXACTLY the following five sections in order:\n\n"
            "### 1. Question Category\n"
            "State the primary problem categories and data structures (e.g., Array, Two Pointers, Hash Table, Dynamic Programming, Binary Search, etc.).\n\n"
            "### 2. Intuition\n"
            "Explain the core insight, mental model, and reasoning behind how to solve the problem efficiently.\n\n"
            "### 3. Algorithm\n"
            "Provide the step-by-step algorithm in clear, concise English bullet points.\n\n"
            "### 4. Code (C++)\n"
            "Provide optimal, clean, and modern C++ solution code inside a ```cpp code block, including necessary includes and comments.\n\n"
            "### 5. Time and Space Complexity\n"
            "- **Time Complexity**: Big-O notation with concise justification.\n"
            "- **Space Complexity**: Big-O notation with concise justification.\n\n"
            "Strictly follow this 5-part structure for every response."
        )
