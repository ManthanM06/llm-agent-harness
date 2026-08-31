# Autonomous Local LLM Agent Harness

A lightweight, zero-framework autonomous agent harness built from scratch in Python for local LLMs (specifically `qwen2.5-coder:3b` via Ollama).

## Features
- **Zero Heavy Frameworks:** Custom-built execution engine and context manager without LangChain or LlamaIndex.
- **Native Tool Calling:** Dynamic Python tool registration with JSON Schema reflection.
- **Sliding Context Window:** Adaptive conversation history manager preventing context overflow.
- **Multi-Interface Architecture:** Modular design supporting CLI and Web interfaces.

## Quickstart
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama run qwen2.5-coder:3b
python main.py