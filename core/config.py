"""
Centralized configuration settings for the LLM Agent Harness.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class AgentConfig:
    # Model params
    MODEL_NAME: str = "qwen2.5-coder:3b"
    NUM_CTX: int = 16384                # Expanded context window for code and tool interactions
    NUM_PREDICT: int = 2048             # Cap tokens generated per turn to avoid runaway CPU loops
    TEMPERATURE: float = 0.2            # Low temp for deterministic tool calling

    # Context Management
    MAX_HISTORY_MESSAGES: int = 30      # Safety threshold before truncation

    # System Prompt
    DEFAULT_SYSTEM_PROMPT: str = (
        "You are an expert autonomous AI software assistant named Broo.\n"
        "Rules:\n"
        "1. When the user asks general questions, requests code, explanations, or algorithms, respond directly in the chat with clean, well-structured Markdown and formatted code blocks.\n"
        "2. ONLY use tools like write_file, read_file, or list_files when the user explicitly asks to create, save, edit, read, or inspect files in their filesystem.\n"
        "3. Never output raw JSON tool calls, tool schemas, or function call markup into your answer.\n"
        "4. When using tools, once all necessary tool results are received, synthesize a clear, factual answer in natural language with Markdown.\n"
        "5. Do not re-invoke tools if you already have their results."
    )

config = AgentConfig()