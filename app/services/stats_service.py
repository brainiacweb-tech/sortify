"""Statistics service for computing storage analytics and activity metrics."""
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from app.core.undo_manager import UndoManager
from app.utils.helpers import format_file_size

logger = logging.getLogger("SmartFileOrganizer")

@dataclass
class DashboardStats:
    """Dashboard overall analytics metric summary."""
    total_runs: int = 0
    total_files_organized: int = 0
    total_bytes_organized: int = 0
    total_duplicates_found: int = 0
    total_wasted_bytes: int = 0
    category_breakdown: Dict[str, int] = field(default_factory=dict)

class StatsService:
    """Computes operational statistics and storage analytics for dashboard and reports."""

    def __init__(self, undo_manager: Optional[UndoManager] = None):
        self.undo_manager = undo_manager or UndoManager()

    def get_dashboard_stats(self) -> DashboardStats:
        """Compute aggregated statistics across all historical organization runs."""
        batches = self.undo_manager.get_history()
        
        total_runs = len(batches)
        files_count = 0
        cat_counts: Dict[str, int] = {}
        
        for batch in batches:
            if not batch.undone:
                for move in batch.moves:
                    if move.status == "SUCCESS" and not move.restored:
                        files_count += 1
                        cat = move.original_category or "Others"
                        cat_counts[cat] = cat_counts.get(cat, 0) + 1

        return DashboardStats(
            total_runs=total_runs,
            total_files_organized=files_count,
            category_breakdown=cat_counts
        )
