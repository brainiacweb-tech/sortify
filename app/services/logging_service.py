"""Logging service to configure application file and stream logging."""
import logging
from pathlib import Path
from app.utils.constants import LOG_FILE, LOG_DIR

def setup_logging(log_level: int = logging.INFO) -> logging.Logger:
    """Initialize logging configuration for Smart File Organizer."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger("SmartFileOrganizer")
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers if re-initialized
    if logger.handlers:
        return logger

    # File handler
    file_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    # Console handler
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)

    return logger

def get_logger() -> logging.Logger:
    """Get the application logger instance."""
    return logging.getLogger("SmartFileOrganizer")
