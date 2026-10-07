"""File classification engine based on configuration rules."""
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from app.services.config_service import ConfigService
from app.utils.constants import OTHERS_FOLDER_NAME

class FileClassifier:
    """Classifies files into destination category folders according to file extension rules."""

    def __init__(self, config_service: Optional[ConfigService] = None):
        self.config_service = config_service or ConfigService()

    def classify_file(self, file_input: str | Path) -> str | None:
        """
        Classify a file by extension into a category name.
        Returns category name string (e.g. 'Images', 'PDFs') or None if unclassified.
        """
        path = Path(file_input)
        extension = path.suffix.lower()

        if not extension:
            # Files without extensions
            if self.config_service.get("organize_unknown_files", True):
                return OTHERS_FOLDER_NAME
            return None

        categories = self.config_service.get_all_categories()

        for cat_name, cat_data in categories.items():
            exts = [e.lower() for e in cat_data.get("extensions", [])]
            if extension in exts:
                return cat_name

        # Unknown extension
        if self.config_service.get("organize_unknown_files", True):
            return OTHERS_FOLDER_NAME

        return None

    def get_destination_folder(self, file_path: Path, category_name: str) -> Path:
        """
        Determine the destination subfolder relative to target base folder.
        If date-based organization is enabled, appends Year/Month subdirectories.
        Example: Images/2026/October or PDFs/
        """
        categories = self.config_service.get_all_categories()
        cat_info = categories.get(category_name, {})
        folder_name = cat_info.get("folder", category_name)

        dest = Path(folder_name)

        if self.config_service.get("date_based_organization", False):
            try:
                mtime = file_path.stat().st_mtime
                file_dt = datetime.fromtimestamp(mtime)
                year_str = file_dt.strftime("%Y")
                month_str = file_dt.strftime("%B")
                dest = dest / year_str / month_str
            except Exception:
                pass

        return dest
