"""
test_coding_skills.py
Comprehensive test suite for the newly integrated coding skills:
- /debug
- /refactor
- /testgen
- /explain
- /docstring
"""
from core.agent import AgentEngine

SKILL_TESTS = [
    {
        "skill": "/debug",
        "name": "Code Debugger",
        "prompt": (
            "/debug def find_max(numbers):\n"
            "    max_val = 0\n"
            "    for n in numbers:\n"
            "        if n > max_val:\n"
            "            max_val = n\n"
            "    return max_val\n"
            "# Bug: When passed all negative numbers like [-5, -2, -9], it returns 0 instead of -2."
        ),
        "expected_sections": [
            "Root Cause",
            "Failing",
            "Corrected Code",
            "Prevention"
        ]
    },
    {
        "skill": "/refactor",
        "name": "Code Refactoring Specialist",
        "prompt": (
            "/refactor def process_users(data):\n"
            "    res = []\n"
            "    for i in range(len(data)):\n"
            "        if data[i]['active'] == True:\n"
            "            if data[i]['age'] >= 18:\n"
            "                res.append(data[i]['name'].upper())\n"
            "    return res"
        ),
        "expected_sections": [
            "Code Smell",
            "Refactoring Strategy",
            "Refactored Code",
            "Benefit"
        ]
    },
    {
        "skill": "/testgen",
        "name": "Unit Test Generator",
        "prompt": (
            "/testgen def divide(a: float, b: float) -> float:\n"
            "    if b == 0:\n"
            "        raise ValueError('Cannot divide by zero')\n"
            "    return a / b"
        ),
        "expected_sections": [
            "Test Scenario",
            "Unit Test",
            "Edge Case"
        ]
    },
    {
        "skill": "/explain",
        "name": "Code Explainer",
        "prompt": (
            "/explain def binary_search(arr, target):\n"
            "    low, high = 0, len(arr) - 1\n"
            "    while low <= high:\n"
            "        mid = (low + high) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            low = mid + 1\n"
            "        else:\n"
            "            high = mid - 1\n"
            "    return -1"
        ),
        "expected_sections": [
            "Executive Summary",
            "Step-by-Step",
            "Key Concept",
            "Gotcha"
        ]
    },
    {
        "skill": "/docstring",
        "name": "Documentation & Typing Specialist",
        "prompt": (
            "/docstring def calculate_compound_interest(principal, rate, times_per_year, years):\n"
            "    return principal * (1 + rate / times_per_year) ** (times_per_year * years)"
        ),
        "expected_sections": [
            "Interface Overview",
            "Fully Typed",
            "Usage Example"
        ]
    }
]

def run_tests():
    print("=" * 70)
    print("  TESTING NEW CODING SKILLS: /debug, /refactor, /testgen, /explain, /docstring")
    print("=" * 70)

    passed_count = 0

    for idx, test in enumerate(SKILL_TESTS, 1):
        skill_cmd = test["skill"]
        skill_name = test["name"]
        print("-" * 70)
        print(f"[*] Test {idx}/{len(SKILL_TESTS)}: {skill_cmd} ({skill_name})")
        print(f"[*] Prompt snippet: {test['prompt'][:80]}...\n")

        engine = AgentEngine()
        response_chunks = []
        for chunk in engine.chat(test["prompt"]):
            print(chunk, end="", flush=True)
            response_chunks.append(chunk)

        full_response = "".join(response_chunks).lower()
        print("\n")

        # Verify expected sections
        missing = []
        for section in test["expected_sections"]:
            if section.lower() not in full_response:
                missing.append(section)

        if not missing:
            print(f"[✔] {skill_cmd} passed all structural requirements!")
            passed_count += 1
        else:
            print(f"[!] {skill_cmd} missing section(s): {missing}")

    print("\n" + "=" * 70)
    print(f"[*] Coding Skills Test Summary: {passed_count}/{len(SKILL_TESTS)} skills verified successfully.")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
