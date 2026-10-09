"""SORTIFY Desktop Application Window Launcher."""
import sys
import os
import threading
from pathlib import Path
from werkzeug.serving import make_server

class DesktopApi:
    """Native Python API exposed to React frontend inside PyWebView."""
    def select_folder(self, initial=""):
        try:
            import webview

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

def start_api_server():
    """Start a private API server on an OS-assigned loopback port."""
    root_dir = Path(__file__).resolve().parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))

    from app.api_server import app

    server = make_server("127.0.0.1", 0, app, threaded=True)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    return server

def main():
    import webview

    try:
        from app.services.logging_service import setup_logging
        setup_logging()
    except Exception as e:
        print(f"[WARN] Logging setup failed: {e}", file=sys.stderr)
    server = start_api_server()
    app_url = f"http://127.0.0.1:{server.server_port}"
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
    
    try:
        webview.start(debug=False)
    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    main()
