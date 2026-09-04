"""
tests/test_permissions.py
Verifies the permission gating system for sensitive tools.
"""
import os
import unittest
from tools.registry import registry

class TestToolPermissions(unittest.TestCase):
    def setUp(self):
        self.test_file = ".test_perm_tmp.txt"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        registry.set_permission_handler(None)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_sensitive_tool_classification(self):
        self.assertTrue(registry.requires_permission("read_file"))
        self.assertTrue(registry.requires_permission("write_file"))
        self.assertFalse(registry.requires_permission("get_current_time"))
        self.assertFalse(registry.requires_permission("list_files"))

    def test_permission_denied_blocks_execution(self):
        calls = []
        def deny_handler(tool_name, args):
            calls.append((tool_name, args))
            return False

        registry.set_permission_handler(deny_handler)
        res = registry.execute("write_file", {"file_path": self.test_file, "content": "secret data"})
        self.assertIn("Execution cancelled", res)
        self.assertIn("User denied permission", res)
        self.assertFalse(os.path.exists(self.test_file))
        self.assertEqual(len(calls), 1)

    def test_permission_granted_executes_tool(self):
        calls = []
        def allow_handler(tool_name, args):
            calls.append((tool_name, args))
            return True

        registry.set_permission_handler(allow_handler)
        res_write = registry.execute("write_file", {"file_path": self.test_file, "content": "allowed data"})
        self.assertIn("Successfully wrote", res_write)
        self.assertTrue(os.path.exists(self.test_file))

        res_read = registry.execute("read_file", {"file_path": self.test_file})
        self.assertEqual(res_read, "allowed data")
        self.assertEqual(len(calls), 2)

    def test_safe_tools_bypass_permission_handler(self):
        calls = []
        def allow_handler(tool_name, args):
            calls.append((tool_name, args))
            return True

        registry.set_permission_handler(allow_handler)
        res_time = registry.execute("get_current_time", {"timezone_offset": 0})
        self.assertEqual(len(calls), 0)
        self.assertIn("UTC", res_time)

if __name__ == "__main__":
    unittest.main()
