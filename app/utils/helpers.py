"""Helper utilities for file size formatting, path collision resolution, and date formatting."""
import os
import sys
from datetime import datetime
from pathlib import Path

def format_file_size(size_in_bytes: int) -> str:
    """Format bytes into human-readable strings (B, KB, MB, GB, TB)."""
    if size_in_bytes < 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    size = float(size_in_bytes)
    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    if unit_index == 0:
        return f"{int(size)} B"
    return f"{size:.1f} {units[unit_index]}"

def format_timestamp(dt: datetime | None = None) -> str:
    """Format a datetime object into a standardized readable string."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def get_safe_filename(target_dir: Path, filename: str) -> Path:
    """
    Generate a non-colliding destination path in target_dir.
    If 'photo.jpg' exists, generates 'photo_1.jpg', 'photo_2.jpg', etc.
    """
    dest_path = target_dir / filename
    if not dest_path.exists():
        return dest_path
    
    stem = dest_path.stem
    suffix = dest_path.suffix
    counter = 1
    
    while True:
        candidate_name = f"{stem}_{counter}{suffix}"
        candidate_path = target_dir / candidate_name
        if not candidate_path.exists():
            return candidate_path
        counter += 1

def is_hidden_file(path: Path) -> bool:
    """Check if a file or directory is hidden across Windows and Unix platforms."""
    name = path.name
    if name.startswith(".") and name != ".":
        return True
    
    # Windows hidden attribute check
    if sys.platform == "win32":
        try:
            import stat
            attrs = os.stat(path).st_file_attributes
            return bool(attrs & stat.FILE_ATTRIBUTE_HIDDEN)
        except (AttributeError, OSError):
            pass
            
    return False
