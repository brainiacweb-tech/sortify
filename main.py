"""App entry point for Smart File Organizer."""
import sys
import logging
from pathlib import Path
from app.services.logging_service import setup_logging
from app.gui.main_window import MainWindow

def enable_high_dpi_awareness():
    """Enable crisp Per-Monitor V2 High DPI scaling on Windows to prevent blurriness on 4K displays."""
    if sys.platform == "win32":
        try:
            import ctypes
            # Set Process DPI Awareness (Per-Monitor DPI Aware V2 = 2)
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                import ctypes
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

def main():
    """Initialize application logging and launch desktop GUI main window."""
    enable_high_dpi_awareness()
    try:
        setup_logging()
    except Exception as e:
        print(f"Logging setup warning: {e}", file=sys.stderr)
    logger = logging.getLogger("SmartFileOrganizer")
    logger.info("Launching Smart File Organizer application with 4K High-DPI support...")

    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        logger.critical(f"Unhandled exception in main application thread: {e}", exc_info=True)
        print(f"Error launching application: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
