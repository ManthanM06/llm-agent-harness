"""
Core system tools that the LLM can use to interact with the environment.
"""

import datetime
import os

def get_current_time(timezone_offset: float = 0.0) -> str:
    tz = datetime.timezone(datetime.timedelta(hours=timezone_offset))
    now = datetime.datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")

def list_files(directory_path:str = ".") -> str:
    try:
        if not os.path.exists(directory_path):
             return f"Error: The directory '{directory_path}' was not found."
        files = os.listdir(directory_path)
        # Check if list is completely empty
        if len(files) == 0:
            return f"The directory '{directory_path}' is completely empty."
        return ", ".join(files)
    except Exception as e:
        return f"Error reading directory: {str(e)}"