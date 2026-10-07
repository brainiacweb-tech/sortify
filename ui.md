# UI/UX Specification Document: Smart File Organizer

## 1. Visual Design Philosophy & Aesthetics
- **Modern Desktop Experience**: Clean dark/light theme options built using CustomTkinter with crisp typography, high contrast, smooth rounded corners, and clear visual hierarchy.
- **Visual Safety Nets**: Highlighting actions clearly before execution. Non-destructive design with clear color coding (e.g., Blue for Scan/Preview, Green for Safe Move, Amber/Orange for Duplicate Warnings, Soft Red for Cancellation).

## 2. Main Window Layout Structure
The application uses a responsive two-column sidebar layout:
- **Left Sidebar (Navigation)**:
  - App Logo & Title: `Smart File Organizer`
  - Navigation Buttons:
    - 📊 Dashboard
    - 📁 Organize Files
    - 🔍 Duplicates
    - 📜 History
    - ⚙️ Custom Rules
    - 🛠️ Settings
  - Footer: Version string and About modal trigger.
- **Right Main Content Area**:
  - Dynamically updates to display the active view frame based on sidebar selection.

## 3. Detailed View Specifications

### 3.1 Dashboard View
- **Summary Cards**:
  - Total Files Scanned
  - Total Files Organized
  - Duplicate Files Detected
  - Total Storage Processed
  - Duplicate Wasted Space (e.g., `1.4 GB Wasted`)
- **Quick Action**: Prominent folder selection banner and direct "Scan & Organize" action button.
- **Category Breakdown Table / Progress Bars**: Displays file count per category with visual percentage bars.

### 3.2 Organize Files View (Scan & Dry Run Preview)
- **Folder Selector Controls**:
  - Path input bar with "Browse Folder" button.
  - Scan Options toggles: `[ ] Scan Subfolders (Recursive)`, `[x] Organize Unknown Files into 'Others'`.
- **Action Toolbar**:
  - `[ Scan Folder ]` (Initiates threaded scan)
  - `[ Preview Organization ]` (Populates Dry-Run table without disk writes)
  - `[ Organize Files ]` (Executes safe file moves)
  - `[ Cancel Scan ]` (Visible during active background scanning)
- **Dry-Run Preview Table**:
  - Columns: `Filename`, `Original Category`, `Target Path`, `File Size`, `Status / Collision Warning`.
  - Filterable by extension or search term.

### 3.3 Duplicates View
- **Duplicate Group Inspector**:
  - Cards for each detected duplicate group showing file size and SHA-256 hash snippet.
  - Comparison table listing original vs duplicates with full path view.
- **Actions**:
  - `[ Move Selected to Duplicates Folder ]` (Quarantines file safely)
  - `[ Open File Location ]` (Opens OS file explorer)
  - `[ Ignore Duplicate ]`

### 3.4 History View
- Chronological list of organization runs.
- Detailed operation table (Timestamp, Action, Original Path, Target Path, Status).
- Prominent `[ Undo Last Organization ]` button with confirmation prompt.

### 3.5 Rules & Settings Views
- **Rules View**: Grid of categories with file extension tags. Modal dialogs for adding new custom extensions or creating custom category rules.
- **Settings View**:
  - Theme selection: Light, Dark, System default.
  - Default behaviors: Recursive scan default state, Confirm before organize, Auto-open summary.
  - Reset application settings to factory default.

## 4. UI Safety & Feedback Dialogs
- **Confirmation Modals**: Requiring explicit user approval before initiating batch moves.
- **Summary Modal**: Displays organized breakdown stats immediately after completion with direct link to View History or Undo.
- **Error Toasts**: Soft warning dialogs for locked or permission-denied files with option to skip and continue batch.
