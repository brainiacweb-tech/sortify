"""Tests for file classification engine."""
import pytest
from pathlib import Path
from app.core.file_classifier import FileClassifier
from app.services.config_service import ConfigService

@pytest.fixture
def temp_config(tmp_path):
    """Fixture providing a temporary ConfigService using an isolated tmp_path."""
    cfg_file = tmp_path / "test_config.json"
    service = ConfigService(config_file=cfg_file)
    return service

def test_default_classifications(temp_config):
    classifier = FileClassifier(config_service=temp_config)
    
    assert classifier.classify_file("photo.JPG") == "Images"
    assert classifier.classify_file("assignment.pdf") == "PDFs"
    assert classifier.classify_file("movie.mkv") == "Videos"
    assert classifier.classify_file("project.zip") == "Archives"
    assert classifier.classify_file("budget.xlsx") == "Spreadsheets"
    assert classifier.classify_file("installer.exe") == "Applications"
    assert classifier.classify_file("song.mp3") == "Audio"
    assert classifier.classify_file("presentation.pptx") == "Presentations"
    assert classifier.classify_file("script.py") == "Code"
    assert classifier.classify_file("font.ttf") == "Fonts"

def test_unknown_extension_behavior(temp_config):
    classifier = FileClassifier(config_service=temp_config)
    
    # Unknown file organized into Others by default
    assert classifier.classify_file("document.unknownext") == "Others"
    
    # Disable organize_unknown_files
    temp_config.set("organize_unknown_files", False)
    assert classifier.classify_file("document.unknownext") is None

def test_custom_rules(temp_config):
    classifier = FileClassifier(config_service=temp_config)
    
    # Add custom rule for Photoshop files .psd
    temp_config.add_custom_rule("Photoshop", [".psd"], "Photoshop Files")
    
    assert classifier.classify_file("design.psd") == "Photoshop"
    dest = classifier.get_destination_folder(Path("design.psd"), "Photoshop")
    assert dest == Path("Photoshop Files")
