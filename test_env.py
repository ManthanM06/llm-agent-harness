"""
Verifies the local environment and connection to Ollama.
"""

import sys
import ollama
from core.config import config

def test_connections():
    print(f"[*] Checking connection to Ollama for model: {config.MODEL_NAME}...")
    try:
        response = ollama.chat(
            model=config.MODEL_NAME,
            messages=[{"role":"user", "content":"Respond with 'SYSTEM_READY' if you can read this."}],
            options={"num_ctx":2048}
        )
        reply = response["message"]["content"].strip()
        print(f"[+] Model response: {reply}")
        print("[✔] Environment verified successfully!")
    except Exception as e:
        print(f"[!] Verification failed: {e}", file=sys.stderr)
        print("[!] Ensure Ollama is running (`ollama serve`) and the model is downloaded.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    test_connections()