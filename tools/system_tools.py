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

def _resolve_sandbox_path(path: str) -> str:
    """
    Resolves the absolute path and verifies it is strictly inside the current working directory.
    Raises PermissionError if the path attempts to escape the working directory.
    """
    if not path or not str(path).strip():
        raise ValueError("No file path provided.")

    cwd = os.path.realpath(os.getcwd())
    abs_path = os.path.abspath(path)
    real_path = os.path.realpath(abs_path)

    if real_path != cwd and not real_path.startswith(cwd + os.sep):
        raise PermissionError(f"Access denied: Path '{path}' is outside the working directory.")
    return real_path

def read_file(file_path: str) -> str:
    """Read the contents of a file located within the current working directory.

    Args:
        file_path: The relative or absolute path of the file to read (must be inside the working directory).

    Returns:
        The text content of the file, or an error message.
    """
    try:
        resolved = _resolve_sandbox_path(file_path)
    except (PermissionError, ValueError) as err:
        return f"Error: {str(err)}"

    if not os.path.exists(resolved):
        return f"Error: File '{file_path}' does not exist."

    if os.path.isdir(resolved):
        return f"Error: '{file_path}' is a directory, not a file."

    try:
        max_chars = 50000
        with open(resolved, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(max_chars + 1)

        if len(content) > max_chars:
            return content[:max_chars] + f"\n\n... [Truncated: Showing first {max_chars} characters of {file_path}]"
        return content
    except Exception as e:
        return f"Error reading file '{file_path}': {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """Write text content to a file located within the current working directory.

    Args:
        file_path: The path of the file to create or overwrite (must be inside the working directory).
        content: The text content to write to the file.

    Returns:
        A confirmation message indicating success or an error message.
    """
    try:
        resolved = _resolve_sandbox_path(file_path)
    except (PermissionError, ValueError) as err:
        return f"Error: {str(err)}"

    try:
        parent_dir = os.path.dirname(resolved)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(resolved, "w", encoding="utf-8") as f:
            f.write(content)

        return f"Successfully wrote {len(content)} characters to '{file_path}'."
    except Exception as e:
        return f"Error writing to file '{file_path}': {str(e)}"