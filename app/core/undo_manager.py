"""Undo Manager & Activity Journal System."""
import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.core.file_operations import OperationResult, safe_restore_file
from app.utils.constants import APP_DIR, HISTORY_FILE

logger = logging.getLogger("SmartFileOrganizer")

@dataclass
class MoveRecord:
    """Record of a single file move action."""
    source: str
    destination: str
    original_category: str
    timestamp: str
    status: str = "SUCCESS"
    was_renamed: bool = False
    restored: bool = False
    restored_destination: Optional[str] = None

@dataclass
class BatchRecord:
    """Record of a batch organization execution."""
    batch_id: str
    timestamp: str
    base_folder: str
    moves: List[MoveRecord]
    undone: bool = False

class UndoManager:
    """Manages activity history journal and provides safe undo restoration capabilities."""

    def __init__(self, history_file: Optional[Path] = None):
        self.history_file = history_file or HISTORY_FILE

    def _load_history(self) -> List[Dict[str, Any]]:
        """Load history batches from JSON file."""
        if not self.history_file.exists():
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load history from {self.history_file}: {e}")
            return []

    def _save_history(self, history: List[Dict[str, Any]]) -> None:
        """Save history batches to JSON file."""
        try:
            APP_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save history to {self.history_file}: {e}")

    def record_batch(
        self,
        batch_id: str,
        base_folder: Path | str,
        move_results: List[OperationResult],
        category_map: Optional[Dict[str, str]] = None
    ) -> BatchRecord:
        """
        Record a newly completed batch of file moves into the history journal.
        """
        category_map = category_map or {}
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        moves: List[MoveRecord] = []
        for result in move_results:
            if result.success:
                src_str = str(result.source_path)
                dest_str = str(result.destination_path)
                cat = category_map.get(src_str, "Uncategorized")
                rec = MoveRecord(
                    source=src_str,
                    destination=dest_str,
                    original_category=cat,
                    timestamp=now_str,
                    status="SUCCESS",
                    was_renamed=result.was_renamed
                )
                moves.append(rec)

        batch = BatchRecord(
            batch_id=batch_id,
            timestamp=now_str,
            base_folder=str(base_folder),
            moves=moves,
            undone=False
        )

        history = self._load_history()
        history.insert(0, asdict(batch))
        self._save_history(history)
        logger.info(f"Recorded batch {batch_id} with {len(moves)} successful moves.")
        return batch

    def get_history(self) -> List[BatchRecord]:
        """Get all recorded batches from newest to oldest."""
        raw_history = self._load_history()
        batches: List[BatchRecord] = []

        for b_data in raw_history:
            moves = [MoveRecord(**m) for m in b_data.get("moves", [])]
            batch = BatchRecord(
                batch_id=b_data.get("batch_id", ""),
                timestamp=b_data.get("timestamp", ""),
                base_folder=b_data.get("base_folder", ""),
                moves=moves,
                undone=b_data.get("undone", False)
            )
            batches.append(batch)

        return batches

    def get_latest_batch(self) -> Optional[BatchRecord]:
        """Get the most recent non-undone batch if available."""
        batches = self.get_history()
        for b in batches:
            if not b.undone and b.moves:
                return b
        return None

    def undo_batch(self, batch_id: str) -> tuple[bool, str, List[OperationResult]]:
        """
        Reverse all moves in a specified batch in reverse order.
        Returns (success: bool, summary_message: str, list_of_restore_results).
        """
        history = self._load_history()
        target_batch_idx = None

        for idx, b in enumerate(history):
            if b.get("batch_id") == batch_id:
                target_batch_idx = idx
                break

        if target_batch_idx is None:
            return False, f"Batch '{batch_id}' not found in activity history.", []

        b_data = history[target_batch_idx]
        if b_data.get("undone", False):
            return False, f"Batch '{batch_id}' has already been undone.", []

        moves = b_data.get("moves", [])
        if not moves:
            return False, f"Batch '{batch_id}' has no recorded file moves.", []

        results: List[OperationResult] = []
        restored_count = 0
        failed_count = 0

        # Restore files in REVERSE order of original move
        for m in reversed(moves):
            dest_path = Path(m["destination"])
            orig_src_path = Path(m["source"])

            if not dest_path.exists():
                res = OperationResult(
                    success=False,
                    source_path=dest_path,
                    destination_path=orig_src_path,
                    error_message=f"File missing at organized destination: {dest_path}"
                )
                results.append(res)
                failed_count += 1
                continue

            restore_res = safe_restore_file(dest_path, orig_src_path)
            results.append(restore_res)

            if restore_res.success:
                restored_count += 1
                m["restored"] = True
                m["restored_destination"] = str(restore_res.destination_path)
            else:
                failed_count += 1

        # Mark batch as undone if at least some files were restored
        if restored_count > 0:
            b_data["undone"] = True
            history[target_batch_idx] = b_data
            self._save_history(history)

        msg = f"Undo completed for batch {batch_id}: {restored_count} files restored"
        if failed_count > 0:
            msg += f", {failed_count} operations failed."
        else:
            msg += " successfully."

        logger.info(msg)
        return (restored_count > 0), msg, results
