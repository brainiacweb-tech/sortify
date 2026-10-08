"""Application constants for Smart File Organizer."""
from pathlib import Path

APP_NAME = "SORTIFY"
DEVELOPER_NAME = "Francis Kusi"
APP_VERSION = "1.0.0"
REPO_NAME = "smart-file-organizer-python"
FONT_FAMILY = "Raleway"

# Default configuration directory in user profile
APP_DIR = Path.home() / ".smart_file_organizer"
CONFIG_FILE = APP_DIR / "config.json"
HISTORY_FILE = APP_DIR / "history.json"
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "smart_file_organizer.log"

# Default File Hashing Chunk Size (1 MB)
HASH_CHUNK_SIZE = 1048576

# Ignored files and folders
IGNORED_FILENAMES = {
    "desktop.ini",
    "thumbs.db",
    ".ds_store",
    "icon\r",
}

IGNORED_EXTENSIONS = {
    ".tmp",
    ".crdownload",
    ".part",
    ".bak",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".svn",
    ".hg",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
}

# Default Folder Names
DUPLICATES_FOLDER_NAME = "Duplicates"
OTHERS_FOLDER_NAME = "Others"

# UI Theme Options
THEME_LIGHT = "Light"
THEME_DARK = "Dark"
THEME_SYSTEM = "System"

# CustomTkinter Dual Theme Color Tuples (Light Mode Color, Dark Mode Color)
COLOR_BG_MAIN = ("#F8FAFC", "#10111A")
COLOR_SIDEBAR_BG = ("#FFFFFF", "#151624")
COLOR_CARD_BG = ("#FFFFFF", "#1D1E30")
COLOR_CARD_BORDER = ("#E2E8F0", "#2D2F48")
COLOR_CARD_HOVER = ("#F1F5F9", "#272942")

COLOR_PRIMARY = "#6366F1"        # Indigo
COLOR_PRIMARY_HOVER = "#4F46E5"
COLOR_SUCCESS = "#10B981"        # Emerald
COLOR_INFO = "#3B82F6"           # Sapphire Blue
COLOR_WARNING = "#F59E0B"        # Amber
COLOR_DANGER = "#EF4444"         # Crimson
COLOR_PURPLE = "#8B5CF6"         # Violet
COLOR_PINK = "#EC4899"           # Rose Pink

COLOR_TEXT_PRIMARY = ("#0F172A", "#FFFFFF")
COLOR_TEXT_SECONDARY = ("#475569", "#9CA3AF")
COLOR_TEXT_MUTED = ("#64748B", "#6B7280")
