"""
tests/test_file_tools.py
Verifies that read_file and write_file tools are properly sandboxed to the current working directory.
"""
import os
import shutil
import unittest
from tools.system_tools import read_file, write_file

class TestFileTools(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.getcwd(), ".test_sandbox_tmp")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_write_and_read_file(self):
        target_file = os.path.join(".test_sandbox_tmp", "hello.txt")
        write_res = write_file(target_file, "Hello from Broo CLI!")
        self.assertIn("Successfully wrote", write_res)
        self.assertTrue(os.path.exists(target_file))

        read_res = read_file(target_file)
        self.assertEqual(read_res, "Hello from Broo CLI!")

    def test_nested_directory_write(self):
        nested_file = os.path.join(".test_sandbox_tmp", "nested", "sub", "test.py")
        write_res = write_file(nested_file, "print('nested')")
        self.assertIn("Successfully wrote", write_res)
        self.assertEqual(read_file(nested_file), "print('nested')")

    def test_traversal_read_blocked(self):
        traversal_read = read_file("../../../../etc/passwd")
        self.assertTrue("Access denied" in traversal_read or "outside the working directory" in traversal_read)

    def test_traversal_write_blocked(self):
        traversal_write = write_file("/tmp/hack.txt", "evil")
        self.assertTrue("Access denied" in traversal_write or "outside the working directory" in traversal_write)
        self.assertFalse(os.path.exists("/tmp/hack.txt"))

    def test_nonexistent_file(self):
        res = read_file(".test_sandbox_tmp/does_not_exist.txt")
        self.assertIn("does not exist", res)

    def test_directory_as_file(self):
        res = read_file(".test_sandbox_tmp")
        self.assertIn("is a directory", res)

if __name__ == "__main__":
    unittest.main()
