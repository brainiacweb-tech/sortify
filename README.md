# Smart File Organizer (Sortify) 📁⚡

> A modern, safe, high-performance desktop file triage & organization engine for Windows, macOS, and Linux. Built with Python and CustomTkinter.

---

## 🌟 Key Features

- **Automated Extension Triage**: Classify files into clean category folders (`Images`, `PDFs`, `Documents`, `Spreadsheets`, `Presentations`, `Videos`, `Audio`, `Archives`, `Code`, `Applications`, `Fonts`, `Others`).
- **Cryptographic Duplicate Detection**: 2-stage multi-stage hashing (File size filtering -> SHA-256 1 MB chunk hashing) identifies duplicate downloads instantly without memory spikes.
- **100% Filesystem Safety First**: 
  - Mandatory **Dry-Run Preview Mode** before writing changes to disk.
  - Non-destructive **Collision-Free Renaming** (`photo_1.jpg`, `photo_2.jpg`).
  - Zero accidental overwrites or file deletions.
- **1-Click Activity Undo**: Full operation journaling with instant reverse restoration back to original source paths.
- **Custom Classification Rules**: Easily add custom extension mappings or new categories.
- **Modern Dark/Light Desktop UI**: Built using CustomTkinter with responsive sidebar navigation and live storage progress bars.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Demo File Generator (Optional)
Generate a populated sandbox directory with sample files and duplicate images to safely test the app:
```bash
python create_demo_files.py
```

### 3. Launch Application
```bash
python main.py
```

### 4. Run Automated Test Suite
```bash
python -m pytest
```

---

## 🛠️ Architecture

```
smart-file-organizer-python/
├── app/
│   ├── core/
│   │   ├── file_classifier.py    # Rule evaluation engine
│   │   ├── file_operations.py    # Safe move & collision resolution
│   │   ├── duplicate_detector.py # 2-stage SHA-256 duplicate engine
│   │   ├── undo_manager.py       # Activity history journal & undo restore
│   │   └── organizer.py           # Master organization flow orchestrator
│   ├── gui/
│   │   ├── main_window.py        # Top-level window & sidebar router
│   │   ├── dashboard.py          # Storage analytics dashboard
│   │   ├── organize_view.py      # Folder selection & dry-run preview table
│   │   ├── duplicates_view.py    # Duplicate inspector & quarantine
│   │   ├── history_view.py       # Activity log viewer & 1-click undo
│   │   ├── rules_view.py         # Category extension rule editor
│   │   ├── settings_view.py      # Application settings & themes
│   │   └── components.py         # Reusable CustomTkinter UI widgets
│   ├── services/
│   │   ├── config_service.py     # Persistent settings manager
│   │   ├── logging_service.py    # Application log configuration
│   │   └── stats_service.py      # Storage analytics & breakdown stats
│   └── utils/
│       ├── constants.py          # App defaults & paths
│       ├── helpers.py            # Size formatters & collision helpers
│       └── validators.py         # System directory safeguards
├── tests/                        # Automated Pytest suite
│   ├── test_classifier.py
│   ├── test_duplicates.py
│   ├── test_file_operations.py
│   ├── test_organizer.py
│   └── test_undo.py
├── main.py                       # App launcher
└── create_demo_files.py          # Demo sandbox generator
```

---

## 🧪 Testing Coverage

The project includes unit tests covering 100% of core algorithms:
- `test_classifier.py`: Extension mapping & unknown handling
- `test_duplicates.py`: Identical file hash matching & size filtering
- `test_file_operations.py`: Safe moves, collision renaming, path validation
- `test_organizer.py`: Dry run calculation & batch execution
- `test_undo.py`: Reverse restoration & batch journal integrity

To run tests with verbose output:
```bash
python -m pytest -v
```

---

## 📄 License
MIT License. Free for personal and commercial use.
