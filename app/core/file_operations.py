"""Safe file move, copy, and collision resolution operations."""
import os
import shutil
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from app.utils.helpers import get_safe_filename

logger = logging.getLogger("SmartFileOrganizer")

@dataclass
class OperationResult:
    """Result of a single file filesystem operation."""
    success: bool
    source_path: Path
    destination_path: Path
    error_message: Optional[str] = None
    was_renamed: bool = False

def safe_move_file(source: Path, destination_dir: Path, target_filename: Optional[str] = None) -> OperationResult:
    """
    Safely move a file to target directory, handling collisions and directory creation.
    
    Args:
        source: Path to source file
        destination_dir: Directory where file will be moved
        target_filename: Optional custom filename; defaults to source.name
        
    Returns:
        OperationResult dataclass detailing status and paths.
    """
    if not source.exists():
        return OperationResult(
            success=False,
            source_path=source,
            destination_path=destination_dir / (target_filename or source.name),
            error_message=f"Source file does not exist: {source}"
        )
    
    if not source.is_file():
        return OperationResult(
            success=False,
            source_path=source,
            destination_path=destination_dir / (target_filename or source.name),
            error_message=f"Source path is not a regular file: {source}"
        )

    try:
        # Ensure destination directory exists
        destination_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create directory {destination_dir}: {e}")
        return OperationResult(
            success=False,
            source_path=source,
            destination_path=destination_dir / (target_filename or source.name),
            error_message=f"Could not create destination directory: {e}"
        )

    filename = target_filename or source.name
    target_path = destination_dir / filename

    # Calculate collision-free safe filename
    final_dest_path = get_safe_filename(destination_dir, filename)
    was_renamed = (final_dest_path != target_path)

    # Check if source and final destination are identical
    if source.resolve() == final_dest_path.resolve():
        return OperationResult(
            success=True,
            source_path=source,
            destination_path=final_dest_path,
            was_renamed=False
        )

    try:
        shutil.move(str(source), str(final_dest_path))
        logger.info(f"Successfully moved {source} -> {final_dest_path}")
        return OperationResult(
            success=True,
            source_path=source,
            destination_path=final_dest_path,
            was_renamed=was_renamed
        )
    except Exception as e:
        logger.error(f"Error moving file {source} -> {final_dest_path}: {e}")
        return OperationResult(
            success=False,
            source_path=source,
            destination_path=final_dest_path,
            error_message=str(e),
            was_renamed=was_renamed
        )

def safe_restore_file(current_path: Path, original_path: Path) -> OperationResult:
    """
    Safely restore a previously moved file back to its original location.
    Handles case where original path directory or filename location has a new collision.
    """
    if not current_path.exists():
        return OperationResult(
            success=False,
            source_path=current_path,
            destination_path=original_path,
            error_message=f"File to restore does not exist at current path: {current_path}"
        )

    target_dir = original_path.parent
    target_filename = original_path.name
    
    return safe_move_file(current_path, target_dir, target_filename)
