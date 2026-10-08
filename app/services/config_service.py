"""Configuration service for managing persistent user settings and rules."""
import json
import logging
from pathlib import Path
from typing import Any, Dict
from app.utils.constants import APP_DIR, CONFIG_FILE

logger = logging.getLogger("SmartFileOrganizer")

DEFAULT_SETTINGS: Dict[str, Any] = {
    "organize_unknown_files": True,
    "create_others_folder": True,
    "move_duplicates_automatically": False,
    "include_subfolders": False,
    "confirm_before_organizing": True,
    "remember_last_folder": True,
    "last_selected_folder": "",
    "theme": "Dark",
    "date_based_organization": False,
    "custom_categories": {}
}

class ConfigService:
    """Manages application settings and extension classification rules."""

    def __init__(self, config_file: Path | None = None):
        self.config_file = config_file or CONFIG_FILE
        self.default_rules_file = Path(__file__).parent.parent / "config" / "default_rules.json"
        self._settings: Dict[str, Any] = {}
        self._rules: Dict[str, Any] = {}
        self.load()

    def _load_default_rules(self) -> Dict[str, Any]:
        """Load default categories and extension mappings from default_rules.json."""
        if self.default_rules_file.exists():
            try:
                with open(self.default_rules_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load default_rules.json: {e}")
        return {
            "categories": {},
            "default_folder_for_unknown": "Others"
        }

    def load(self) -> None:
        """Load settings from config.json or initialize defaults."""
        self._rules = self._load_default_rules()
        self._settings = DEFAULT_SETTINGS.copy()

        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    self._settings.update(saved_data)
            except Exception as e:
                logger.warning(f"Could not read config file {self.config_file}, using defaults: {e}")
        else:
            self.save()

    def save(self) -> None:
        """Save current settings to config.json."""
        try:
            APP_DIR.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save settings to {self.config_file}: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a setting value and persist to file."""
        self._settings[key] = value
        self.save()

    def get_all_categories(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all active category rules (default rules + user custom rules).
        Returns a dict mapping category_name -> {"folder": str, "extensions": list[str]}.
        """
        categories = {}
        # Default categories
        raw_defaults = self._rules.get("categories", {})
        for name, data in raw_defaults.items():
            categories[name] = {
                "folder": data.get("folder", name),
                "extensions": list(data.get("extensions", []))
            }

        # Override or add custom categories
        custom_cats = self._settings.get("custom_categories", {})
        for name, data in custom_cats.items():
            if name in categories:
                # Merge extensions or replace
                exts = list(set(categories[name]["extensions"] + data.get("extensions", [])))
                categories[name]["extensions"] = exts
            else:
                categories[name] = {
                    "folder": data.get("folder", name),
                    "extensions": list(data.get("extensions", []))
                }
        return categories

    def add_custom_rule(self, category_name: str, extensions: list[str], folder_name: str | None = None) -> None:
        """Add or update a custom rule."""
        folder = folder_name or category_name
        # Normalize extensions
        clean_exts = []
        for ext in extensions:
            ext = ext.strip().lower()
            if ext and not ext.startswith("."):
                ext = f".{ext}"
            if ext:
                clean_exts.append(ext)

        customs = self._settings.get("custom_categories", {})
        customs[category_name] = {
            "folder": folder,
            "extensions": clean_exts
        }
        self._settings["custom_categories"] = customs
        self.save()

    def reset_rules_to_defaults(self) -> None:
        """Reset custom rules back to system defaults."""
        self._settings["custom_categories"] = {}
        self.save()

    def reset_all(self) -> None:
        """Reset all settings to default factory values."""
        self._settings = DEFAULT_SETTINGS.copy()
        self.save()
