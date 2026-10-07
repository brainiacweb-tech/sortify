# Engineering & Architecture Document: Smart File Organizer

## 1. Architectural Design Overview
Smart File Organizer follows a clean, modular layer architecture separating UI, Core Business Logic, Services, and Utilities. UI components never directly perform filesystem mutations; all operations pass through dedicated Core managers and Service handlers.

```
                          ┌──────────────────────────┐
                          │   GUI (CustomTkinter)    │
                          └─────────────┬────────────┘
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             ▼                          ▼                          ▼
  ┌──────────────────┐       ┌────────────────────┐      ┌──────────────────┐
  │ Organizer Engine │       │ Duplicate Detector │      │  Stats Service   │
  └──────────┬───────┘       └──────────┬─────────┘      └──────────────────┘
             │                          │
             ├──────────────────────────┤
             ▼                          ▼
  ┌──────────────────┐       ┌────────────────────┐
  │ File Operations  │       │    Undo Manager    │
  └──────────┬───────┘       └──────────┬─────────┘
             │                          │
             └─────────────┬────────────┘
                           ▼
              ┌──────────────────────────┐
              │ File System & Config/Log │
              └──────────────────────────┘
```

## 2. Directory & Module Structure
```
smart-file-organizer-python/
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── organizer.py           # Master organization flow orchestrator
│   │   ├── duplicate_detector.py # 2-stage SHA-256 duplicate detection engine
│   │   ├── file_classifier.py    # Extension-to-category rule evaluation engine
│   │   ├── file_operations.py    # Safe move, copy, collision renaming operations
│   │   └── undo_manager.py       # Operation journal and reverse-restore logic
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py        # Top-level window, sidebar & view router
│   │   ├── dashboard.py          # Dashboard view with storage analytics cards
│   │   ├── organize_view.py      # Folder selection, dry run preview & execution
│   │   ├── duplicates_view.py    # Duplicate group inspector & safe quarantine
│   │   ├── history_view.py       # Activity history log viewer with undo trigger
│   │   ├── rules_view.py         # Custom rule manager UI
│   │   ├── settings_view.py      # Application preferences & theme switcher
│   │   └── components.py         # Reusable UI components (cards, dialogs, tables)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── config_service.py     # Persistent JSON settings & custom rule manager
│   │   ├── logging_service.py    # Application logging configuration
│   │   └── stats_service.py      # Space calculation & breakdown statistics
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── constants.py          # Fixed defaults, paths & UI constants
│   │   ├── helpers.py            # Size formatters, date formatters, safe paths
│   │   └── validators.py         # Directory & path validation rules
│   └── config/
│       └── default_rules.json    # Standard classification mapping
├── logs/                         # App runtime log files
├── tests/                        # Comprehensive pytest test suite
│   ├── test_classifier.py
│   ├── test_organizer.py
│   ├── test_duplicates.py
│   ├── test_file_operations.py
│   └── test_undo.py
├── docs/                         # Documentation assets & screenshots
│   └── screenshots/
├── main.py                       # App entry point
├── create_demo_files.py          # Utility script to generate safe test environment
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── product.md
├── engineering.md
├── ui.md
└── CONTRIBUTING.md
```

## 3. Core Technical Subsystems

### 3.1 File Classification Strategy (`file_classifier.py`)
- Rules are stored in `default_rules.json` and supplemented by custom user configurations via `ConfigService`.
- File extensions are normalized (lowercased, leading dot stripped) and evaluated against rule lookup maps.
- Excluded targets: Subdirectory names matching defined target categories, system/hidden files (`.git`, `desktop.ini`, `Thumbs.db`, `.DS_Store`), and temporary files (`.tmp`, `~$*`).

### 3.2 Duplicate Detection Algorithm (`duplicate_detector.py`)
To achieve peak performance over massive file collections:
1. **Size Filter**: Traverse candidate files and group by `path.stat().st_size`. Files with unique sizes are immediately filtered out.
2. **Chunk Hashing**: For groups of size size >= 2:
   - Compute SHA-256 hash by reading data in 1 MB (1,048,576 bytes) chunks:
     ```python
     hasher = hashlib.sha256()
     with open(filepath, "rb") as f:
         while chunk := f.read(1048576):
             hasher.update(chunk)
     ```
3. **Group Assembly**: Files sharing matching SHA-256 hashes are grouped as duplicates, designating the oldest modified file or top-level file as reference original.

### 3.3 Collision Resolution Engine (`file_operations.py`)
When moving file `source` to `destination/filename.ext`:
- If `destination/filename.ext` exists:
  - Extract stem (`filename`) and suffix (`.ext`).
  - Iteratively test `filename_1.ext`, `filename_2.ext`, ... until an unallocated filename is found.
  - Execute move and return final path to calling context.

### 3.4 Undo & Journal System (`undo_manager.py`)
- Every execution generates a structured operation batch record in `history.json`:
  ```json
  {
    "batch_id": "20261007_193500",
    "timestamp": "2026-10-07 19:35:00",
    "moves": [
      {"source": "/path/to/Downloads/report.pdf", "destination": "/path/to/Downloads/PDFs/report.pdf", "status": "SUCCESS"}
    ]
  }
  ```
- Triggering `undo_batch(batch_id)` reads items in reverse order and safely moves destination files back to original source paths (applying conflict renaming if original source path has since been reoccupied).

### 3.5 Multithreading & GUI Responsiveness
- All long-running disk operations (scanning, preview generation, file moving, hashing) execute inside `threading.Thread` instances.
- UI state updates use thread-safe queues or CustomTkinter `after()` callbacks.
- Cancellable execution flag checked inside file traversal loops.

## 4. Testing & Quality Assurance
- Automated tests built with `pytest`.
- Mandatory use of `tmp_path` fixture for filesystem isolation—never execute tests against user Desktop or Downloads folders.
- Edge cases tested: Empty files, locked files, special characters in filenames, identical size but different hashes, duplicate detection over chunk boundaries, and full undo lifecycle.
