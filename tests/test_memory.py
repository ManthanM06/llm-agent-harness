"""
tests/test_memory.py
Verifies the ChatMemory sliding window logic and system prompt persistence.
"""
import unittest
from core.memory import ChatMemory
from core.config import config

class TestChatMemory(unittest.TestCase):
    def test_initial_state(self):
        system_prompt = "You are a test assistant."
        memory = ChatMemory(system_prompt=system_prompt)
        self.assertEqual(len(memory.get_messages()), 1)
        self.assertEqual(memory.get_messages()[0]["role"], "system")
        self.assertEqual(memory.get_messages()[0]["content"], system_prompt)

    def test_sliding_window_truncation(self):
        system_prompt = "You are a test assistant."
        memory = ChatMemory(system_prompt=system_prompt)
        total_to_add = config.MAX_HISTORY_MESSAGES + 10
        for i in range(total_to_add):
            memory.add_message("user" if i % 2 == 0 else "assistant", f"Message {i}")

        messages = memory.get_messages()
        self.assertEqual(len(messages), config.MAX_HISTORY_MESSAGES)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], system_prompt)
        self.assertEqual(messages[-1]["content"], f"Message {total_to_add - 1}")

    def test_clear_memory(self):
        system_prompt = "You are a test assistant."
        memory = ChatMemory(system_prompt=system_prompt)
        memory.add_message("user", "Hello")
        memory.add_message("assistant", "Hi")
        self.assertEqual(len(memory.get_messages()), 3)
        memory.clear()
        self.assertEqual(len(memory.get_messages()), 1)
        self.assertEqual(memory.get_messages()[0]["role"], "system")

if __name__ == "__main__":
    unittest.main()
