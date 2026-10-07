"""Script to generate crisp 1920x1080 PNG screenshots of SORTIFY for Microsoft Store listing."""
import time
import shutil
from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageGrab, ImageDraw, ImageFont
from app.gui.main_window import MainWindow

def capture_store_screenshots():
    """Render and capture 4 crisp 1920x1080 screenshots of SORTIFY views."""
    desktop_dir = Path.home() / "OneDrive" / "Desktop"
    if not desktop_dir.exists():
        desktop_dir = Path.home() / "Desktop"

    app = MainWindow()
    app.geometry("1920x1080")
    app.update()
    time.sleep(0.5)

    views_to_capture = [
        ("dashboard", "screenshot_1_dashboard.png"),
        ("organize", "screenshot_2_organize.png"),
        ("duplicates", "screenshot_3_duplicates.png"),
        ("history", "screenshot_4_history.png"),
    ]

    generated_files = []

    for view_name, filename in views_to_capture:
        app.navigate_to(view_name)
        app.update_idletasks()
        app.update()
        time.sleep(0.5)

        # Capture window coordinates
        x = app.winfo_rootx()
        y = app.winfo_rooty()
        w = app.winfo_width()
        h = app.winfo_height()

        if w > 0 and h > 0:
            bbox = (x, y, x + w, y + h)
            img = ImageGrab.grab(bbox=bbox)
            # Ensure exact 1920x1080 dimensions
            img_1080 = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            
            assets_path = Path("app/assets") / filename
            img_1080.save(assets_path, "PNG")
            
            desktop_path = desktop_dir / filename
            img_1080.save(desktop_path, "PNG")
            
            print(f"[+] Captured {filename}: 1920x1080 PNG saved to Desktop")
            generated_files.append(desktop_path)

    app.destroy()
    return generated_files

if __name__ == "__main__":
    capture_store_screenshots()
