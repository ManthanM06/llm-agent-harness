"""
test_skill.py
Automated test suite for the Skills system and the /leetcode skill.
Tests at least 5 classic algorithmic problems across different data structures and patterns.
"""
from core.agent import AgentEngine

QUESTIONS = [
    {
        "title": "Two Sum",
        "prompt": "/leetcode Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice."
    },
    {
        "title": "Valid Palindrome",
        "prompt": "/leetcode A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Given a string s, return true if it is a palindrome, or false otherwise."
    },
    {
        "title": "Maximum Subarray (Kadane's Algorithm)",
        "prompt": "/leetcode Given an integer array nums, find the subarray with the largest sum, and return its sum."
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "prompt": "/leetcode You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction."
    },
    {
        "title": "Invert Binary Tree",
        "prompt": "/leetcode Given the root of a binary tree, invert the tree, and return its root."
    }
]

REQUIRED_SECTIONS = [
    "Question Category",
    "Intuition",
    "Algorithm",
    "Code",
    "Complexity"
]

def check_structure(response_text: str) -> bool:
    """Verifies that all required sections are present in the response."""
    lower_text = response_text.lower()
    missing = []
    for section in REQUIRED_SECTIONS:
        if section.lower() not in lower_text:
            missing.append(section)
    if missing:
        print(f"    [!] Warning: Missing section(s): {missing}")
        return False
    return True

def test_leetcode_skill():
    print("=" * 70)
    print("  TESTING SKILLS SYSTEM: /leetcode SKILL ON 5 QUESTIONS")
    print("=" * 70)

    # 1. Test empty skill trigger (help/usage message)
    print("\n[*] Testing Empty Trigger: '/leetcode'...")
    engine_help = AgentEngine()
    help_output = "".join(engine_help.chat("/leetcode"))
    print(help_output)
    assert "Skill Activated: LeetCode Assistant" in help_output, "Failed empty trigger test"
    print("[✔] Empty trigger test passed!\n")

    # 2. Test 5 LeetCode Questions
    passed_count = 0

    for idx, q in enumerate(QUESTIONS, 1):
        print("-" * 70)
        print(f"[*] Question {idx}/5: {q['title']}")
        print(f"[*] Prompt: {q['prompt'][:100]}...\n")

        engine = AgentEngine()
        response_chunks = []
        for chunk in engine.chat(q["prompt"]):
            print(chunk, end="", flush=True)
            response_chunks.append(chunk)

        full_response = "".join(response_chunks)
        print("\n")

        has_structure = check_structure(full_response)
        has_cpp_code = "```cpp" in full_response or "```c++" in full_response or "class Solution" in full_response or "#include" in full_response
        
        if has_structure and has_cpp_code:
            print(f"[✔] Question {idx} passed all structural requirements!")
            passed_count += 1
        else:
            print(f"[!] Question {idx} completed with structural warnings (Structure: {has_structure}, C++: {has_cpp_code})")

    print("\n" + "=" * 70)
    print(f"[*] Skill Test Summary: {passed_count}/{len(QUESTIONS)} questions fully structured and verified.")
    print("=" * 70)

if __name__ == "__main__":
    test_leetcode_skill()
