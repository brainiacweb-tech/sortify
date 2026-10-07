"""Master file organization flow orchestrator."""
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional
from app.core.duplicate_detector import DuplicateDetector, DuplicateDetectionResult
from app.core.file_classifier import FileClassifier
from app.core.file_operations import OperationResult, safe_move_file
from app.core.undo_manager import UndoManager
from app.services.config_service import ConfigService
from app.utils.constants import DUPLICATES_FOLDER_NAME, IGNORED_DIRECTORIES, IGNORED_EXTENSIONS, IGNORED_FILENAMES, OTHERS_FOLDER_NAME
from app.utils.helpers import get_safe_filename, is_hidden_file
from app.utils.validators import validate_folder_path

logger = logging.getLogger("SmartFileOrganizer")

@dataclass
class DryRunItem:
    """Represents a planned file organization move in dry-run mode."""
    source_path: Path
    category: str
    destination_dir: Path
    target_path: Path
    safe_destination_path: Path
    file_size: int
    is_collision: bool = False
    is_duplicate: bool = False

@dataclass
class DryRunResult:
    """Aggregated dry-run calculation preview."""
    base_folder: Path
    items: List[DryRunItem] = field(default_factory=list)
    total_files: int = 0
    total_size_bytes: int = 0
    category_counts: Dict[str, int] = field(default_factory=dict)
    category_sizes: Dict[str, int] = field(default_factory=dict)
    duplicate_result: Optional[DuplicateDetectionResult] = None

@dataclass
class OrganizeExecutionResult:
    """Result summary of executed file organization batch."""
    batch_id: str
    base_folder: Path
    total_attempted: int = 0
    total_successful: int = 0
    total_failed: int = 0
    total_bytes_moved: int = 0
    results: List[OperationResult] = field(default_factory=list)
    undone: bool = False

