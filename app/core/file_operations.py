"""Safe file move, copy, deletion, compression, and collision resolution operations."""
import os
import shutil
import logging
import zipfile
import ctypes
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
from app.utils.helpers import get_safe_filename

logger = logging.getLogger("SmartFileOrganizer")

PROTECTED_DIRS = [
    r"C:\Windows",
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    r"C:\ProgramData",
    r"C:\System Volume Information",
    r"C:\Recovery",
    r"C:\\"
]

@dataclass
class OperationResult:
    """Result of a single file filesystem operation."""
    success: bool
    source_path: Path
    destination_path: Path
    error_message: Optional[str] = None
    was_renamed: bool = False

def is_protected_path(path_str: str) -> bool:
    """Check if target path is a system-critical location that should not be mass reorganized."""
    if not path_str:
        return True
    try:
        resolved = str(Path(path_str).resolve()).lower()
        if len(resolved) <= 3 and resolved.endswith(":\\"):
            return True
        for prot in PROTECTED_DIRS:
            prot_res = str(Path(prot).resolve()).lower()
            if resolved == prot_res or resolved.startswith(prot_res + "\\"):
                return True
        return False
    except Exception:
        return True

class SHFILEOPSTRUCTW(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("wFunc", wintypes.UINT),
        ("pFrom", wintypes.LPCWSTR),
        ("pTo", wintypes.LPCWSTR),
        ("fFlags", wintypes.WORD),
        ("fAnyOperationsAborted", wintypes.BOOL),
        ("hNameMappings", wintypes.LPVOID),
        ("lpszProgressTitle", wintypes.LPCWSTR)
    ]

FO_DELETE = 3
FOF_ALLOWUNDO = 0x0040
FOF_NOCONFIRMATION = 0x0010

def send_to_recycle_bin(path_str: str) -> bool:
    """Send file or folder to Windows Recycle Bin natively (non-destructive delete)."""
    try:
        p = str(Path(path_str).resolve())
        if not os.path.exists(p):
            return False
        op = SHFILEOPSTRUCTW()
        op.wFunc = FO_DELETE
        op.pFrom = p + '\0\0'
        op.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION
        res = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op))
        return res == 0
    except Exception as e:
        logger.error(f"Failed to move {path_str} to Recycle Bin: {e}")
        return False

def toggle_hide_attribute(path_str: str, hide: bool = True) -> bool:
    """Set or remove Windows hidden file attribute (attrib +h / -h)."""
    FILE_ATTRIBUTE_HIDDEN = 0x2
    FILE_ATTRIBUTE_NORMAL = 0x80
    try:
        p = str(Path(path_str).resolve())
        attrs = ctypes.windll.kernel32.GetFileAttributesW(p)
        if attrs == -1:
            return False
        if hide:
            new_attrs = attrs | FILE_ATTRIBUTE_HIDDEN
        else:
            new_attrs = attrs & ~FILE_ATTRIBUTE_HIDDEN
            if new_attrs == 0:
                new_attrs = FILE_ATTRIBUTE_NORMAL
        return ctypes.windll.kernel32.SetFileAttributesW(p, new_attrs) != 0
    except Exception as e:
        logger.error(f"Failed to toggle hide attribute for {path_str}: {e}")
        return False

def is_hidden_path(path_str: str) -> bool:
    """Check if file or folder has Windows hidden attribute."""
    FILE_ATTRIBUTE_HIDDEN = 0x2
    try:
        p = str(Path(path_str).resolve())
        attrs = ctypes.windll.kernel32.GetFileAttributesW(p)
        if attrs == -1:
            return False
        return bool(attrs & FILE_ATTRIBUTE_HIDDEN)
    except Exception:
        return False

