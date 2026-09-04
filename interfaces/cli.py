"""
interfaces/cli.py
Interactive CLI application ('broo') for the LLM Agent Harness using Rich and Prompt Toolkit.
"""

import os
import sys
import argparse
from typing import Dict, Any, Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.text import Text
from rich.prompt import Confirm
from rich.align import Align
from rich import box

from core.agent import AgentEngine
from core.config import config
from skills.registry import skill_registry
from tools.registry import registry

console = Console()

BANNER_LINES = [
    "[bold cyan]██████╗ ██████╗  ██████╗  ██████╗ [/bold cyan]",
    "[bold cyan]██╔══██╗██╔══██╗██╔═══██╗██╔═══██╗[/bold cyan]",
    "[bold magenta]██████╔╝██████╔╝██║   ██║██║   ██║[/bold magenta]",
    "[bold magenta]██╔══██╗██╔══██╗██║   ██║██║   ██║[/bold magenta]",
    "[bold green]██████╔╝██║  ██║╚██████╔╝╚██████╔╝[/bold green]",
    "[bold green]╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ [/bold green]",
]

PROMPT_STYLE = Style.from_dict({
    "completion-menu.completion": "bg:#282a36 #f8f8f2",
    "completion-menu.completion.current": "bg:#bd93f9 #282a36 bold",
    "completion-menu.meta": "bg:#21222c #6272a4",
    "completion-menu.meta.current": "bg:#ff79c6 #282a36 bold",
    "scrollbar.background": "bg:#21222c",
    "scrollbar.button": "bg:#6272a4",
})

class BrooSlashCompleter(Completer):
    """
    Autocompletes slash commands (/help, /skills, /tools, /clear, /exit, etc.)
    and coding skills (/leetcode, /debug, etc.) when the user types '/'.
    Supports arrow key navigation and display metadata.
    """
    def __init__(self):
        self.builtin_commands = {
            "/help": "Show commands manual & usage guide",
            "/skills": "List all active coding & agent skills",
            "/tools": "List available tools & permission requirements",
            "/clear": "Clear conversation memory & terminal screen",
            "/exit": "Exit the Broo CLI",
            "/quit": "Exit the Broo CLI",
        }

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if text.startswith("/"):
            word = text.strip().split()[0] if text.strip() else "/"
            
            # Combine builtins and dynamically registered skills
            candidates: Dict[str, str] = dict(self.builtin_commands)
            for skill in skill_registry.get_all_skills():
                desc_short = (skill.description or "")[:45]
                candidates[skill.trigger.lower()] = f"{skill.name}: {desc_short}..."

            for cmd, desc in candidates.items():
                if cmd.lower().startswith(word.lower()):
                    yield Completion(
                        cmd,
                        start_position=-len(word),
                        display=cmd,
                        display_meta=desc
                    )

def render_banner() -> None:
    """Render the welcome banner and system information."""
    console.print()
    console.print(Align.center("\n".join(BANNER_LINES)))
    console.print()
    
    welcome_text = Text()
    welcome_text.append("⚡ Autonomous AI Assistant & Coding Agent Harness\n", style="bold white")
    welcome_text.append(f"• Model: ", style="dim")
    welcome_text.append(f"{config.MODEL_NAME}\n", style="bold green")
    welcome_text.append(f"• Working Directory: ", style="dim")
    welcome_text.append(f"{os.getcwd()}\n", style="bold yellow")
    welcome_text.append(f"• Sandboxed Tools: ", style="dim")
    welcome_text.append("File reads/writes restricted to working directory with permission prompts\n", style="italic cyan")
    welcome_text.append("\nType ", style="dim")
    welcome_text.append("/help", style="bold cyan")
    welcome_text.append(" for commands, ", style="dim")
    welcome_text.append("/skills", style="bold cyan")
    welcome_text.append(" for coding skills, or ", style="dim")
    welcome_text.append("/exit", style="bold cyan")
    welcome_text.append(" to quit.", style="dim")

    console.print(
        Panel(
            welcome_text,
            title="[bold green]Welcome to Broo[/bold green]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2)
        )
    )

