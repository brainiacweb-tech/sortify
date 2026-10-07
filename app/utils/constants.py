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
