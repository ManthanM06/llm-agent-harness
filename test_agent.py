"""
Tests the full Agent Engine, ensuring it can autonomously decide to use tools.
"""
from core.agent import AgentEngine

def test_full_loop():
    engine = AgentEngine()
    
    print("[*] Starting Agent Engine Test...")
    print("[*] Prompt: 'What time is it right now (offset 5.5), and what files are in the current directory?'\n")
    
    prompt = "What time is it right now (use offset 5.5), and what files are in the current directory?"
    
    # The chat method returns a generator (yielding chunks of text)
    print("Agent Response: ", end="", flush=True)
    for chunk in engine.chat(prompt):
        print(chunk, end="", flush=True)
    
    print("\n\n[*] Test Complete.")

if __name__ == "__main__":
    test_full_loop()