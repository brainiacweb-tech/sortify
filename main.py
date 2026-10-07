"""App entry point for Smart File Organizer."""
import sys
import logging
from pathlib import Path
from app.services.logging_service import setup_logging
from app.gui.main_window import MainWindow

def main():
    """Initialize application logging and launch desktop GUI main window."""
    setup_logging()
    logger = logging.getLogger("SmartFileOrganizer")
    logger.info("Launching Smart File Organizer application...")

    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Unhandled exception in main application thread: {e}", exc_info=True)
        print(f"Error launching application: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
