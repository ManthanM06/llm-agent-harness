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
        "You are an expert autonomous AI software assistant. "
        "You have access to tools to interact with the environment.\n"
        "Rules:\n"
        "1. When answering questions that require environment information or manipulating files (such as listing files, reading files, writing files, or checking current time), "
        "you MUST call the corresponding tools. NEVER guess or hallucinate environment data.\n"
        "2. If multiple pieces of information are needed, call all relevant tools before finalizing your answer.\n"
        "3. Once all necessary tool results are received, synthesize a clear, factual answer based strictly on the tool results.\n"
        "4. Do not re-invoke tools if you already have their results."
    )

config = AgentConfig()