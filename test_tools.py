"""
Verifies that the Tool Registry works and can execute functions.
"""
from tools.registry import registry

def test_registry():
    print("[*] Testing Tool Registry...")
    
    # Test getting all tools
    all_tools = registry.get_all_tools()
    print(f"[+] Registered tools: {[t.__name__ for t in all_tools]}")
    
    # Test execution: time
    print("\n[*] Testing get_current_time (Offset: 5.5 for IST)...")
    time_result = registry.execute("get_current_time", {"timezone_offset": 5.5})
    print(f"[+] Result: {time_result}")
    
    # Test execution: list files
    print("\n[*] Testing list_files (Path: '.')...")
    file_result = registry.execute("list_files", {"directory_path": "."})
    print(f"[+] Result: {file_result}")
    
    # Test error handling (missing tool)
    print("\n[*] Testing missing tool...")
    error_result = registry.execute("fake_tool", {})
    print(f"[+] Result: {error_result}")

if __name__ == "__main__":
    test_registry()