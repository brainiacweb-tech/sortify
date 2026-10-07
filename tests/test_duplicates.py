"""Unit tests for multi-stage SHA-256 duplicate detection."""
import pytest
from pathlib import Path
from app.core.duplicate_detector import DuplicateDetector

def test_no_duplicates_empty_folder(tmp_path: Path):
    detector = DuplicateDetector()
    res = detector.find_duplicates(tmp_path)
    assert res.total_files_scanned == 0
    assert len(res.groups) == 0

def test_identical_files_detected(tmp_path: Path):
    detector = DuplicateDetector()

    # Create 3 identical files
    content = b"Exact identical byte content for SHA256 test" * 50
    f1 = tmp_path / "photo1.png"
    f2 = tmp_path / "photo1_copy.png"
    f3 = tmp_path / "photo1_backup.png"

    f1.write_bytes(content)
    f2.write_bytes(content)
    f3.write_bytes(content)

    # Create 1 unique file with same size but different content
    f4 = tmp_path / "different.png"
    f4.write_bytes(b"Different byte content of same length as content" * 50)

    res = detector.find_duplicates(tmp_path)
    assert res.total_files_scanned == 4
    assert len(res.groups) == 1

    group = res.groups[0]
    assert group.file_size == len(content)
    assert len(group.files) == 3
    assert len(group.duplicate_files) == 2
    assert group.wasted_bytes == len(content) * 2

def test_different_sizes_filtered_fast(tmp_path: Path):
    detector = DuplicateDetector()

    (tmp_path / "a.txt").write_text("Short")
    (tmp_path / "b.txt").write_text("Medium text length")
    (tmp_path / "c.txt").write_text("Longer text content overall")

    res = detector.find_duplicates(tmp_path)
    assert res.total_files_scanned == 3
    assert len(res.groups) == 0
