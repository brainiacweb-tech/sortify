"""Unit tests for UndoManager history journal and restoration logic."""
import pytest
from pathlib import Path
from app.core.file_operations import safe_move_file
from app.core.undo_manager import UndoManager

def test_undo_batch_lifecycle(tmp_path: Path):
    history_file = tmp_path / "history.json"
    undo_mgr = UndoManager(history_file=history_file)

    src_dir = tmp_path / "src"
    dest_dir = tmp_path / "dest"
    src_dir.mkdir()
    dest_dir.mkdir()

    f1 = src_dir / "doc.pdf"
    f2 = src_dir / "pic.jpg"
    f1.write_text("Document text")
    f2.write_text("Picture bytes")

    res1 = safe_move_file(f1, dest_dir)
    res2 = safe_move_file(f2, dest_dir)

    batch = undo_mgr.record_batch(
        batch_id="TEST_BATCH_1",
        base_folder=src_dir,
        move_results=[res1, res2],
        category_map={str(f1): "PDFs", str(f2): "Images"}
    )

    assert batch.batch_id == "TEST_BATCH_1"
    assert len(batch.moves) == 2

    # Execute undo
    success, msg, restore_results = undo_mgr.undo_batch("TEST_BATCH_1")
    assert success is True
    assert f1.exists()
    assert f2.exists()
    assert f1.read_text() == "Document text"
    assert f2.read_text() == "Picture bytes"
    assert not (dest_dir / "doc.pdf").exists()
    assert not (dest_dir / "pic.jpg").exists()

def test_cannot_undo_twice(tmp_path: Path):
    history_file = tmp_path / "history.json"
    undo_mgr = UndoManager(history_file=history_file)

    src_dir = tmp_path / "src"
    dest_dir = tmp_path / "dest"
    src_dir.mkdir()
    dest_dir.mkdir()

    f1 = src_dir / "notes.txt"
    f1.write_text("Notes")
    res1 = safe_move_file(f1, dest_dir)

    undo_mgr.record_batch("TEST_BATCH_2", src_dir, [res1])

    s1, msg1, r1 = undo_mgr.undo_batch("TEST_BATCH_2")
    assert s1 is True

    s2, msg2, r2 = undo_mgr.undo_batch("TEST_BATCH_2")
    assert s2 is False
    assert "already been undone" in msg2
