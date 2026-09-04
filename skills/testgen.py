"""
skills/testgen.py
Skill for generating comprehensive unit test suites with boundary and edge case coverage.
"""
from skills.base import BaseSkill

class TestGenSkill(BaseSkill):
    """
    Skill activated by `/testgen`.
    Instructs the LLM to design a complete unit test suite with edge cases.
    """

    @property
    def name(self) -> str:
        return "Unit Test Generator"

    @property
    def trigger(self) -> str:
        return "/testgen"

    @property
    def description(self) -> str:
        return "Generates thorough unit tests covering happy paths, edge cases, boundaries, and error scenarios."

    def get_system_instructions(self) -> str:
        return (
            "You are a lead QA and test automation engineer.\n"
            "When given a code snippet, function, or class, you MUST format your response using EXACTLY the following three sections in order:\n\n"
            "### 1. Test Scenarios Matrix\n"
            "Bullet points or table of test cases covering:\n"
            "- Happy paths / standard inputs\n"
            "- Boundary values (empty, zero, max/min bounds)\n"
            "- Error conditions & invalid inputs\n\n"
            "### 2. Unit Test Suite Code\n"
            "Provide executable, production-ready unit tests using the standard test framework for the language (e.g., pytest for Python, GoogleTest/Catch2 for C++, JUnit for Java, Jest for JS/TS) in a code block.\n\n"
            "### 3. Edge Cases Explained\n"
            "Briefly explain subtle edge cases and failure modes targeted by the tests.\n\n"
            "Strictly follow this 3-part structure for every response."
        )
