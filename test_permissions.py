"""
test_permissions.py
Verifies the permission gating system for sensitive tools.
"""
import os
import shutil
from tools.registry import registry

def test_permission_system():
    print("=" * 60)
    print("TESTING TOOL PERMISSION SYSTEM")
    print("=" * 60)

    test_file = ".test_perm_tmp.txt"
    if os.path.exists(test_file):
        os.remove(test_file)

    try:
        # Check tool sensitivity tags
        print("\n[*] Test 1: Checking sensitive tool classifications")
        assert registry.requires_permission("read_file") is True, "read_file must require permission"
        assert registry.requires_permission("write_file") is True, "write_file must require permission"
        assert registry.requires_permission("get_current_time") is False, "get_current_time should not require permission"
        assert registry.requires_permission("list_files") is False, "list_files should not require permission"
        print("[✓] Tool sensitivity tags verified.")

        # Test Permission Denied
        calls = []
        def deny_handler(tool_name, args):
            calls.append((tool_name, args))
            return False

        registry.set_permission_handler(deny_handler)

        print("\n[*] Test 2: Permission denied for write_file")
        res_denied = registry.execute("write_file", {"file_path": test_file, "content": "secret data"})
        print(f"Result: {res_denied}")
        assert "Execution cancelled" in res_denied and "User denied permission" in res_denied
        assert not os.path.exists(test_file), "File should NOT have been created when permission was denied"
        assert len(calls) == 1
        assert calls[0][0] == "write_file"
        print("[✓] Deny behavior verified.")

        # Test Permission Granted
        calls.clear()
        def allow_handler(tool_name, args):
            calls.append((tool_name, args))
            return True

        registry.set_permission_handler(allow_handler)

        print("\n[*] Test 3: Permission granted for write_file")
        res_allowed = registry.execute("write_file", {"file_path": test_file, "content": "allowed data"})
        print(f"Result: {res_allowed}")
        assert "Successfully wrote" in res_allowed
        assert os.path.exists(test_file), "File should have been written"
        assert len(calls) == 1

        print("\n[*] Test 4: Permission granted for read_file")
        res_read = registry.execute("read_file", {"file_path": test_file})
        print(f"Result: {res_read}")
        assert res_read == "allowed data"
        assert len(calls) == 2
        assert calls[1][0] == "read_file"
        print("[✓] Allow behavior verified.")

        # Test Safe Tool bypasses permission handler
        calls.clear()
        print("\n[*] Test 5: Safe tools do not trigger permission handler")
        res_time = registry.execute("get_current_time", {"timezone_offset": 0})
        print(f"Result: {res_time}")
        assert len(calls) == 0, "Permission handler should NOT be called for safe tools"
        print("[✓] Safe tool bypass verified.")

        # Reset handler
        registry.set_permission_handler(None)

        print("\n" + "=" * 60)
        print("ALL PERMISSION SYSTEM TESTS PASSED! [✓]")
        print("=" * 60)

    finally:
        registry.set_permission_handler(None)
        if os.path.exists(test_file):
            os.remove(test_file)

if __name__ == "__main__":
    test_permission_system()
