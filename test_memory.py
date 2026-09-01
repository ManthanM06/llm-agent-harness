"""
Verifies the ChatMemory sliding window logic.
"""

from core.memory import ChatMemory
from core.config import config

def test_sliding_window():
    print(f"[*] Initializing Memory (Max limit set to: {config.MAX_HISTORY_MESSAGES})...")

    memory = ChatMemory(system_prompt="You are a test bot.")
    
    print("[*] Adding 6 messages (which should trigger truncation)...")
    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Reply 1")
    memory.add_message("user", "Message 2")
    memory.add_message("assistant", "Reply 2")
    memory.add_message("user", "Message 3")
    memory.add_message("assistant", "Reply 3")
    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Reply 1")
    memory.add_message("user", "Message 2")
    memory.add_message("assistant", "Reply 2")
    memory.add_message("user", "Message 3")
    memory.add_message("assistant", "Reply 3")
    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Reply 1")
    memory.add_message("user", "Message 2")
    memory.add_message("assistant", "Reply 2")
    memory.add_message("user", "Message 3")
    memory.add_message("assistant", "Reply 3")
    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Reply 1")
    memory.add_message("user", "Message 2")
    memory.add_message("assistant", "Reply 2")
    memory.add_message("user", "Message 3")
    memory.add_message("assistant", "Reply 3")
    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Reply 1")
    memory.add_message("user", "Message 2")
    memory.add_message("assistant", "Reply 2")
    memory.add_message("user", "Message 3")
    memory.add_message("assistant", "Reply 3")
    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Reply 1")
    memory.add_message("user", "Message 2")
    memory.add_message("assistant", "Reply 2")
    memory.add_message("user", "Message 3")
    memory.add_message("assistant", "Reply 3")

    final_messages = memory.get_messages()
    
    print(f"\n[+] Total messages in memory: {len(final_messages)}")
    for i, msg in enumerate(final_messages):
        print(f"    {i}: [{msg['role']}] {msg.get('content', '')}")
        

if __name__ == "__main__":
    test_sliding_window()