"""
test_file_tools.py
Verifies that read_file and write_file tools are properly sandboxed to the current working directory.
"""
import os
import shutil
import tempfile
from tools.system_tools import read_file, write_file

def test_file_tools():
    print("=" * 60)
    print("TESTING FILE TOOLS & CWD SANDBOX")
    print("=" * 60)

    test_sandbox_dir = os.path.join(os.getcwd(), ".test_sandbox_tmp")
    if os.path.exists(test_sandbox_dir):
        shutil.rmtree(test_sandbox_dir)
    os.makedirs(test_sandbox_dir, exist_ok=True)

    try:
        # Test 1: Write file in CWD
        print("\n[*] Test 1: Write file inside working directory")
        target_file = os.path.join(".test_sandbox_tmp", "hello.txt")
        write_res = write_file(target_file, "Hello from Broo CLI!")
        print(f"Result: {write_res}")
        assert "Successfully wrote" in write_res, f"Expected success message, got {write_res}"
        assert os.path.exists(target_file), "File was not written to disk"

        # Test 2: Read file from CWD
        print("\n[*] Test 2: Read file inside working directory")
        read_res = read_file(target_file)
        print(f"Result: {read_res}")
        assert read_res == "Hello from Broo CLI!", f"Expected 'Hello from Broo CLI!', got {read_res}"

        # Test 3: Overwrite file in nested directory inside CWD
        print("\n[*] Test 3: Write to nested directory inside CWD")
        nested_file = os.path.join(".test_sandbox_tmp", "nested", "sub", "test.py")
        write_nested = write_file(nested_file, "print('nested')")
        print(f"Result: {write_nested}")
        assert "Successfully wrote" in write_nested
        assert read_file(nested_file) == "print('nested')"

        # Test 4: Path traversal attempt with ../ escaping CWD
        print("\n[*] Test 4: Traversal attempt escaping CWD (../../../../etc/passwd)")
        traversal_read = read_file("../../../../etc/passwd")
        print(f"Result: {traversal_read}")
        assert "Access denied" in traversal_read or "outside the working directory" in traversal_read

        # Test 5: Traversal write attempt escaping CWD
        print("\n[*] Test 5: Traversal write attempt escaping CWD (/tmp/hack.txt)")
        traversal_write = write_file("/tmp/hack.txt", "evil")
        print(f"Result: {traversal_write}")
        assert "Access denied" in traversal_write or "outside the working directory" in traversal_write
        assert not os.path.exists("/tmp/hack.txt")

        # Test 6: Non-existent file
        print("\n[*] Test 6: Read non-existent file inside CWD")
        non_existent = read_file(".test_sandbox_tmp/does_not_exist.txt")
        print(f"Result: {non_existent}")
        assert "does not exist" in non_existent

        # Test 7: Attempt to read directory as file
        print("\n[*] Test 7: Read directory as file")
        dir_read = read_file(".test_sandbox_tmp")
        print(f"Result: {dir_read}")
        assert "is a directory" in dir_read

        print("\n" + "=" * 60)
        print("ALL FILE TOOL & SANDBOX TESTS PASSED! [✓]")
        print("=" * 60)

    finally:
        if os.path.exists(test_sandbox_dir):
            shutil.rmtree(test_sandbox_dir)

if __name__ == "__main__":
    test_file_tools()
