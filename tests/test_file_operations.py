"""Unit tests for safe file operations and collision resolution."""
import pytest
from pathlib import Path
from app.core.file_operations import safe_move_file, safe_restore_file
from app.utils.helpers import get_safe_filename

def test_safe_filename_no_collision(tmp_path: Path):
    target_dir = tmp_path / "dest"
    target_dir.mkdir()
    safe_path = get_safe_filename(target_dir, "document.pdf")
    assert safe_path.name == "document.pdf"

def test_safe_filename_with_collision(tmp_path: Path):
    target_dir = tmp_path / "dest"
    target_dir.mkdir()
    (target_dir / "document.pdf").write_text("existing content")

    safe_path = get_safe_filename(target_dir, "document.pdf")
    assert safe_path.name == "document_1.pdf"

    (target_dir / "document_1.pdf").write_text("another existing content")
    safe_path2 = get_safe_filename(target_dir, "document.pdf")
    assert safe_path2.name == "document_2.pdf"

def test_safe_move_file_success(tmp_path: Path):
    src_dir = tmp_path / "src"
    dest_dir = tmp_path / "dest"
    src_dir.mkdir()
    
    src_file = src_dir / "test.txt"
    src_file.write_text("Hello World")

    result = safe_move_file(src_file, dest_dir)
    assert result.success is True
    assert result.source_path == src_file
    assert result.destination_path == dest_dir / "test.txt"
    assert (dest_dir / "test.txt").exists()
    assert (dest_dir / "test.txt").read_text() == "Hello World"
    assert not src_file.exists()

def test_safe_move_file_collision_renaming(tmp_path: Path):
    src_dir = tmp_path / "src"
    dest_dir = tmp_path / "dest"
    src_dir.mkdir()
    dest_dir.mkdir()

    (dest_dir / "image.png").write_text("Existing Image")

    src_file = src_dir / "image.png"
    src_file.write_text("New Image")

    result = safe_move_file(src_file, dest_dir)
    assert result.success is True
    assert result.was_renamed is True
    assert result.destination_path.name == "image_1.png"
    assert (dest_dir / "image_1.png").read_text() == "New Image"

def test_safe_restore_file(tmp_path: Path):
    orig_dir = tmp_path / "original"
    dest_dir = tmp_path / "organized"
    orig_dir.mkdir()
    dest_dir.mkdir()

    orig_file = orig_dir / "sample.pdf"
    moved_file = dest_dir / "sample.pdf"
    moved_file.write_text("Sample PDF Content")

    result = safe_restore_file(moved_file, orig_file)
    assert result.success is True
    assert (orig_dir / "sample.pdf").exists()
    assert not moved_file.exists()
