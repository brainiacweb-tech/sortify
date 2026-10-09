"""Tests for the desktop app's file-backed API endpoints."""
from io import BytesIO
from pathlib import Path

from app import api_server
from app.core.undo_manager import UndoManager
from app.services.stats_service import StatsService


def test_new_install_has_empty_stats_and_history(tmp_path: Path, monkeypatch):
    history_file = tmp_path / "history.json"
    undo_manager = UndoManager(history_file=history_file)
    monkeypatch.setattr(api_server, "undo_manager", undo_manager)
    monkeypatch.setattr(api_server, "stats_service", StatsService(undo_manager))
    client = api_server.app.test_client()

    stats_response = client.get("/api/stats")
    history_response = client.get("/api/history")

    assert stats_response.status_code == 200
    assert stats_response.get_json() == {
        "total_files_organized": 0,
        "total_runs": 0,
        "duplicates_found": 0,
        "category_breakdown": {},
        "categories_count": len(api_server.config_service.get_all_categories()),
    }
    assert history_response.status_code == 200
    assert history_response.get_json() == []


def test_default_folders_do_not_create_a_sample_sandbox(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(
        "app.utils.constants.get_user_app_dir",
        lambda: tmp_path,
    )
    client = api_server.app.test_client()

    response = client.get("/api/default-folders")

    assert response.status_code == 200
    assert "sandbox" not in response.get_json()
    assert not (tmp_path / "sample_sandbox").exists()


def test_upload_saves_each_batch_to_its_own_folder(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(
        "app.utils.constants.get_user_app_dir",
        lambda: tmp_path,
    )
    client = api_server.app.test_client()

    first_response = client.post(
        "/api/upload",
        data={"files": (BytesIO(b"first"), "report.txt")},
        content_type="multipart/form-data",
    )
    second_response = client.post(
        "/api/upload",
        data={"files": (BytesIO(b"second"), "report.txt")},
        content_type="multipart/form-data",
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    first_batch = Path(first_response.get_json()["target_directory"])
    second_batch = Path(second_response.get_json()["target_directory"])
    assert first_batch != second_batch
    assert (first_batch / "report.txt").read_bytes() == b"first"
    assert (second_batch / "report.txt").read_bytes() == b"second"
    assert not (tmp_path / "sample_sandbox").exists()
