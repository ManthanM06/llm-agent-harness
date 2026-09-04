"""
test_cli.py
Verifies the Broo CLI helpers, rendering functions, command handling, and permission prompts.
"""
from unittest.mock import patch
from interfaces.cli import (
    render_banner,
    show_help,
    show_skills,
    show_tools,
    cli_permission_handler,
    BrooCLI
)

def test_cli():
    print("=" * 60)
    print("TESTING BROO CLI COMPONENTS")
    print("=" * 60)

    # Test 1: Rendering functions run without error
    print("\n[*] Test 1: Testing banner, help, skills, and tools rendering")
    render_banner()
    show_help()
    show_skills()
    show_tools()
    print("[✓] Rendering components executed successfully.")

    # Test 2: BrooCLI command handler
    print("\n[*] Test 2: Testing CLI command dispatcher")
    cli = BrooCLI()
    assert cli.handle_command("/help") is True
    assert cli.handle_command("/skills") is True
    assert cli.handle_command("/tools") is True
    assert cli.handle_command("/clear") is True
    assert cli.handle_command("Hello world") is False
    assert cli.handle_command("/debug test code") is False
    print("[✓] Command dispatcher correctly identified commands and passthroughs.")

    # Test 3: Interactive permission prompt - Grant
    print("\n[*] Test 3: Testing cli_permission_handler with granted input")
    with patch("rich.prompt.Confirm.ask", return_value=True):
        granted = cli_permission_handler("write_file", {"file_path": "demo.py", "content": "print(1)"})
        assert granted is True
    print("[✓] Permission prompt granted verified.")

    # Test 4: Interactive permission prompt - Deny
    print("\n[*] Test 4: Testing cli_permission_handler with denied input")
    with patch("rich.prompt.Confirm.ask", return_value=False):
        denied = cli_permission_handler("write_file", {"file_path": "demo.py", "content": "print(1)"})
        assert denied is False
    print("[✓] Permission prompt denied verified.")

    # Test 5: Slash command completer
    print("\n[*] Test 5: Testing BrooSlashCompleter suggestions when typing '/'")
    from prompt_toolkit.document import Document
    from interfaces.cli import BrooSlashCompleter

    completer = BrooSlashCompleter()
    
    # Test typing '/' returns all slash commands and skills
    completions_root = list(completer.get_completions(Document("/"), None))
    comp_texts_root = [c.text for c in completions_root]
    print(f"Suggestions for '/': {comp_texts_root}")
    assert "/help" in comp_texts_root
    assert "/skills" in comp_texts_root
    assert "/tools" in comp_texts_root
    assert "/clear" in comp_texts_root
    assert "/debug" in comp_texts_root
    assert "/refactor" in comp_texts_root

    # Test typing '/sk' filters to /skills
    completions_sk = list(completer.get_completions(Document("/sk"), None))
    comp_texts_sk = [c.text for c in completions_sk]
    print(f"Suggestions for '/sk': {comp_texts_sk}")
    assert comp_texts_sk == ["/skills"]

    # Test non-slash input does not trigger completions
    completions_plain = list(completer.get_completions(Document("hello"), None))
    assert len(completions_plain) == 0
    print("[✓] BrooSlashCompleter suggestions and filtering verified.")

    print("\n" + "=" * 60)
    print("ALL CLI TESTS PASSED! [✓]")
    print("=" * 60)

if __name__ == "__main__":
    test_cli()
