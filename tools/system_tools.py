"""
Core system tools that the LLM can use to interact with the environment.
"""

import datetime
import os

def get_current_time(timezone_offset: float = 0.0) -> str:
    """Get the current date and time formatted as a string for a given timezone offset.

    Args:
        timezone_offset: Timezone offset in hours relative to UTC (e.g., 5.5 for IST, -5.0 for EST). Defaults to 0.0.

    Returns:
        A string representation of the current date, time, and timezone.
    """
    try:
        offset_hours = float(timezone_offset) if timezone_offset is not None else 0.0
    except (ValueError, TypeError):
        offset_hours = 0.0
    tz = datetime.timezone(datetime.timedelta(hours=offset_hours))
    now = datetime.datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")

def list_files(directory_path: str = ".") -> str:
    """List all files and subdirectories in the specified directory path.

    Args:
        directory_path: The filesystem path to inspect. Defaults to '.' (the current working directory).

    Returns:
        A comma-separated list of filenames, or an error message if the directory is invalid.
    """
    if not directory_path or str(directory_path).strip() == "":
        directory_path = "."
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