def show_help() -> None:
    """Display interactive commands and usage manual."""
    table = Table(title="Broo CLI Commands & Shortcuts", box=box.ROUNDED, header_style="bold magenta")
    table.add_column("Command / Trigger", style="cyan", width=22)
    table.add_column("Description", style="white")

    table.add_row("/help", "Show this help message")
    table.add_row("/skills", "List all active coding and agent skills")
    table.add_row("/tools", "List available tools and permission requirements")
    table.add_row("/clear", "Clear conversation memory and reset session")
    table.add_row("/exit, /quit", "Exit the Broo CLI")
    table.add_row("<any text>", "Chat with the autonomous agent or ask questions")

    console.print(table)

def show_skills() -> None:
    """Display registered skills in a styled table."""
    skills = skill_registry.get_all_skills()
    table = Table(title="Registered Skills", box=box.ROUNDED, header_style="bold green")
    table.add_column("Trigger", style="bold cyan", width=14)
    table.add_column("Skill Name", style="bold white", width=22)
    table.add_column("Description", style="dim white")

    for s in skills:
        table.add_row(s.trigger, s.name, s.description)

    console.print(table)

def show_tools() -> None:
    """Display registered tools in a styled table."""
    tools = registry.get_all_tools()
    table = Table(title="Available System Tools", box=box.ROUNDED, header_style="bold blue")
    table.add_column("Tool Name", style="bold cyan", width=20)
    table.add_column("Requires Permission", style="bold yellow", justify="center", width=22)
    table.add_column("Description", style="dim white")

    for t in tools:
        name = t.__name__
        requires_perm = "🔒 Yes (Prompt)" if registry.requires_permission(name) else "✓ No (Auto)"
        doc = (t.__doc__ or "No description provided.").strip().split("\n")[0]
        table.add_row(name, requires_perm, doc)

    console.print(table)

def cli_permission_handler(tool_name: str, arguments: Dict[str, Any]) -> bool:
    """
    Interactive prompt asking user for permission before running a sensitive tool.
    Returns True if user permits, False otherwise.
    """
    perm_text = Text()
    perm_text.append(f"Tool Requested: ", style="bold white")
    perm_text.append(f"{tool_name}\n", style="bold cyan")

    if "file_path" in arguments:
        perm_text.append(f"Target File: ", style="bold white")
        perm_text.append(f"{arguments['file_path']}\n", style="bold yellow")

    if "content" in arguments:
        content_preview = str(arguments["content"])
        if len(content_preview) > 200:
            preview_str = content_preview[:200] + "... [truncated]"
        else:
            preview_str = content_preview
        perm_text.append(f"Content Length: ", style="bold white")
        perm_text.append(f"{len(content_preview)} chars\n", style="dim")
        perm_text.append(f"Preview:\n{preview_str}\n", style="italic")

    console.print()
    console.print(
        Panel(
            perm_text,
            title="[bold yellow]🔒 Permission Request[/bold yellow]",
            border_style="yellow",
            box=box.DOUBLE,
            padding=(0, 2)
        )
    )

    try:
        granted = Confirm.ask(
            "[bold yellow]Do you want to grant permission for this action?[/bold yellow]",
            default=False
        )
        if granted:
            console.print("[bold green]✓ Permission granted.[/bold green]")
        else:
            console.print("[bold red]✗ Permission denied by user.[/bold red]")
        return granted
    except (KeyboardInterrupt, EOFError):
        console.print("\n[bold red]✗ Action cancelled by user.[/bold red]")
        return False

