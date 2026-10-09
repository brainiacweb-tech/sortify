import os
import tempfile
from pathlib import Path

def get_user_app_dir() -> Path:
    """
    Get a safe, writeable application directory for storing logs, config, and history.
    Prioritizes %LOCALAPPDATA%, %APPDATA%, %USERPROFILE%, and temp directory fallback.
    Guarantees write access and prevents ever targeting system32 or read-only directories.
    """
    candidates = []

    # 1. Standard Windows LocalAppData (%LOCALAPPDATA%\Sortify)
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data and "system32" not in local_app_data.lower():
        candidates.append(Path(local_app_data) / "Sortify")

    # 2. Standard Windows AppData (%APPDATA%\Sortify)
    app_data = os.environ.get("APPDATA")
    if app_data and "system32" not in app_data.lower():
        candidates.append(Path(app_data) / "Sortify")

    # 3. User Profile / Home directory (%USERPROFILE%\.smart_file_organizer)
    user_profile = os.environ.get("USERPROFILE")
    if user_profile and "system32" not in user_profile.lower():
        candidates.append(Path(user_profile) / ".smart_file_organizer")

    try:
        home = Path.home()
        if "system32" not in str(home).lower():
            candidates.append(home / ".smart_file_organizer")
    except Exception:
        pass

    # 4. Fallback to System Temp folder (%TEMP%\Sortify)
    candidates.append(Path(tempfile.gettempdir()) / "Sortify")

    for target in candidates:
        try:
            target.mkdir(parents=True, exist_ok=True)
            # Test write permission by creating a temporary file
            test_file = target / ".write_test"
            test_file.write_text("ok", encoding="utf-8")
            if test_file.exists():
                test_file.unlink()
            return target
        except Exception:
            continue

    # Absolute fallback
    fallback = Path(tempfile.gettempdir()) / "Sortify"
    try:
        fallback.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return fallback

# Default configuration directory in user profile
APP_DIR = get_user_app_dir()
CONFIG_FILE = APP_DIR / "config.json"
HISTORY_FILE = APP_DIR / "history.json"
LOG_DIR = APP_DIR / "logs"
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
