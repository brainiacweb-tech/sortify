"""Logging service to configure application file and stream logging."""
import sys
import logging
from pathlib import Path
from app.utils.constants import LOG_FILE, LOG_DIR

def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """Initialize logging configuration for Smart File Organizer with zero-crash guarantee."""
    logger = logging.getLogger("SmartFileOrganizer")
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers if re-initialized
    if logger.handlers:
        return logger

    # Console handler
    try:
        console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)
    except Exception:
        pass

    # File handler with safe fallbacks
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
    except Exception as e:
        try:
            sys.stderr.write(f"Warning: Could not initialize primary log file at {LOG_FILE}: {e}\n")
        except Exception:
            pass
        try:
            import tempfile
            fallback_log = Path(tempfile.gettempdir()) / "smart_file_organizer.log"
            file_formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler = logging.FileHandler(fallback_log, encoding="utf-8")
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(log_level)
            logger.addHandler(file_handler)
        except Exception:
            pass

    return logger

def get_logger() -> logging.Logger:
    """Get the application logger instance."""
    return logging.getLogger("SmartFileOrganizer")