class BrooCLI:
    def __init__(self):
        self.engine = AgentEngine(
            permission_handler=cli_permission_handler,
            on_skill_activated=self._on_skill_activated,
            on_tool_call=self._on_tool_call,
            on_tool_result=self._on_tool_result
        )

    def _on_skill_activated(self, skill: Any) -> None:
        console.print(f"\n[bold green]🎯 Skill Activated:[/bold green] [bold white]{skill.name}[/bold white] ([cyan]{skill.trigger}[/cyan])")

    def _on_tool_call(self, name: str, arguments: Dict[str, Any]) -> None:
        arg_summary = ", ".join(f"{k}={repr(v)[:50]}" for k, v in arguments.items())
        console.print(f"[dim]🛠️  Executing tool:[/dim] [cyan]{name}[/cyan]({arg_summary})")

    def _on_tool_result(self, name: str, result: str) -> None:
        trimmed = result.strip()
        if len(trimmed) > 120:
            trimmed = trimmed[:120] + "..."
        console.print(f"[dim]↳ Result ({name}):[/dim] [italic]{trimmed}[/italic]")

    def handle_command(self, cmd: str) -> bool:
        """
        Processes built-in CLI commands.
        Returns True if a command was handled and REPL should continue to next prompt.
        Returns False if not a built-in command (pass to agent).
        """
        clean = cmd.strip()
        first_token = clean.split()[0].lower() if clean else ""

        if first_token in ("/exit", "/quit", "exit", "quit"):
            console.print("\n[bold cyan]Broo session ended. Goodbye![/bold cyan]")
            sys.exit(0)

        if first_token == "/help":
            show_help()
            return True

        if first_token == "/skills":
            show_skills()
            return True

        if first_token == "/tools":
            show_tools()
            return True

        if first_token == "/clear":
            self.engine.clear_session()
            console.clear()
            render_banner()
            console.print("[green]✓ Conversation memory cleared.[/green]\n")
            return True

        return False

    def run_prompt(self, user_input: str) -> None:
        """Processes a single prompt through the agent and streams the response."""
        full_response = ""
        try:
            with console.status("[bold cyan]Broo is thinking...[/bold cyan]", spinner="dots"):
                chunks = self.engine.chat(user_input)
                try:
                    first_chunk = next(chunks)
                    full_response += first_chunk
                except StopIteration:
                    first_chunk = ""

            if first_chunk:
                for chunk in chunks:
                    full_response += chunk

            console.print()
            console.print(Panel(Markdown(full_response), title="[bold cyan]Broo[/bold cyan]", border_style="dim cyan", box=box.ROUNDED))
            console.print()
        except Exception as e:
            console.print(f"\n[bold red]Error running agent:[/bold red] {str(e)}")

    def start_repl(self) -> None:
        """Starts the interactive prompt loop."""
        render_banner()

        if not sys.stdin.isatty():
            # Non-interactive piped mode
            while True:
                try:
                    line = sys.stdin.readline()
                    if not line:
                        break
                    user_input = line.strip()
                    if not user_input:
                        continue
                    if self.handle_command(user_input):
                        continue
                    self.run_prompt(user_input)
                except (KeyboardInterrupt, EOFError):
                    break
            return

        completer = BrooSlashCompleter()
        session = PromptSession(
            completer=completer,
            complete_while_typing=True,
            style=PROMPT_STYLE
        )

        while True:
            try:
                prompt_html = HTML("<ansigreen><b>broo</b></ansigreen> <ansicyan><b>&gt;</b></ansicyan> ")
                user_input = session.prompt(prompt_html)
            except (KeyboardInterrupt, EOFError):
                console.print("\n[bold cyan]Session closed. Goodbye![/bold cyan]")
                break
            except Exception:
                try:
                    user_input = input("broo > ")
                except (KeyboardInterrupt, EOFError):
                    console.print("\n[bold cyan]Session closed. Goodbye![/bold cyan]")
                    break

            if not user_input or not user_input.strip():
                continue

            if self.handle_command(user_input):
                continue

            self.run_prompt(user_input)

def main() -> None:
    parser = argparse.ArgumentParser(description="Broo: Autonomous AI Agent CLI")
    parser.add_argument("prompt", nargs="*", help="Optional initial prompt to execute directly")
    args = parser.parse_args()

    cli = BrooCLI()
    if args.prompt:
        user_prompt = " ".join(args.prompt)
        render_banner()
        console.print(f"[bold green]broo > [/bold green]{user_prompt}")
        cli.run_prompt(user_prompt)
    else:
        cli.start_repl()

if __name__ == "__main__":
    main()
