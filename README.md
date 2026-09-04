# ⚡ Broo: Autonomous LLM Agent Harness

An autonomous, lightweight, zero-heavy-framework AI coding agent harness and interactive CLI built in Python. Designed for local LLMs (powered by `qwen2.5-coder:3b` via Ollama), Broo equips the model with sandboxed system tools, human-in-the-loop permission gating, specialized coding skills, and a modern Rich terminal interface.

---

## ✨ Features

- **🚀 Interactive CLI (`broo`)**:
  - Direct shell keyword execution: start with `broo` anywhere in your terminal.
  - Interactive slash autocompletion when typing `/` with arrow-key navigation and command descriptions.
  - Fixes terminal prompt truncation and prevents backspace deletion of prompt fields.
  - Rich Markdown rendering with syntax-highlighted code blocks.
- **🛡️ Sandboxed File Tools**:
  - `read_file` & `write_file`: strictly restricted to the current working directory (`os.getcwd()`).
  - Path traversal protection blocking `../` escaping, absolute external paths, and unauthorized access.
- **🔒 Human-In-The-Loop Permission Prompts**:
  - Whenever the agent requests to read or write a file, an interactive permission dialog prompts the user (`[y/N]`) with file paths and content previews before proceeding.
- **🎯 Extensible Coding Skills**:
  - `/leetcode`: Solves LeetCode problems with structured Category, Intuition, Algorithm, C++ code, and Complexities.
  - `/debug`: Diagnoses bugs, identifies root causes, and outputs verified fixes.
  - `/refactor`: Refactors code for readability, performance, modularity, and clean code principles.
  - `/testgen`: Generates comprehensive unit tests covering edge cases and boundary conditions.
  - `/explain`: Breaks down complex algorithms, data flows, and architectural mechanics.
  - `/docstring`: Adds standardized docstrings (Google/NumPy/Sphinx) and comprehensive type annotations.
- **🧠 Native Agent Architecture**:
  - Zero heavy abstractions (no LangChain / LlamaIndex bloat).
  - Sliding context window managing token usage and long conversations.
  - Robust JSON Schema tool reflection and dual-mode tool call parsing.

---

## 🏗️ Architecture Overview

```
llm-agent-harness/
├── broo                  # Shell launcher script (symlinked to ~/.local/bin/broo)
├── pyproject.toml        # Project metadata & console_scripts entrypoint
├── requirements.txt      # Core dependencies (ollama, rich, prompt_toolkit, pydantic)
├── core/
│   ├── agent.py          # AgentEngine: tool-calling loop, cycle detection & callbacks
│   ├── config.py         # Model parameters, context window, and system instructions
│   └── memory.py         # ChatMemory: sliding-window conversation history
├── interfaces/
│   └── cli.py            # Rich CLI REPL with prompt_toolkit autocompletion & dialogs
├── skills/
│   ├── base.py           # BaseSkill contract
│   ├── registry.py       # Dynamic skill discovery and trigger matching
│   ├── leetcode.py       # /leetcode skill
│   ├── debug.py          # /debug skill
│   ├── refactor.py       # /refactor skill
│   ├── testgen.py        # /testgen skill
│   ├── explain.py        # /explain skill
│   └── docstring.py      # /docstring skill
├── tools/
│   ├── registry.py       # ToolRegistry with permission hooks and tool execution
│   └── system_tools.py   # Sandboxed get_current_time, list_files, read_file, write_file
└── tests/                # Automated verification suites
```

---

## 🚀 Quickstart

### 1. Prerequisites
- **Python 3.10+**
- **Ollama** installed and running:
  ```bash
  ollama run qwen2.5-coder:3b
  ```

### 2. Installation
Clone the repository and install in editable mode:
```bash
git clone https://github.com/ManthanM06/llm-agent-harness.git
cd llm-agent-harness

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### 3. Launching Broo
Simply run `broo` in your terminal:
```bash
broo
```
Or execute a one-shot query directly:
```bash
broo "What files are in the working directory?"
```

---

## 💡 Using the CLI

### Built-in Slash Commands
| Command | Description |
| :--- | :--- |
| `/help` | Display CLI commands manual and shortcuts |
| `/skills` | Display all registered coding skills and triggers |
| `/tools` | Display available system tools and permission requirements |
| `/copy [n]` | Copy code block #n (or latest) to system clipboard |
| `/clear` | Clear conversation memory and reset session |
| `/exit`, `/quit` | Exit the Broo session |

### Available Skills
Type `/` to view the interactive autocomplete dropdown. Navigate with the **Up/Down arrow keys** and press **Tab** or **Enter**:
- `/leetcode <problem description>`
- `/debug <code snippet with bug>`
- `/refactor <code snippet>`
- `/testgen <function or module>`
- `/explain <code or algorithm>`
- `/docstring <untyped code snippet>`

### Sandboxed File Tools & Permissions
When Broo wants to read or write a file in the working directory, it displays an interactive prompt:
```
╔═══════════════════════════ 🔒 Permission Request ════════════════════════════╗
║  Tool Requested: write_file                                                  ║
║  Target File: example.py                                                     ║
║  Content Length: 42 chars                                                    ║
║  Preview:                                                                    ║
║  print('Hello from Broo!')                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
Do you want to grant permission for this action? [y/N]:
```
- Type `y` to allow the action.
- Type `n` or press Enter to deny the action. Broo will adapt its response accordingly.

### Real-Time Token Streaming & Code Copy Boxes
- **Token-by-Token Streaming:** Responses stream live token-by-token directly to your terminal with real-time feedback so you never have to wait for large responses in silence.
- **Top-Right Copy Button Icon:** Code blocks are framed in a rounded Monokai syntax-highlighted panel featuring a dedicated `[📋 Copy: /copy]` button in the top-right corner.
- **Instant Clipboard Integration:** Generated code blocks are automatically copied to your system clipboard (ready for `Ctrl+V`). You can also copy any specific code block anytime using `/copy [block_number]`.

---

## 🧪 Running Tests

Run the test suites:
```bash
# Test sandboxed file tools and path traversal protection
.venv/bin/python -m unittest tests/test_file_tools.py

# Test permission prompts and sensitive tool gating
.venv/bin/python -m unittest tests/test_permissions.py

# Test CLI commands and autocompletion
.venv/bin/python -m unittest tests/test_cli.py
```

---

## 📄 License
MIT License.
