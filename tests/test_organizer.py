"""Unit tests for OrganizerEngine scan, dry-run, execution and duplicate quarantine."""
import pytest
from pathlib import Path
from app.core.organizer import OrganizerEngine
from app.services.config_service import ConfigService

def test_dry_run_preview(tmp_path: Path):
    scan_folder = tmp_path / "sandbox"
    scan_folder.mkdir()
    cfg_file = tmp_path / "config.json"
    cfg = ConfigService(config_file=cfg_file)
    engine = OrganizerEngine(config_service=cfg)

    # Create dummy files inside sandbox
    (scan_folder / "photo.jpg").write_bytes(b"image data")
    (scan_folder / "report.pdf").write_bytes(b"pdf data")
    (scan_folder / "script.py").write_bytes(b"print('hello')")
    (scan_folder / "unknown.xyz").write_bytes(b"random data")

    preview = engine.scan_and_preview(scan_folder, recursive=False, check_duplicates=False)
    assert preview.total_files == 4
    assert preview.category_counts.get("Images") == 1
    assert preview.category_counts.get("PDFs") == 1
    assert preview.category_counts.get("Code") == 1
    assert preview.category_counts.get("Others") == 1

def test_execute_organization(tmp_path: Path):
    scan_folder = tmp_path / "sandbox"
    scan_folder.mkdir()
    cfg_file = tmp_path / "config.json"
    history_file = tmp_path / "history.json"
    cfg = ConfigService(config_file=cfg_file)
    engine = OrganizerEngine(config_service=cfg)
    engine.undo_manager.history_file = history_file

    (scan_folder / "vector.svg").write_bytes(b"svg content")
    (scan_folder / "document.docx").write_bytes(b"docx content")

    preview = engine.scan_and_preview(scan_folder, recursive=False, check_duplicates=False)
    assert preview.total_files == 2

    exec_result = engine.execute_organization(preview)
    assert exec_result.total_successful == 2
    assert (scan_folder / "Images" / "vector.svg").exists()
    assert (scan_folder / "Documents" / "document.docx").exists()
    assert not (scan_folder / "vector.svg").exists()
    assert not (scan_folder / "document.docx").exists()

def test_quarantine_duplicates(tmp_path: Path):
    scan_folder = tmp_path / "sandbox"
    scan_folder.mkdir()
    cfg_file = tmp_path / "config.json"
    cfg = ConfigService(config_file=cfg_file)
    engine = OrganizerEngine(config_service=cfg)

    c1 = scan_folder / "dup1.txt"
    c2 = scan_folder / "dup2.txt"
    c1.write_text("Same content")
    c2.write_text("Same content")

    results = engine.quarantine_duplicates(scan_folder, [c2])
    assert len(results) == 1
    assert results[0].success is True
    assert (scan_folder / "Duplicates" / "dup2.txt").exists()
    assert not c2.exists()
