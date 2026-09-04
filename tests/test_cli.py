"""
tests/test_cli.py
Verifies the Broo CLI helpers, rendering functions, command handling, and permission prompts.
"""
import unittest
from unittest.mock import patch
from prompt_toolkit.document import Document
from interfaces.cli import (
    render_banner,
    show_help,
    show_skills,
    show_tools,
    cli_permission_handler,
    BrooCLI,
    BrooSlashCompleter
)

class TestCLI(unittest.TestCase):
    def test_rendering_functions(self):
        # Ensure rendering components execute cleanly without throwing
        render_banner()
        show_help()
        show_skills()
        show_tools()

    def test_command_dispatcher(self):
        cli = BrooCLI()
        self.assertTrue(cli.handle_command("/help"))
        self.assertTrue(cli.handle_command("/skills"))
        self.assertTrue(cli.handle_command("/tools"))
        self.assertTrue(cli.handle_command("/clear"))
        self.assertFalse(cli.handle_command("Hello world"))
        self.assertFalse(cli.handle_command("/debug test code"))

    def test_permission_prompt_grant(self):
        with patch("rich.prompt.Confirm.ask", return_value=True):
            granted = cli_permission_handler("write_file", {"file_path": "demo.py", "content": "print(1)"})
            self.assertTrue(granted)

    def test_permission_prompt_deny(self):
        with patch("rich.prompt.Confirm.ask", return_value=False):
            denied = cli_permission_handler("write_file", {"file_path": "demo.py", "content": "print(1)"})
            self.assertFalse(denied)

    def test_slash_completer(self):
        completer = BrooSlashCompleter()

        # Root slash gives all commands and skills
        completions_root = list(completer.get_completions(Document("/"), None))
        comp_texts_root = [c.text for c in completions_root]
        for cmd in ["/help", "/skills", "/tools", "/clear", "/exit", "/debug", "/refactor", "/leetcode"]:
            self.assertIn(cmd, comp_texts_root)

        # Typing '/sk' filters to /skills
        completions_sk = list(completer.get_completions(Document("/sk"), None))
        comp_texts_sk = [c.text for c in completions_sk]
        self.assertEqual(comp_texts_sk, ["/skills"])

        # Non-slash input produces no completions
        completions_plain = list(completer.get_completions(Document("hello"), None))
        self.assertEqual(len(completions_plain), 0)

if __name__ == "__main__":
    unittest.main()
