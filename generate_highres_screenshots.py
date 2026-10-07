"""Generate 4 crisp 1920x1080 PNG screenshots of SORTIFY for Microsoft Store listing."""
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def draw_sidebar(draw, active_item="Dashboard"):
    # Dark sidebar background #0F172A
    draw.rectangle([0, 0, 360, 1080], fill=(15, 23, 42))
    
    # Header area
    try:
        logo = Image.open('app/assets/logo.png').convert('RGBA')
        logo_w, logo_h = 240, int(240 * logo.height / logo.width)
        logo_res = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        # We will paste logo on canvas later
    except Exception:
        pass

    # Navigation items
    nav_items = [
        ("📊 Dashboard", "Dashboard"),
        ("📁 Organize Files", "Organize"),
        ("🔍 Duplicates", "Duplicates"),
        ("📜 History & Undo", "History"),
        ("⚙️ Custom Rules", "Rules"),
        ("🛠️ Settings", "Settings"),
    ]

    y = 180
    for text, name in nav_items:
        if name == active_item:
            # Active blue highlight #2563EB
            draw.rounded_rectangle([20, y, 340, y + 54], radius=10, fill=(37, 99, 235))
            draw.text((45, y + 16), text, fill=(255, 255, 255))
        else:
            draw.text((45, y + 16), text, fill=(148, 163, 184))
        y += 68

