"""Path validation utilities to ensure filesystem safety."""
import os
import sys
from pathlib import Path

def validate_folder_path(folder_input: str | Path) -> tuple[bool, str, Path | None]:
    """
    Validate that the given folder path is safe, existing, readable, and not a system root.
    Returns (is_valid: bool, error_message: str, resolved_path: Path | None).
    """
    if not folder_input:
        return False, "Folder path cannot be empty.", None

    try:
        path = Path(folder_input).resolve()
    except Exception as e:
        return False, f"Invalid path syntax: {e}", None

    if not path.exists():
        return False, f"Path does not exist: '{path}'", None

    if not path.is_dir():
        return False, f"Path is not a directory: '{path}'", None

    # System Root Safeguards
    if path == path.anchor:
        return False, f"Refusing to organize root system drive: '{path}'", None

    # Prevent organizing Windows system folders directly
    if sys.platform == "win32":
        windir = os.environ.get("WINDIR", "C:\\Windows")
        sys_root = Path(windir).resolve()
        if path == sys_root or sys_root in path.parents:
            return False, f"Refusing to organize system directory: '{path}'", None

    # Test read access
    try:
        next(path.iterdir(), None)
    except PermissionError:
        return False, f"Permission denied accessing directory: '{path}'", None
    except Exception as e:
        return False, f"Error accessing directory: {e}", None

    return True, "", path
