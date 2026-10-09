"""Real File System API Server for SORTIFY connecting React UI to Python Core Engines."""
import os
import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

# Ensure workspace root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename

from app.services.config_service import ConfigService
from app.core.file_classifier import FileClassifier
from app.core.undo_manager import UndoManager
from app.core.duplicate_detector import DuplicateDetector
from app.services.stats_service import StatsService
from app.core.organizer import OrganizerEngine, DryRunResult, DryRunItem
from app.core.file_operations import safe_move_file, safe_restore_file
from app.utils.constants import DUPLICATES_FOLDER_NAME
from app.utils.helpers import format_file_size

app = Flask(__name__)
CORS(app)

# Initialize Real Python Backend Engines
config_service = ConfigService()
file_classifier = FileClassifier(config_service)
undo_manager = UndoManager()
duplicate_detector = DuplicateDetector()
stats_service = StatsService(undo_manager)
organizer_engine = OrganizerEngine(
    config_service=config_service,
    file_classifier=file_classifier,
    undo_manager=undo_manager,
    duplicate_detector=duplicate_detector
)

# In-memory storage for active dry run session
current_dry_run_session: dict = {}

@app.route("/api/user-info", methods=["GET", "POST"])
def get_user_info():
    """Return logged-in Windows account user display name & initials dynamically."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        new_name = data.get("name", "").strip()
        if new_name:
            config_service.set("user_display_name", new_name)

    stored_name = config_service.get("user_display_name", "")
    if not stored_name:
        try:
            import ctypes, getpass
            buf = ctypes.create_unicode_buffer(100)
            buf_size = ctypes.c_ulong(100)
            if ctypes.windll.secur32.GetUserNameExW(3, buf, ctypes.byref(buf_size)) and buf.value:
                stored_name = buf.value.strip()
            else:
                stored_name = getpass.getuser().capitalize()
        except Exception:
            import getpass
            stored_name = getpass.getuser().capitalize()

    parts = stored_name.split()
    initials = (parts[0][0] + (parts[1][0] if len(parts) > 1 else (parts[0][1] if len(parts[0]) > 1 else ''))).upper() if parts else "US"
    return jsonify({"name": stored_name, "initials": initials})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Return real dashboard statistics from user system activity."""
    stats = stats_service.get_dashboard_stats()
    return jsonify({
        "total_files_organized": stats.total_files_organized,
        "total_runs": stats.total_runs,
        "duplicates_found": stats.total_duplicates_found,
        "category_breakdown": stats.category_breakdown,
        "categories_count": len(config_service.get_all_categories())
    })