class OrganizerEngine:
    """Orchestrates file scanning, dry-run previewing, organization execution, and duplicate quarantine."""

    def __init__(
        self,
        config_service: Optional[ConfigService] = None,
        file_classifier: Optional[FileClassifier] = None,
        undo_manager: Optional[UndoManager] = None,
        duplicate_detector: Optional[DuplicateDetector] = None
    ):
        self.config_service = config_service or ConfigService()
        self.file_classifier = file_classifier or FileClassifier(self.config_service)
        self.undo_manager = undo_manager or UndoManager()
        self.duplicate_detector = duplicate_detector or DuplicateDetector()

    def _get_active_category_folders(self) -> set[str]:
        """Get set of folder names corresponding to active categories."""
        categories = self.file_classifier.config_service.get_all_categories()
        active = {cat_data.get("folder", cat_name).lower() for cat_name, cat_data in categories.items()}
        active.add(DUPLICATES_FOLDER_NAME.lower())
        active.add(OTHERS_FOLDER_NAME.lower())
        return active

    def is_ignored_path(self, path: Path, base_folder: Path) -> bool:
        """
        Check if a file or folder should be ignored during scanning.
        Prevents recursive self-organization of category subfolders.
        """
        if is_hidden_file(path):
            return True

        if path.name in IGNORED_FILENAMES or path.suffix.lower() in IGNORED_EXTENSIONS:
            return True

        # Check path components relative to base_folder
        try:
            rel_parts = path.relative_to(base_folder).parts
        except ValueError:
            return True

        if not rel_parts:
            return False

        # Ignore system/hidden directories
        for part in rel_parts[:-1]:
            if part in IGNORED_DIRECTORIES or part.startswith("."):
                return True

        # Active category folder names (e.g. Images, PDFs, Duplicates, Others)
        categories = self.file_classifier.config_service.get_all_categories()
        active_cat_folders = {cat_data.get("folder", cat_name).lower() for cat_name, cat_data in categories.items()}
        active_cat_folders.add(DUPLICATES_FOLDER_NAME.lower())
        active_cat_folders.add(OTHERS_FOLDER_NAME.lower())

        # If the top-level relative subfolder is an existing category folder, ignore it
        first_dir = rel_parts[0].lower()
        if len(rel_parts) > 1 and first_dir in active_cat_folders:
            return True

        # If path is a file inside top-level category folder
        if len(rel_parts) == 2 and first_dir in active_cat_folders:
            return True

        return False

    def scan_and_preview(
        self,
        folder_input: str | Path,
        recursive: bool = False,
        check_duplicates: bool = True,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        cancel_checker: Optional[Callable[[], bool]] = None
    ) -> DryRunResult:
        """
        Scan directory and compute dry-run organization preview without writing to disk.
        """
        is_valid, err_msg, base_folder = validate_folder_path(folder_input)
        if not is_valid or base_folder is None:
            logger.error(f"Invalid scan folder: {err_msg}")
            raise ValueError(err_msg)

        if recursive:
            iterator = base_folder.rglob("*")
        else:
            iterator = base_folder.glob("*")

        candidate_files: List[Path] = []
        for item in iterator:
            if cancel_checker and cancel_checker():
                logger.info("Scan cancelled during file collection.")
                return DryRunResult(base_folder=base_folder)

            if item.is_file() and not self.is_ignored_path(item, base_folder):
                candidate_files.append(item)

        total_files = len(candidate_files)
        items: List[DryRunItem] = []
        category_counts: Dict[str, int] = {}
        category_sizes: Dict[str, int] = {}
        total_size = 0

        # Run optional duplicate detection
        dup_result: Optional[DuplicateDetectionResult] = None
        duplicate_paths: set[Path] = set()

        if check_duplicates and total_files > 0:
            if progress_callback:
                progress_callback(0, total_files, "Checking for duplicate files...")
            dup_result = self.duplicate_detector.find_duplicates(
                folder_path=base_folder,
                recursive=recursive,
                progress_callback=progress_callback,
                cancel_checker=cancel_checker
            )
            for group in dup_result.groups:
                for d_file in group.duplicate_files:
                    duplicate_paths.add(d_file.resolve())

        for idx, file_path in enumerate(candidate_files):
            if cancel_checker and cancel_checker():
                return DryRunResult(base_folder=base_folder)

            if progress_callback:
                progress_callback(idx + 1, total_files, f"Classifying file {idx + 1}/{total_files}: {file_path.name}")

            category = self.file_classifier.classify_file(file_path)
            if not category:
                continue

            rel_dest_dir = self.file_classifier.get_destination_folder(file_path, category)
            abs_dest_dir = base_folder / rel_dest_dir

            target_path = abs_dest_dir / file_path.name
            safe_dest_path = get_safe_filename(abs_dest_dir, file_path.name)
            is_collision = (safe_dest_path != target_path)

            try:
                f_size = file_path.stat().st_size
            except Exception:
                f_size = 0

            is_dup = (file_path.resolve() in duplicate_paths)

            item = DryRunItem(
                source_path=file_path,
                category=category,
                destination_dir=abs_dest_dir,
                target_path=target_path,
                safe_destination_path=safe_dest_path,
                file_size=f_size,
                is_collision=is_collision,
                is_duplicate=is_dup
            )

            items.append(item)
            category_counts[category] = category_counts.get(category, 0) + 1
            category_sizes[category] = category_sizes.get(category, 0) + f_size
            total_size += f_size

        return DryRunResult(
            base_folder=base_folder,
            items=items,
            total_files=len(items),
            total_size_bytes=total_size,
            category_counts=category_counts,
            category_sizes=category_sizes,
            duplicate_result=dup_result
        )

    def execute_organization(
        self,
        dry_run_result: DryRunResult,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
        cancel_checker: Optional[Callable[[], bool]] = None
    ) -> OrganizeExecutionResult:
        """
        Execute file moves based on calculated dry run result and record batch in UndoManager.
        """
        batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_folder = dry_run_result.base_folder

        total_items = len(dry_run_result.items)
        if total_items == 0:
            return OrganizeExecutionResult(batch_id=batch_id, base_folder=base_folder)

        results: List[OperationResult] = []
        category_map: Dict[str, str] = {}
        successful_count = 0
        failed_count = 0
        bytes_moved = 0

        for idx, item in enumerate(dry_run_result.items):
            if cancel_checker and cancel_checker():
                logger.info(f"Organization batch {batch_id} cancelled at item {idx}/{total_items}.")
                break

            if progress_callback:
                progress_callback(
                    idx + 1,
                    total_items,
                    f"Moving file {idx + 1}/{total_items}: {item.source_path.name} -> {item.category}"
                )

            res = safe_move_file(
                source=item.source_path,
                destination_dir=item.destination_dir,
                target_filename=item.source_path.name
            )

            results.append(res)
            category_map[str(res.source_path)] = item.category

            if res.success:
                successful_count += 1
                bytes_moved += item.file_size
            else:
                failed_count += 1

        # Record batch in UndoManager
        self.undo_manager.record_batch(
            batch_id=batch_id,
            base_folder=base_folder,
            move_results=results,
            category_map=category_map
        )

        return OrganizeExecutionResult(
            batch_id=batch_id,
            base_folder=base_folder,
            total_attempted=len(results),
            total_successful=successful_count,
            total_failed=failed_count,
            total_bytes_moved=bytes_moved,
            results=results
        )

    def quarantine_duplicates(
        self,
        base_folder: Path,
        duplicate_files: List[Path],
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> List[OperationResult]:
        """
        Move selected duplicate files into a 'Duplicates' quarantine folder safely.
        """
        dest_dir = base_folder / DUPLICATES_FOLDER_NAME
        results: List[OperationResult] = []
        total = len(duplicate_files)

        for idx, src_file in enumerate(duplicate_files):
            if progress_callback:
                progress_callback(
                    idx + 1,
                    total,
                    f"Quarantining duplicate {idx + 1}/{total}: {src_file.name}"
                )
            res = safe_move_file(src_file, dest_dir)
            results.append(res)

        return results
