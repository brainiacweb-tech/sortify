"""Duplicates view for inspecting identical SHA-256 files and safe quarantine handling."""
import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from pathlib import Path
from typing import Optional
from app.core.duplicate_detector import DuplicateDetector, DuplicateDetectionResult
from app.core.file_operations import safe_move_file
from app.utils.constants import (
    FONT_FAMILY,
    DUPLICATES_FOLDER_NAME,
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS,
    COLOR_WARNING,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED
)
from app.utils.helpers import format_file_size

class DuplicatesView(ctk.CTkFrame):
    """Duplicate file inspector view."""

    def __init__(self, master, duplicate_detector: DuplicateDetector, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.detector = duplicate_detector

        self.current_result: Optional[DuplicateDetectionResult] = None
        self._is_cancelled = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Header Title
        title_label = ctk.CTkLabel(
            self,
            text="🔍 Cryptographic Duplicate Finder",
            font=ctk.CTkFont(family=FONT_FAMILY, size=24, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        title_label.grid(row=0, column=0, padx=24, pady=(24, 4), sticky="w")

        subtitle_label = ctk.CTkLabel(
            self,
            text="Identify exact duplicate files using SHA-256 hashing and safely quarantine them.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        subtitle_label.grid(row=1, column=0, padx=24, pady=(0, 16), sticky="w")

        # Control Bar
        ctrl_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_CARD_BORDER
        )
        ctrl_frame.grid(row=2, column=0, padx=24, pady=(0, 16), sticky="ew")
        ctrl_frame.grid_columnconfigure(1, weight=1)

        f_label = ctk.CTkLabel(
            ctrl_frame,
            text="Scan Directory:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        f_label.grid(row=0, column=0, padx=(16, 10), pady=16, sticky="w")

        self.folder_entry = ctk.CTkEntry(
            ctrl_frame,
            placeholder_text="Select directory to scan for duplicate files...",
            height=38,
            corner_radius=10,
            fg_color=("#F1F5F9", "#151624"),
            border_color=COLOR_CARD_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12)
        )
        self.folder_entry.grid(row=0, column=1, padx=10, pady=16, sticky="ew")

        browse_btn = ctk.CTkButton(
            ctrl_frame,
            text="Browse Folder",
            width=130,
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            command=self._handle_browse
        )
        browse_btn.grid(row=0, column=2, padx=(10, 10), pady=16)

        self.scan_btn = ctk.CTkButton(
            ctrl_frame,
            text="🔍 Detect Duplicates",
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            fg_color=COLOR_SUCCESS,
            hover_color="#059669",
            command=self._handle_start_scan
        )
        self.scan_btn.grid(row=0, column=3, padx=(0, 16), pady=16)

        # Actions & Results bar
        act_frame = ctk.CTkFrame(ctrl_frame, fg_color="transparent")
        act_frame.grid(row=1, column=0, columnspan=4, padx=16, pady=(0, 16), sticky="ew")

        self.quarantine_btn = ctk.CTkButton(
            act_frame,
            text="🛡️ Quarantine Duplicates to 'Duplicates/'",
            fg_color=COLOR_WARNING,
            hover_color="#B45309",
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            state="disabled",
            command=self._handle_quarantine
        )
        self.quarantine_btn.pack(side="left", padx=(0, 10))

        self.open_btn = ctk.CTkButton(
            act_frame,
            text="📂 Open File Location",
            fg_color=("#CBD5E1", "#374151"),
            hover_color=("#94A3B8", "#4B5563"),
            text_color=COLOR_TEXT_PRIMARY,
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            state="disabled",
            command=self._handle_open_location
        )
        self.open_btn.pack(side="left")

        self.summary_lbl = ctk.CTkLabel(
            act_frame,
            text="Scan a directory to inspect duplicate groups.",
            text_color=COLOR_TEXT_MUTED,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12)
        )
        self.summary_lbl.pack(side="right", padx=10)

        # Table area
        table_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_CARD_BORDER
        )
        table_frame.grid(row=3, column=0, padx=24, pady=(0, 24), sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        columns = ("type", "filename", "size", "hash", "path")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

        self.tree.heading("type", text="Role")
        self.tree.heading("filename", text="Filename")
        self.tree.heading("size", text="Size")
        self.tree.heading("hash", text="SHA-256 Hash")
        self.tree.heading("path", text="Full Path")

        self.tree.column("type", width=120)
        self.tree.column("filename", width=200)
        self.tree.column("size", width=100, anchor="e")
        self.tree.column("hash", width=160)
        self.tree.column("path", width=400)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(12, 0), pady=12)
        vsb.grid(row=0, column=1, sticky="ns", padx=(0, 12), pady=12)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _handle_browse(self):
        folder = filedialog.askdirectory(title="Select Folder for Duplicate Detection")
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)

    def _handle_start_scan(self):
        folder_str = self.folder_entry.get().strip()
        if not folder_str or not Path(folder_str).exists():
            messagebox.showwarning("Invalid Path", "Please select an existing directory.")
            return

        self.scan_btn.configure(state="disabled")
        self.quarantine_btn.configure(state="disabled")
        self.summary_lbl.configure(text="Scanning and computing SHA-256 hashes...")

        for item in self.tree.get_children():
            self.tree.delete(item)

        target_dir = Path(folder_str)

        def worker():
            res = self.detector.find_duplicates(target_dir, recursive=True)
            self.after(0, lambda: self._on_scan_done(target_dir, res))

        threading.Thread(target=worker, daemon=True).start()

    def _on_scan_done(self, base_folder: Path, res: DuplicateDetectionResult):
        self.current_result = res
        self.scan_btn.configure(state="normal")

        if not res.groups:
            self.summary_lbl.configure(text=f"Scan complete: Scanned {res.total_files_scanned} files. No duplicates found!")
            messagebox.showinfo("No Duplicates", "No duplicate files were found in target folder.")
            return

        self.summary_lbl.configure(
            text=f"Found {res.duplicate_files_count} duplicate copies across {len(res.groups)} groups ({format_file_size(res.total_wasted_bytes)} wasted space)."
        )
        self.quarantine_btn.configure(state="normal")

        for grp in res.groups:
            hash_snippet = grp.sha256_hash[:12] + "..."
            size_str = format_file_size(grp.file_size)

            # Insert original file
            self.tree.insert("", "end", values=("Original File", grp.original_file.name, size_str, hash_snippet, str(grp.original_file)))

            # Insert duplicate copies
            for dup in grp.duplicate_files:
                self.tree.insert("", "end", values=("Duplicate Copy", dup.name, size_str, hash_snippet, str(dup)))

    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.open_btn.configure(state="normal")
        else:
            self.open_btn.configure(state="disabled")

    def _handle_open_location(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        file_path = Path(item["values"][4])

        if file_path.exists():
            if sys.platform == "win32":
                subprocess.run(["explorer", "/select,", str(file_path)])
            elif sys.platform == "darwin":
                subprocess.run(["open", "-R", str(file_path)])
            else:
                subprocess.run(["xdg-open", str(file_path.parent)])

    def _handle_quarantine(self):
        if not self.current_result or not self.current_result.groups:
            return

        folder_str = self.folder_entry.get().strip()
        base_dir = Path(folder_str)
        dest_dir = base_dir / DUPLICATES_FOLDER_NAME

        confirm = messagebox.askyesno(
            "Confirm Quarantine",
            f"Move {self.current_result.duplicate_files_count} duplicate files into '{DUPLICATES_FOLDER_NAME}' folder?\n\nNo files will be permanently deleted."
        )
        if not confirm:
            return

        moved_count = 0
        for grp in self.current_result.groups:
            for dup in grp.duplicate_files:
                if dup.exists():
                    res = safe_move_file(dup, dest_dir)
                    if res.success:
                        moved_count += 1

        messagebox.showinfo("Quarantine Complete", f"Successfully moved {moved_count} duplicate files into '{dest_dir.name}'.")
        self._handle_start_scan()
