"""Two-stage SHA-256 duplicate file detection engine."""
import hashlib
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional
from app.utils.constants import HASH_CHUNK_SIZE, IGNORED_DIRECTORIES, IGNORED_EXTENSIONS, IGNORED_FILENAMES
from app.utils.helpers import is_hidden_file

logger = logging.getLogger("SmartFileOrganizer")

@dataclass
class DuplicateGroup:
    """Represents a group of duplicate files sharing the same content hash."""
    sha256_hash: str
    file_size: int
    files: List[Path]
    original_file: Path
    duplicate_files: List[Path] = field(default_factory=list)

    @property
    def wasted_bytes(self) -> int:
        """Total space wasted by duplicate copies (excluding 1 original)."""
        return self.file_size * len(self.duplicate_files)

@dataclass
class DuplicateDetectionResult:
    """Aggregated result of duplicate detection scan."""
    groups: List[DuplicateGroup] = field(default_factory=list)
    total_files_scanned: int = 0
    duplicate_files_count: int = 0
    total_wasted_bytes: int = 0

class DuplicateDetector:
    """Optimized two-stage SHA-256 duplicate detection engine."""

    def __init__(self, chunk_size: int = HASH_CHUNK_SIZE):
        self.chunk_size = chunk_size

    def calculate_file_hash(
        self,
        file_path: Path,
        cancel_checker: Optional[Callable[[], bool]] = None
    ) -> Optional[str]:
        """Compute SHA-256 hash of a file reading in 1 MB chunks."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(self.chunk_size):
                    if cancel_checker and cancel_checker():
                        return None
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (PermissionError, OSError, IOError) as e:
            logger.warning(f"Could not read file for hashing {file_path}: {e}")
            return None

    def _should_ignore(self, path: Path, base_dir: Path) -> bool:
        """Determine if path should be skipped during duplicate scanning."""
        if is_hidden_file(path):
            return True
        if path.name in IGNORED_FILENAMES or path.suffix.lower() in IGNORED_EXTENSIONS:
            return True
        for part in path.relative_to(base_dir).parts[:-1]:
            if part in IGNORED_DIRECTORIES or part.startswith("."):
                return True
        return False

    def find_duplicates(
        self,
        folder_path: Path,
        recursive: bool = False,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        cancel_checker: Optional[Callable[[], bool]] = None
    ) -> DuplicateDetectionResult:
        """
        Scan directory and find exact duplicate files via file-size grouping followed by SHA-256 hashing.
        
        Args:
            folder_path: Target root directory
            recursive: Whether to inspect subdirectories
            progress_callback: Optional callback receiving (current_index, total_count, status_message)
            cancel_checker: Optional callable returning True if scan should abort
            
        Returns:
            DuplicateDetectionResult dataclass
        """
        folder_path = folder_path.resolve()
        candidate_files: List[Path] = []

        # Step 0: Gather candidate files
        if recursive:
            iterator = folder_path.rglob("*")
        else:
            iterator = folder_path.glob("*")

        for item in iterator:
            if cancel_checker and cancel_checker():
                logger.info("Duplicate scan cancelled during file gathering.")
                return DuplicateDetectionResult()
            
            if item.is_file() and not self._should_ignore(item, folder_path):
                candidate_files.append(item)

        total_files = len(candidate_files)
        if total_files == 0:
            return DuplicateDetectionResult()

        # Step 1: Quick grouping by exact file size
        size_groups: Dict[int, List[Path]] = {}
        for idx, file_path in enumerate(candidate_files):
            if cancel_checker and cancel_checker():
                return DuplicateDetectionResult()
                
            try:
                size = file_path.stat().st_size
                size_groups.setdefault(size, []).append(file_path)
            except (OSError, PermissionError):
                continue

        # Filter size groups to only those with >= 2 candidate files
        candidate_size_groups = {s: files for s, files in size_groups.items() if len(files) >= 2}

        # Calculate total candidate files needing hash computation
        files_to_hash = [f for files in candidate_size_groups.values() for f in files]
        total_to_hash = len(files_to_hash)

        if total_to_hash == 0:
            return DuplicateDetectionResult(total_files_scanned=total_files)

        # Step 2: Calculate SHA-256 chunk hashes for candidate groups
        hash_groups: Dict[tuple[int, str], List[Path]] = {}
        hashed_count = 0

        for size, file_list in candidate_size_groups.items():
            for file_path in file_list:
                if cancel_checker and cancel_checker():
                    logger.info("Duplicate scan cancelled during hashing stage.")
                    return DuplicateDetectionResult(total_files_scanned=total_files)

                hashed_count += 1
                if progress_callback:
                    progress_callback(
                        hashed_count,
                        total_to_hash,
                        f"Hashing file {hashed_count}/{total_to_hash}: {file_path.name}"
                    )

                file_hash = self.calculate_file_hash(file_path, cancel_checker)
                if file_hash:
                    hash_groups.setdefault((size, file_hash), []).append(file_path)

        # Step 3: Assemble duplicate groups
        result_groups: List[DuplicateGroup] = []
        total_duplicate_files = 0
        total_wasted = 0

        for (size, file_hash), matched_files in hash_groups.items():
            if len(matched_files) >= 2:
                # Sort files by creation / modification time or path length to designate original
                sorted_files = sorted(
                    matched_files,
                    key=lambda p: (p.stat().st_mtime if p.exists() else 0, len(str(p)))
                )
                original = sorted_files[0]
                duplicates = sorted_files[1:]

                group = DuplicateGroup(
                    sha256_hash=file_hash,
                    file_size=size,
                    files=sorted_files,
                    original_file=original,
                    duplicate_files=duplicates
                )
                result_groups.append(group)
                total_duplicate_files += len(duplicates)
                total_wasted += group.wasted_bytes

        return DuplicateDetectionResult(
            groups=result_groups,
            total_files_scanned=total_files,
            duplicate_files_count=total_duplicate_files,
            total_wasted_bytes=total_wasted
        )