@app.route("/api/scan", methods=["POST"])
def scan_directory():
    """Real folder scan & dry run preview generation with Smart, Date, or Category arrange modes."""
    data = request.get_json(silent=True) or {}
    folder_str = data.get("folder", "").strip()
    recursive = data.get("recursive", False)
    check_duplicates = data.get("check_duplicates", True)
    arrange_mode = data.get("arrange_mode", "standard")

    if not folder_str:
        return jsonify({"error": "No folder path provided"}), 400

    target_path = Path(folder_str)
    if not target_path.exists() or not target_path.is_dir():
        return jsonify({"error": f"Directory '{folder_str}' does not exist."}), 400

    # Protected system directory validation
    from app.core.file_operations import is_protected_path
    if is_protected_path(str(target_path)):
        return jsonify({"error": "Protected system directory! Cannot organize Windows system folders (e.g. C:\\Windows, C:\\Program Files) to prevent OS instability."}), 400

    try:
        result: DryRunResult = organizer_engine.scan_and_preview(
            folder_input=target_path,
            recursive=recursive,
            check_duplicates=check_duplicates
        )
        
        # Adjust target paths based on arrange_mode (Smart Arrange, Date Arrange, etc.)
        items_payload = []
        for item in result.items:
            rel_target = str(item.safe_destination_path.relative_to(result.base_folder))
            
            if arrange_mode == "date":
                try:
                    mtime = item.source_path.stat().st_mtime
                    dt = datetime.fromtimestamp(mtime)
                    rel_target = f"{dt.year}/{dt.strftime('%B')}/{item.source_path.name}"
                except Exception:
                    pass
            elif arrange_mode == "smart":
                cat = item.category.lower()
                ext = item.source_path.suffix.lower()
                if ext in ['.pdf']:
                    sub = "Documents/PDFs"
                elif ext in ['.doc', '.docx']:
                    sub = "Documents/Word"
                elif ext in ['.xls', '.xlsx', '.csv']:
                    sub = "Documents/Spreadsheets"
                elif ext in ['.ppt', '.pptx']:
                    sub = "Documents/Presentations"
                elif cat == 'images':
                    sub = "Images"
                elif cat == 'videos':
                    sub = "Videos"
                elif cat == 'audio':
                    sub = "Audio"
                elif cat == 'archives':
                    sub = "Archives"
                elif cat == 'code':
                    sub = "Code"
                elif cat == 'executables':
                    sub = "Applications"
                else:
                    sub = "Others"
                rel_target = f"{sub}/{item.source_path.name}"

            items_payload.append({
                "source_path": str(item.source_path),
                "filename": item.source_path.name,
                "category": item.category,
                "target_path": rel_target,
                "size": format_file_size(item.file_size),
                "is_collision": item.is_collision,
                "is_duplicate": item.is_duplicate,
                "warning": "⚠️ Renaming collision" if item.is_collision else ("⚠️ Duplicate copy" if item.is_duplicate else "OK")
            })

        current_dry_run_session["result"] = result

        return jsonify({
            "base_folder": str(result.base_folder),
            "total_files": result.total_files,
            "total_size": format_file_size(result.total_size_bytes),
            "items": items_payload
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/organize", methods=["POST"])
def execute_organize():
    """Execute real file moves on actual disk files."""
    if "result" not in current_dry_run_session:
        return jsonify({"error": "No active dry run scan found. Please run scan first."}), 400

    try:
        dry_run_result = current_dry_run_session["result"]
        exec_result = organizer_engine.execute_organization(dry_run_result)
        current_dry_run_session.clear()

        return jsonify({
            "batch_id": exec_result.batch_id,
            "total_successful": exec_result.total_successful,
            "total_failed": exec_result.total_failed,
            "bytes_moved": format_file_size(exec_result.total_bytes_moved)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/duplicates", methods=["POST"])
def scan_duplicates():
    """Perform real SHA-256 duplicate detection over directory."""
    data = request.get_json(silent=True) or {}
    folder_str = data.get("folder", "").strip()
    if not folder_str or not Path(folder_str).exists():
        return jsonify({"error": "Invalid directory path"}), 400

    target_dir = Path(folder_str)
    try:
        dup_result = duplicate_detector.find_duplicates(target_dir, recursive=True)
        
        groups_payload = []
        for grp in dup_result.groups:
            groups_payload.append({
                "hash": grp.sha256_hash,
                "size": format_file_size(grp.file_size),
                "original": str(grp.original_file),
                "copies": [str(c) for c in grp.duplicate_files]
            })

        return jsonify({
            "total_scanned": dup_result.total_files_scanned,
            "duplicate_count": dup_result.duplicate_files_count,
            "group_count": len(dup_result.groups),
            "wasted_space": format_file_size(dup_result.total_wasted_bytes),
            "groups": groups_payload
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/quarantine", methods=["POST"])
def quarantine_duplicates():
    """Safe-move duplicate files into a Duplicates folder."""
    data = request.get_json(silent=True) or {}
    folder_str = data.get("folder", "").strip()
    if not folder_str or not Path(folder_str).exists():
        return jsonify({"error": "Invalid directory path"}), 400

    target_dir = Path(folder_str)
    dup_result = duplicate_detector.find_duplicates(target_dir, recursive=True)
    dest_dir = target_dir / DUPLICATES_FOLDER_NAME

    moved_count = 0
    for grp in dup_result.groups:
        for dup in grp.duplicate_files:
            if dup.exists():
                res = safe_move_file(dup, dest_dir)
                if res.success:
                    moved_count += 1

    return jsonify({"moved_count": moved_count, "quarantine_folder": str(dest_dir)})

@app.route("/api/history", methods=["GET"])
def get_history():
    """Return real batch journal history from history.json."""
    from dataclasses import asdict
    batches = undo_manager.get_history()
    payload = []
    for b in batches:
        payload.append({
            "id": b.batch_id,
            "timestamp": b.timestamp,
            "total_moves": len(b.moves),
            "moves": [asdict(m) for m in b.moves]
        })
    return jsonify(payload)

@app.route("/api/undo", methods=["POST"])
def undo_batch():
    """Perform real 1-click restore of an organized batch."""
    data = request.get_json(silent=True) or {}
    batch_id = data.get("batch_id")
    if not batch_id:
        return jsonify({"error": "Missing batch_id"}), 400

    try:
        success, msg, results = undo_manager.undo_batch(batch_id)
        restored_count = sum(1 for r in results if r.success)
        failed_count = sum(1 for r in results if not r.success)
        return jsonify({
            "batch_id": batch_id,
            "restored_count": restored_count,
            "failed_count": failed_count,
            "message": msg
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/rules", methods=["GET", "POST"])
def manage_rules():
    """Get or add custom extension classification rules."""
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        cat_name = data.get("category")
        extensions = data.get("extensions", [])
        if cat_name and extensions:
            config_service.add_custom_rule(cat_name, extensions)
            file_classifier.reload_rules()

    all_cats = config_service.get_all_categories()
    payload = []
    for name, data in all_cats.items():
        payload.append({
            "name": name,
            "folder": data.get("folder", name),
            "extensions": data.get("extensions", [])
        })
    return jsonify(payload)

@app.route("/api/rename", methods=["POST"])
def bulk_rename():
    """Execute real bulk file renames on disk files."""
    data = request.get_json(silent=True) or {}
    folder_str = data.get("folder", "").strip()
    prefix = data.get("prefix", "")
    suffix = data.get("suffix", "")
    search_pat = data.get("search", "")
    replace_pat = data.get("replace", "")

    if not folder_str or not Path(folder_str).exists():
        return jsonify({"error": "Invalid directory path"}), 400

    target_dir = Path(folder_str)
    renamed_count = 0

    for file_path in target_dir.iterdir():
        if file_path.is_file():
            stem = file_path.stem
            ext = file_path.suffix
            if search_pat:
                stem = stem.replace(search_pat, replace_pat)
            new_name = f"{prefix}{stem}{suffix}{ext}"
            new_path = file_path.parent / new_name
            if new_path != file_path and not new_path.exists():
                file_path.rename(new_path)
                renamed_count += 1

    return jsonify({"renamed_count": renamed_count})

@app.route("/api/select-folder", methods=["POST", "GET"])
def select_folder():
    """Trigger native Windows folder picker dialog instantly and reliably without freezing."""
    try:
        data = request.get_json(silent=True) or {}
        initial = data.get("initial", "") if isinstance(data, dict) else ""
        if not initial and request.args.get("initial"):
            initial = request.args.get("initial")
            
        if not initial or not os.path.exists(initial):
            initial = str(Path.home() / "Downloads")

        # Method 1: Win32 COM Shell.Application with pythoncom CoInitialize (Guaranteed 100% Reliable & Fast)
        try:
            import pythoncom
            import win32com.client
            pythoncom.CoInitialize()
            shell = win32com.client.Dispatch("Shell.Application")
            folder = shell.BrowseForFolder(0, "Select Directory to Organize - SORTIFY", 0, initial)
            pythoncom.CoUninitialize()
            if folder:
                folder_path = folder.Self.Path
                if folder_path and os.path.exists(folder_path):
                    return jsonify({"folder": folder_path, "cancelled": False})
        except Exception:
            pass

        # Method 2: Native PowerShell System.Windows.Forms.FolderBrowserDialog
        try:
            import subprocess
            ps_cmd = f'[System.Reflection.Assembly]::LoadWithPartialName("System.windows.forms") | Out-Null; $f = New-Object System.Windows.Forms.FolderBrowserDialog; $f.SelectedPath = "{initial}"; if ($f.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {{ Write-Host $f.SelectedPath }}'
            proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, timeout=10)
            selected = proc.stdout.strip()
            if selected and os.path.exists(selected):
                return jsonify({"folder": selected, "cancelled": False})
        except Exception:
            pass

        # Method 3: PyWebView window dialog (Instant)
        try:
            import webview
            if webview.windows and len(webview.windows) > 0:
                res = webview.windows[0].create_file_dialog(
                    webview.FileDialog.FOLDER,
                    directory=initial
                )
                if res and len(res) > 0:
                    return jsonify({"folder": res[0], "cancelled": False})
                return jsonify({"folder": "", "cancelled": True})
        except Exception:
            pass

        return jsonify({"folder": "", "cancelled": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/default-folders", methods=["GET"])
def get_default_folders():
    """Get standard system directories on user's Windows machine."""
    from app.utils.constants import get_user_app_dir
    
    user_home = Path.home()
    user_profile = os.environ.get("USERPROFILE")
    if user_profile and "system32" not in user_profile.lower() and os.path.exists(user_profile):
        user_home = Path(user_profile)
    elif "system32" in str(user_home).lower():
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            user_home = Path(local_app_data).parent.parent

    folders = {
        "downloads": str(user_home / "Downloads"),
        "desktop": str(user_home / "Desktop"),
        "documents": str(user_home / "Documents"),
        "pictures": str(user_home / "Pictures"),
        "videos": str(user_home / "Videos")
    }
    return jsonify(folders)

@app.route("/api/upload", methods=["POST"])
def upload_files():
    """Save an upload batch to its own folder for organization."""
    from app.utils.constants import get_user_app_dir
    if 'files' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    uploaded_files = request.files.getlist('files')
    target_dir = get_user_app_dir() / "uploads" / uuid4().hex
    target_dir.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    for file in uploaded_files:
        if file.filename:
            filename = secure_filename(file.filename)
            if not filename:
                continue
            save_path = target_dir / filename
            file.save(save_path)
            saved_paths.append(str(save_path))

    return jsonify({
        "saved_count": len(saved_paths),
        "target_directory": str(target_dir),
        "files": [Path(p).name for p in saved_paths]
    })

@app.route("/api/files/list", methods=["POST", "GET"])
def list_files():
    """List directory items with metadata (size, mod_time, is_dir, is_hidden, extension) for Files manager view."""
    try:
        data = request.get_json(silent=True) or {}
        folder_str = data.get("folder", "").strip() or request.args.get("folder", "").strip()
        if not folder_str or not os.path.exists(folder_str):
            folder_str = str(Path.home() / "Downloads")

        target_path = Path(folder_str)
        from app.core.file_operations import is_hidden_path, is_protected_path

        items = []
        for p in target_path.iterdir():
            try:
                st = p.stat()
                is_dir = p.is_dir()
                size_bytes = 0 if is_dir else st.st_size
                mtime_dt = datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
                is_hid = is_hidden_path(str(p))
                
                cat = "folder" if is_dir else file_classifier.classify_file(p)
                
                items.append({
                    "name": p.name,
                    "path": str(p),
                    "is_dir": is_dir,
                    "size": format_file_size(size_bytes),
                    "size_bytes": size_bytes,
                    "mtime": mtime_dt,
                    "is_hidden": is_hid,
                    "ext": p.suffix.lower() if not is_dir else "",
                    "category": cat
                })
            except Exception:
                continue

        # Sort: directories first, then files alphabetically
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))

        return jsonify({
            "current_folder": str(target_path),
            "parent_folder": str(target_path.parent) if target_path.parent != target_path else str(target_path),
            "is_protected": is_protected_path(str(target_path)),
            "total_items": len(items),
            "items": items
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/files/action", methods=["POST"])
def execute_file_action():
    """Execute bulk file utility action (Recycle Bin, Zip, Extract, Hide, Unhide, Copy, Move, Rename)."""
    try:
        data = request.get_json(silent=True) or {}
        action = data.get("action", "").lower()  # 'recycle', 'hide', 'unhide', 'zip', 'extract', 'copy', 'move', 'rename'
        paths = data.get("paths", [])
        destination = data.get("destination", "").strip()
        password = data.get("password", "").strip() or None
        new_name = data.get("new_name", "").strip()

        from app.core.file_operations import (
            send_to_recycle_bin, 
            toggle_hide_attribute, 
            compress_to_zip, 
            extract_zip_archive,
            safe_copy_file,
            safe_move_file,
            is_protected_path
        )

        # Protection check
        for p in paths:
            if is_protected_path(p):
                return jsonify({"error": f"Cannot perform '{action}' on protected system path: {p}"}), 400

        successful_count = 0

        if action == "recycle":
            for p in paths:
                if send_to_recycle_bin(p):
                    successful_count += 1
            return jsonify({"message": f"Moved {successful_count} item(s) to Windows Recycle Bin.", "count": successful_count})

        elif action == "hide":
            for p in paths:
                if toggle_hide_attribute(p, hide=True):
                    successful_count += 1
            return jsonify({"message": f"Hidden {successful_count} item(s).", "count": successful_count})

        elif action == "unhide":
            for p in paths:
                if toggle_hide_attribute(p, hide=False):
                    successful_count += 1
            return jsonify({"message": f"Unhidden {successful_count} item(s).", "count": successful_count})

        elif action == "zip":
            output_zip = destination if destination.endswith(".zip") else f"{destination}.zip"
            if compress_to_zip(paths, output_zip, password=password):
                return jsonify({"message": f"Successfully created archive: {Path(output_zip).name}", "zip_path": output_zip})
            return jsonify({"error": "Failed to create ZIP archive."}), 500

        elif action == "extract":
            if paths and extract_zip_archive(paths[0], destination, password=password):
                return jsonify({"message": "ZIP archive extracted successfully.", "extracted_to": destination})
            return jsonify({"error": "Failed to extract ZIP archive. Verify password if encrypted."}), 500

        elif action == "copy" and destination:
            dest_dir = Path(destination)
            for p in paths:
                res = safe_copy_file(Path(p), dest_dir)
                if res.success:
                    successful_count += 1
            return jsonify({"message": f"Copied {successful_count} item(s) to {dest_dir.name}", "count": successful_count})

        elif action == "move" and destination:
            dest_dir = Path(destination)
            for p in paths:
                res = safe_move_file(Path(p), dest_dir)
                if res.success:
                    successful_count += 1
            return jsonify({"message": f"Moved {successful_count} item(s) to {dest_dir.name}", "count": successful_count})

        elif action == "rename" and paths and new_name:
            src = Path(paths[0])
            dest = src.parent / new_name
            if dest != src and not dest.exists():
                src.rename(dest)
                return jsonify({"message": f"Renamed to {new_name}", "new_path": str(dest)})
            return jsonify({"error": "Target filename already exists or unchanged."}), 400

        return jsonify({"error": "Invalid action or parameters."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/storage/analytics", methods=["POST", "GET"])
def storage_analytics():
    """Return disk space analytics, top 25 largest files, category sizes & wasted duplicate space."""
    try:
        data = request.get_json(silent=True) or {}
        folder_str = data.get("folder", "").strip() or request.args.get("folder", "").strip()
        if not folder_str or not os.path.exists(folder_str):
            folder_str = str(Path.home() / "Downloads")

        target_path = Path(folder_str)
        all_files = []
        cat_sizes = {}
        cat_counts = {}
        total_bytes = 0

        for root, _, files in os.walk(str(target_path)):
            for f in files:
                try:
                    fp = Path(root) / f
                    if fp.is_file():
                        sz = fp.stat().st_size
                        total_bytes += sz
                        cat = file_classifier.classify_file(fp)
                        cat_sizes[cat] = cat_sizes.get(cat, 0) + sz
                        cat_counts[cat] = cat_counts.get(cat, 0) + 1
                        all_files.append({
                            "name": fp.name,
                            "path": str(fp),
                            "size_bytes": sz,
                            "size": format_file_size(sz),
                            "category": cat
                        })
                except Exception:
                    continue

        # Top 25 Largest Files
        all_files.sort(key=lambda x: x["size_bytes"], reverse=True)
        top_25 = all_files[:25]

        # Category Breakdown
        cat_breakdown = []
        for cat_name, sz_b in cat_sizes.items():
            cat_breakdown.append({
                "category": cat_name,
                "size_bytes": sz_b,
                "size": format_file_size(sz_b),
                "count": cat_counts.get(cat_name, 0)
            })
        cat_breakdown.sort(key=lambda x: x["size_bytes"], reverse=True)

        return jsonify({
            "target_folder": str(target_path),
            "total_files": len(all_files),
            "total_size": format_file_size(total_bytes),
            "total_bytes": total_bytes,
            "top_largest_files": top_25,
            "categories": cat_breakdown
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

DIST_DIR = ROOT_DIR / "frontend" / "dist"

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if DIST_DIR.exists():
        target = DIST_DIR / path
        if path != "" and target.exists():
            return send_from_directory(DIST_DIR, path)
        return send_from_directory(DIST_DIR, "index.html")
    return jsonify({"status": "SORTIFY API Server Active."})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
