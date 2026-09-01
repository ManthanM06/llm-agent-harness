"""
Centralized configuration settings for the LLM Agent Harness.
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class AgentConfig:
    # Model params
    MODEL_NAME: str = "qwen2.5-coder:3b"
    NUM_CTX: int = 16384                # Expanded context window for code and tool interactions
    TEMPERATURE: float = 0.2            # Low temp for deterministic tool calling

    # Context Management
    MAX_HISTORY_MESSAGES: int = 30      # Safety threshold before truncation

    # System Prompt
    DEFAULT_SYSTEM_PROMPT: str = (
        "You are an expert autonomous AI software assistant. "
        "You have access to functions (tools) to interact with the environment. "
        "When a user asks a question that requires data you do not have, you MUST use the provided tools. "
        "Do NOT write out JSON code blocks for tool calls. You must use the official tool calling format "
        "provided by your environment."
    )

config = AgentConfig()