def compress_to_zip(source_paths: List[str], output_zip_path: str, password: Optional[str] = None) -> bool:
    """Compress selected files/folders into a ZIP archive, optionally with password protection."""
    try:
        out_path = Path(output_zip_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            import pyzipper
            has_pyzipper = True
        except ImportError:
            has_pyzipper = False

        if password and has_pyzipper:
            with pyzipper.AESZipFile(str(out_path), 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES_ACTUAL) as zf:
                zf.setpassword(password.encode('utf-8'))
                for sp in source_paths:
                    p = Path(sp)
                    if p.is_file():
                        zf.write(str(p), arcname=p.name)
                    elif p.is_dir():
                        for root, _, files in os.walk(str(p)):
                            for f in files:
                                fp = Path(root) / f
                                rel = fp.relative_to(p.parent)
                                zf.write(str(fp), arcname=str(rel))
        else:
            with zipfile.ZipFile(str(out_path), 'w', zipfile.ZIP_DEFLATED) as zf:
                if password:
                    zf.setpassword(password.encode('utf-8'))
                for sp in source_paths:
                    p = Path(sp)
                    if p.is_file():
                        zf.write(str(p), arcname=p.name)
                    elif p.is_dir():
                        for root, _, files in os.walk(str(p)):
                            for f in files:
                                fp = Path(root) / f
                                rel = fp.relative_to(p.parent)
                                zf.write(str(fp), arcname=str(rel))
        return True
    except Exception as e:
        logger.error(f"Failed to create zip {output_zip_path}: {e}")
        return False

def extract_zip_archive(zip_file_path: str, extract_to_dir: str, password: Optional[str] = None) -> bool:
    """Extract ZIP archive into target directory."""
    try:
        zpath = Path(zip_file_path)
        dest_path = Path(extract_to_dir)
        dest_path.mkdir(parents=True, exist_ok=True)

        try:
            import pyzipper
            has_pyzipper = True
        except ImportError:
            has_pyzipper = False

        if has_pyzipper:
            with pyzipper.AESZipFile(str(zpath), 'r') as zf:
                pwd_bytes = password.encode('utf-8') if password else None
                zf.extractall(path=str(dest_path), pwd=pwd_bytes)
        else:
            with zipfile.ZipFile(str(zpath), 'r') as zf:
                pwd_bytes = password.encode('utf-8') if password else None
                zf.extractall(path=str(dest_path), pwd=pwd_bytes)
        return True
    except Exception as e:
        logger.error(f"Failed to extract zip {zip_file_path}: {e}")
        return False

def safe_move_file(source: Path, destination_dir: Path, target_filename: Optional[str] = None) -> OperationResult:
    """Safely move a file to target directory, handling collisions and directory creation."""
    if not source.exists():
        return OperationResult(
            success=False,
            source_path=source,
            destination_path=destination_dir / (target_filename or source.name),
            error_message=f"Source file does not exist: {source}"
        )

    try:
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
    final_dest_path = get_safe_filename(destination_dir, filename)
    was_renamed = (final_dest_path != target_path)

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

def safe_copy_file(source: Path, destination_dir: Path, target_filename: Optional[str] = None) -> OperationResult:
    """Safely copy a file to target directory, handling collisions."""
    if not source.exists():
        return OperationResult(
            success=False,
            source_path=source,
            destination_path=destination_dir / (target_filename or source.name),
            error_message=f"Source file does not exist: {source}"
        )

    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return OperationResult(
            success=False,
            source_path=source,
            destination_path=destination_dir / (target_filename or source.name),
            error_message=str(e)
        )

    filename = target_filename or source.name
    target_path = destination_dir / filename
    final_dest_path = get_safe_filename(destination_dir, filename)
    was_renamed = (final_dest_path != target_path)

    try:
        if source.is_dir():
            shutil.copytree(str(source), str(final_dest_path))
        else:
            shutil.copy2(str(source), str(final_dest_path))
        return OperationResult(
            success=True,
            source_path=source,
            destination_path=final_dest_path,
            was_renamed=was_renamed
        )
    except Exception as e:
        return OperationResult(
            success=False,
            source_path=source,
            destination_path=final_dest_path,
            error_message=str(e)
        )

def safe_restore_file(current_path: Path, original_path: Path) -> OperationResult:
    """Safely restore a previously moved file back to its original location."""
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
