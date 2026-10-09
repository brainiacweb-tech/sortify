"""SORTIFY Desktop Application Window Launcher."""
import sys
import os
import time
import threading
import urllib.request
from pathlib import Path
import webview

class DesktopApi:
    """Native Python API exposed to React frontend inside PyWebView."""
    def select_folder(self, initial=""):
        try:
            if not initial or not os.path.exists(initial):
                initial = str(Path.home() / "Downloads")
            if webview.windows and len(webview.windows) > 0:
                res = webview.windows[0].create_file_dialog(
                    webview.FileDialog.FOLDER,
                    directory=initial
                )
                if res and len(res) > 0:
                    return {"folder": res[0], "cancelled": False}
        except Exception as e:
            print("[ERROR] PyWebView dialog error:", e)
        return {"folder": "", "cancelled": True}

def ensure_api_server_running():
    """Start Flask API Server on port 5000 if not already running."""
    try:
        urllib.request.urlopen("http://127.0.0.1:5000/api/stats", timeout=1)
        print("[INFO] SORTIFY Backend API Server is active on port 5000.")
    except Exception:
        print("[INFO] Starting SORTIFY Backend API Server in background thread...")
        root_dir = Path(__file__).resolve().parent
        if str(root_dir) not in sys.path:
            sys.path.insert(0, str(root_dir))
        
        from app.api_server import app
        server_thread = threading.Thread(
            target=lambda: app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False),
            daemon=True
        )
        server_thread.start()
        time.sleep(1.5)

def main():
    try:
        from app.services.logging_service import setup_logging
        setup_logging()
    except Exception as e:
        print(f"[WARN] Logging setup failed: {e}", file=sys.stderr)
    ensure_api_server_running()
    
    # Point directly to Flask production server on port 5000
    app_url = "http://127.0.0.1:5000"
    print(f"[INFO] Launching SORTIFY Desktop Window connected to {app_url}...")
    
    api_instance = DesktopApi()
    window = webview.create_window(
        title="SORTIFY - Smart File Organizer",
        url=app_url,
        width=1280,
        height=840,
        resizable=True,
        min_size=(980, 680),
        background_color="#FFFFFF",
        js_api=api_instance
    )
    
    webview.start(debug=False)

if __name__ == "__main__":
    main()
