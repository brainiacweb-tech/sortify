"""Utility script to generate a populated safe sandbox directory for demo testing."""
import os
from pathlib import Path

def create_demo_sandbox(target_dir: str | Path = "sample_sandbox") -> Path:
    """
    Generate a demo folder with sample files across various categories,
    including exact duplicate files for testing triage and hashing.
    """
    sandbox_path = Path(target_dir).resolve()
    sandbox_path.mkdir(parents=True, exist_ok=True)

    files_to_create = [
        # Images
        ("vacation_photo.jpg", b"\xFF\xD8\xFF\xE0 Sample JPEG byte content for vacation photo"),
        ("logo_render.png", b"\x89PNG\r\n\x1a\n Sample PNG byte content for logo render"),
        ("diagram_arch.svg", b"<svg><rect width='100' height='100'/></svg>"),

        # PDFs & Documents
        ("quarterly_report_2026.pdf", b"%PDF-1.4 Sample PDF Quarterly Report content"),
        ("project_proposal.docx", b"PK\x03\x04 Sample Word document proposal content"),
        ("meeting_notes.txt", b"Meeting Notes - October 2026:\n1. Triage files safely.\n2. Verify undo capability."),

        # Spreadsheets & Presentations
        ("budget_q4.xlsx", b"PK\x03\x04 Sample Excel Workbook budget data"),
        ("slide_deck.pptx", b"PK\x03\x04 Sample PowerPoint Presentation slides"),

        # Code & Scripts
        ("file_organizer_script.py", b"import shutil\nprint('Organize files safely!')\n"),
        ("app_styles.css", b"body { font-family: sans-serif; background-color: #0f172a; }\n"),
        ("index.html", b"<!DOCTYPE html><html><body><h1>Smart File Organizer</h1></body></html>"),
        ("package.json", b'{\n  "name": "sortify",\n  "version": "1.0.0"\n}\n'),

        # Archives & Applications
        ("project_backup_v1.zip", b"PK\x03\x04 Sample ZIP archive data"),
        ("installer_setup.exe", b"MZ Sample executable binary header"),

        # Unknown extension
        ("raw_telemetry_dump.dat", b"\x00\x01\x02\x03 Raw binary payload data"),
        ("notes_without_ext", b"Unprocessed text file without file extension")
    ]

    print(f"Creating demo files in '{sandbox_path}'...")
    for filename, content in files_to_create:
        f_path = sandbox_path / filename
        f_path.write_bytes(content)
        print(f"  [+] Created: {filename}")

    # Create exact DUPLICATE files to test SHA-256 duplicate detection
    dup_content = b"\xFF\xD8\xFF\xE0 Exact identical JPEG image bytes for SHA256 duplicate detection test"
    (sandbox_path / "camera_img_1001.jpg").write_bytes(dup_content)
    (sandbox_path / "camera_img_1001_copy.jpg").write_bytes(dup_content)
    (sandbox_path / "camera_img_1001_backup.jpg").write_bytes(dup_content)
    print("  [+] Created 3 identical duplicate copies: camera_img_1001.jpg")

    print(f"\n[SUCCESS] Demo sandbox environment successfully created at: {sandbox_path}")
    return sandbox_path

if __name__ == "__main__":
    create_demo_sandbox()
