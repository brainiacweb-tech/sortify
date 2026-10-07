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
        protected_env_vars = ["WINDIR", "ProgramFiles", "ProgramFiles(x86)", "SystemRoot"]
        for var in protected_env_vars:
            val = os.environ.get(var)
            if val:
                sys_path = Path(val).resolve()
                if path == sys_path or sys_path in path.parents:
                    return False, f"Refusing to organize protected system directory: '{path}'", None

    # Test read access
    try:
        next(path.iterdir(), None)
    except PermissionError:
        return False, f"Permission denied accessing directory: '{path}'", None
    except Exception as e:
        return False, f"Error accessing directory: {e}", None

    return True, "", path
