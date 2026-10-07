# Product Requirement Document (PRD): Smart File Organizer

## 1. Problem Statement
Desktop users, students, developers, and professionals frequently accumulate hundreds of unorganized files in their `Downloads`, `Desktop`, `Documents`, and media directories. Manual file triage is tedious, error-prone, and often leads to storage waste through undetected duplicate downloads. Existing command-line tools or basic scripts lack visual safety nets, lack full undo capability, and pose risks of silent file overwrites or data loss.

## 2. Target Audience & Personas
- **Students & Researchers**: Download dozens of PDFs, slides, assignments, and zip files daily. Need quick categorization by document type.
- **Content Creators & Designers**: Work with high volumes of raw photos, vectors, audio, and video rendering exports.
- **Software Engineers & IT Professionals**: Frequently download source code archives, binary packages, installers, and logs.
- **General Desktop Users**: Desire a simple, visually appealing tool to declutter their system without fear of losing important documents.

## 3. Core Objectives & Value Proposition
- **Automated Triage**: Automatically classify files into logical category subfolders (e.g., `Images`, `PDFs`, `Documents`, `Code`, `Archives`).
- **Cryptographic Duplicate Detection**: Identify exact duplicate files via file-size grouping followed by SHA-256 chunk-based hashing.
- **Filesystem Safety First**: Guarantee zero data loss through mandatory dry-run previews, conflict-resolving automatic renaming (e.g., `photo_1.jpg`), non-destructive duplicate handling, and full action undo capabilities.
- **User Empowerment**: Allow complete customization of extension-to-category rules, recursive scan preferences, and theme choices.

## 4. Feature Set & Functional Requirements

### 4.1 File Classification Engine
- Case-insensitive extension mapping based on JSON configuration defaults.
- Extension mapping into 11+ default categories (`Images`, `PDFs`, `Documents`, `Spreadsheets`, `Presentations`, `Videos`, `Audio`, `Archives`, `Code`, `Applications`, `Fonts`, `Others`).
- User ability to add, edit, or delete custom extension rules.

### 4.2 Safe File Operations & Conflict Resolution
- Never overwrite existing files. If `Images/photo.jpg` already exists, automatically generate a safe collision-free filename like `photo_1.jpg`.
- Safe file move using atomic operations where supported (`shutil.move` with path validation).
- Avoid organizing the tool's own category folders recursively into themselves.

### 4.3 SHA-256 Duplicate Detection Engine
- Optimized multi-stage hashing:
  1. Quick grouping by exact file size.
  2. Sequential 1 MB chunk hashing for size-matched candidate groups.
- Display duplicate groups with file sizes, paths, and SHA-256 hashes.
- Non-destructive resolution: move duplicates into a designated `Duplicates/` folder or ignore them. No automatic permanent deletion.

### 4.4 Dry Run & Preview Mode
- Full dry-run calculation before performing any disk write.
- Interactive table showing target destination paths, size breakdown, and detected duplicates.
- Summary analytics: Total files, Storage size, Category counts, Duplicate wasted space.

### 4.5 Undo & Activity Logging
- Persistent activity logging recording every file operation (timestamp, source, destination, status).
- Single-click "Undo Last Organization" to safely return files to their exact original locations.

### 4.6 Desktop GUI & Analytics
- Modern dark/light theme desktop interface using CustomTkinter with standard Tkinter fallback.
- Sidebar navigation: Dashboard, Organize Files, Duplicates, History, Rules, Settings.
- Responsive threaded operations with progress feedback and immediate cancellation capability.

## 5. Non-Functional Requirements
- **Performance**: Capable of scanning 10,000+ files in under 5 seconds (size grouping) and chunk-hashing large files without UI freezing or memory spikes.
- **Portability**: Cross-platform ready (Windows 10/11 primary, compatible with macOS and Linux via `pathlib`).
- **Reliability**: Graceful error recovery for locked, open, or permission-denied files.
- **Maintainability**: High test coverage (>90%) with `pytest`, strict type hints, and PEP 8 compliance.

## 6. Success Metrics & Criteria
- Zero accidental file deletions or overwrites in all test cases.
- 100% accurate file restoration upon triggering "Undo".
- Clean execution of automated test suite covering classification, conflict resolution, hashing, and undo logic.