def create_screenshot(view_name, filename):
    canvas = Image.new("RGBA", (1920, 1080), (15, 23, 42, 255))
    
    # Right main area background #020617
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([360, 0, 1920, 1080], fill=(2, 6, 23))

    # Paste Sidebar
    draw_sidebar(draw, view_name)

    # Paste logo on sidebar top
    try:
        logo = Image.open('app/assets/logo.png').convert('RGBA')
        logo_w, logo_h = 250, int(250 * logo.height / logo.width)
        logo_res = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        canvas.paste(logo_res, (35, 35), logo_res)
    except Exception:
        pass

    # Developer by line
    draw.text((40, 115), "by Francis Kusi", fill=(59, 130, 246))

    # Draw View Specific Content
    if view_name == "Dashboard":
        # Header
        draw.text((400, 40), "📊 SORTIFY Dashboard", fill=(248, 250, 252))
        draw.text((400, 85), "Developed by Francis Kusi  |  Overview of file triage activities and storage optimization metrics.", fill=(59, 130, 246))

        # 4 Stat Cards
        cards = [
            ("Files Organized", "55", "📁", (30, 41, 59)),
            ("Organization Runs", "3", "⚡", (30, 41, 59)),
            ("Duplicates Found", "3", "🔍", (30, 41, 59)),
            ("Engine Status", "Ready", "🛡️", (30, 41, 59)),
        ]
        x = 400
        for title, val, icon, color in cards:
            draw.rounded_rectangle([x, 140, x + 340, 260], radius=16, fill=color)
            draw.text((x + 24, 160), f"{icon}  {title}", fill=(148, 163, 184))
            draw.text((x + 24, 200), val, fill=(255, 255, 255))
            x += 365

        # Banner Box
        draw.rounded_rectangle([400, 290, 1860, 390], radius=16, fill=(30, 41, 59))
        draw.text((430, 325), "Declutter & organize your Downloads or Desktop folder in seconds.", fill=(255, 255, 255))
        draw.rounded_rectangle([1550, 315, 1830, 365], radius=10, fill=(37, 99, 235))
        draw.text((1580, 330), "🚀 Start Organization", fill=(255, 255, 255))

        # Category Progress Box
        draw.rounded_rectangle([400, 420, 1860, 1020], radius=16, fill=(30, 41, 59))
        draw.text((430, 450), "Category Distribution & Storage Metrics", fill=(255, 255, 255))

        cats = [
            ("Documents", "22 files (40%)", 0.40, (59, 130, 246)),
            ("PDFs", "14 files (25%)", 0.25, (16, 185, 129)),
            ("Images", "10 files (18%)", 0.18, (245, 158, 11)),
            ("Code & Scripts", "5 files (9%)", 0.09, (139, 92, 246)),
            ("Archives", "4 files (8%)", 0.08, (236, 72, 153)),
        ]

        y_cat = 510
        for cname, cstat, pct, col in cats:
            draw.text((430, y_cat), cname, fill=(255, 255, 255))
            # Progress bar background
            draw.rounded_rectangle([620, y_cat + 4, 1600, y_cat + 22], radius=9, fill=(15, 23, 42))
            # Filled progress
            draw.rounded_rectangle([620, y_cat + 4, 620 + int(980 * pct), y_cat + 22], radius=9, fill=col)
            draw.text((1630, y_cat), cstat, fill=(148, 163, 184))
            y_cat += 75

    elif view_name == "Organize":
        draw.text((400, 40), "📁 Organize Files & Dry-Run Preview", fill=(248, 250, 252))
        draw.text((400, 85), "Select a directory to preview and execute safe categorical file triage.", fill=(148, 163, 184))

        # Control panel
        draw.rounded_rectangle([400, 130, 1860, 290], radius=16, fill=(30, 41, 59))
        draw.text((430, 160), "Target Folder: C:\\Users\\USER\\Downloads", fill=(255, 255, 255))
        draw.rounded_rectangle([1650, 150, 1830, 195], radius=8, fill=(37, 99, 235))
        draw.text((1675, 163), "Browse Folder", fill=(255, 255, 255))

        # Buttons
        draw.rounded_rectangle([430, 215, 620, 260], radius=8, fill=(5, 150, 105))
        draw.text((450, 230), "🔍 Scan & Preview", fill=(255, 255, 255))

        draw.rounded_rectangle([640, 215, 840, 260], radius=8, fill=(37, 99, 235))
        draw.text((660, 230), "⚡ Organize Files", fill=(255, 255, 255))

        # Treeview Table Box
        draw.rounded_rectangle([400, 310, 1860, 1020], radius=16, fill=(30, 41, 59))
        
        # Headers
        draw.rectangle([400, 310, 1860, 360], fill=(15, 23, 42))
        draw.text((430, 328), "Filename", fill=(148, 163, 184))
        draw.text((750, 328), "Category", fill=(148, 163, 184))
        draw.text((950, 328), "Destination Path", fill=(148, 163, 184))
        draw.text((1480, 328), "Size", fill=(148, 163, 184))
        draw.text((1650, 328), "Status", fill=(148, 163, 184))

        table_rows = [
            ("vacation_photo.jpg", "Images", "Images/vacation_photo.jpg", "4.2 MB", "OK"),
            ("quarterly_report_2026.pdf", "PDFs", "PDFs/quarterly_report_2026.pdf", "1.8 MB", "OK"),
            ("project_proposal.docx", "Documents", "Documents/project_proposal.docx", "840 KB", "OK"),
            ("photo_camera_1001.jpg", "Images", "Images/photo_camera_1001_1.jpg", "3.1 MB", "⚠️ Renaming Collision"),
            ("budget_q4.xlsx", "Spreadsheets", "Spreadsheets/budget_q4.xlsx", "520 KB", "OK"),
            ("file_organizer.py", "Code", "Code/file_organizer.py", "45 KB", "OK"),
            ("backup_archive.zip", "Archives", "Archives/backup_archive.zip", "18.5 MB", "OK"),
            ("duplicate_photo.jpg", "Images", "Images/duplicate_photo_1.jpg", "3.1 MB", "⚠️ Duplicate Detected"),
        ]

        y_r = 380
        for fn, cat, dest, sz, st in table_rows:
            draw.text((430, y_r), fn, fill=(248, 250, 252))
            draw.text((750, y_r), cat, fill=(59, 130, 246))
            draw.text((950, y_r), dest, fill=(148, 163, 184))
            draw.text((1480, y_r), sz, fill=(248, 250, 252))
            
            st_col = (239, 68, 68) if "⚠️" in st else (16, 185, 129)
            draw.text((1650, y_r), st, fill=st_col)
            y_r += 65

    elif view_name == "Duplicates":
        draw.text((400, 40), "🔍 Cryptographic Duplicate Finder", fill=(248, 250, 252))
        draw.text((400, 85), "Identify exact duplicate files using SHA-256 chunk hashing and safely quarantine them.", fill=(148, 163, 184))

        draw.rounded_rectangle([400, 130, 1860, 240], radius=16, fill=(30, 41, 59))
        draw.text((430, 160), "Scan Directory: C:\\Users\\USER\\Downloads", fill=(255, 255, 255))
        draw.rounded_rectangle([430, 185, 750, 225], radius=8, fill=(217, 119, 6))
        draw.text((450, 198), "🛡️ Quarantine Selected Duplicates", fill=(255, 255, 255))

        draw.text((1150, 198), "Found 3 duplicate copies across 1 group (9.3 MB wasted space).", fill=(245, 158, 11))

        draw.rounded_rectangle([400, 260, 1860, 1020], radius=16, fill=(30, 41, 59))
        draw.rectangle([400, 260, 1860, 310], fill=(15, 23, 42))
        draw.text((430, 278), "Role", fill=(148, 163, 184))
        draw.text((650, 278), "Filename", fill=(148, 163, 184))
        draw.text((950, 278), "Size", fill=(148, 163, 184))
        draw.text((1100, 278), "SHA-256 Hash", fill=(148, 163, 184))
        draw.text((1350, 278), "Full Path", fill=(148, 163, 184))

        dup_rows = [
            ("Original File", "camera_img_1001.jpg", "3.1 MB", "e3b0c44298fc...", "C:\\Users\\USER\\Downloads\\camera_img_1001.jpg", (16, 185, 129)),
            ("Duplicate Copy", "camera_img_1001_copy.jpg", "3.1 MB", "e3b0c44298fc...", "C:\\Users\\USER\\Downloads\\camera_img_1001_copy.jpg", (239, 68, 68)),
            ("Duplicate Copy", "camera_img_1001_backup.jpg", "3.1 MB", "e3b0c44298fc...", "C:\\Users\\USER\\Downloads\\camera_img_1001_backup.jpg", (239, 68, 68)),
        ]

        y_d = 330
        for role, fn, sz, hs, fp, col in dup_rows:
            draw.text((430, y_d), role, fill=col)
            draw.text((650, y_d), fn, fill=(248, 250, 252))
            draw.text((950, y_d), sz, fill=(248, 250, 252))
            draw.text((1100, y_d), hs, fill=(148, 163, 184))
            draw.text((1350, y_d), fp, fill=(148, 163, 184))
            y_d += 65

    elif view_name == "History":
        draw.text((400, 40), "📜 Activity History & Undo Journal", fill=(248, 250, 252))
        draw.text((400, 85), "Audit every past organization run and safely reverse file moves with 100% precision.", fill=(148, 163, 184))

        # Batches list (Left)
        draw.rounded_rectangle([400, 130, 950, 1020], radius=16, fill=(30, 41, 59))
        draw.text((430, 155), "Past Organization Runs", fill=(255, 255, 255))
        draw.rounded_rectangle([780, 145, 930, 185], radius=8, fill=(220, 38, 38))
        draw.text((800, 158), "↩️ Undo Batch", fill=(255, 255, 255))

        batches = [
            ("📅 2026-10-07 19:53:48", "55 files • Downloads", "ACTIVE", (16, 185, 129)),
            ("📅 2026-10-07 18:20:12", "12 files • Desktop", "UNDONE", (100, 116, 139)),
            ("📅 2026-10-06 14:10:05", "40 files • Documents", "ACTIVE", (16, 185, 129)),
        ]

        y_b = 210
        for dt, info, st, col in batches:
            draw.rounded_rectangle([420, y_b, 930, y_b + 80], radius=10, fill=(15, 23, 42))
            draw.text((440, y_b + 15), dt, fill=(248, 250, 252))
            draw.text((850, y_b + 15), st, fill=col)
            draw.text((440, y_b + 45), info, fill=(148, 163, 184))
            y_b += 95

        # Move Details Table (Right)
        draw.rounded_rectangle([970, 130, 1860, 1020], radius=16, fill=(30, 41, 59))
        draw.text((1000, 155), "File Move Details (Batch 20261007_195348)", fill=(255, 255, 255))

        draw.rectangle([970, 195, 1860, 240], fill=(15, 23, 42))
        draw.text((1000, 210), "Original Source Path", fill=(148, 163, 184))
        draw.text((1350, 210), "Destination Path", fill=(148, 163, 184))
        draw.text((1680, 210), "Category", fill=(148, 163, 184))
        draw.text((1780, 210), "Status", fill=(148, 163, 184))

        m_rows = [
            ("report_q3.pdf", "PDFs/report_q3.pdf", "PDFs", "SUCCESS"),
            ("photo_grad.jpg", "Images/photo_grad.jpg", "Images", "SUCCESS"),
            ("proposal.docx", "Documents/proposal.docx", "Documents", "SUCCESS"),
            ("notes.txt", "Documents/notes.txt", "Documents", "SUCCESS"),
            ("archive.zip", "Archives/archive.zip", "Archives", "SUCCESS"),
        ]

        y_m = 260
        for src, dest, cat, st in m_rows:
            draw.text((1000, y_m), src, fill=(248, 250, 252))
            draw.text((1350, y_m), dest, fill=(148, 163, 184))
            draw.text((1680, y_m), cat, fill=(59, 130, 246))
            draw.text((1780, y_m), st, fill=(16, 185, 129))
            y_m += 65

    # Save PNG
    assets_file = Path("app/assets") / filename
    canvas.save(assets_file, "PNG")

    desktop_dir = Path.home() / "OneDrive" / "Desktop"
    if not desktop_dir.exists():
        desktop_dir = Path.home() / "Desktop"

    shutil.copy(assets_file, desktop_dir / filename)
    print(f"[+] Successfully generated 1920x1080 PNG screenshot: {filename}")

if __name__ == "__main__":
    create_screenshot("Dashboard", "screenshot_1_dashboard.png")
    create_screenshot("Organize", "screenshot_2_organize.png")
    create_screenshot("Duplicates", "screenshot_3_duplicates.png")
    create_screenshot("History", "screenshot_4_history.png")
