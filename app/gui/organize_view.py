"""Organize Files view with folder picker, dry run preview table, and execution controls."""
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from pathlib import Path
from typing import Callable, Optional
from app.core.organizer import OrganizerEngine, DryRunResult
from app.services.config_service import ConfigService
from app.utils.constants import (
    FONT_FAMILY,
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS,
    COLOR_DANGER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED
)
from app.utils.helpers import format_file_size

class OrganizeView(ctk.CTkFrame):
    """Scan and Organize workspace view."""

    def __init__(
        self,
        master,
        organizer_engine: OrganizerEngine,
        config_service: ConfigService,
        on_completed: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.engine = organizer_engine
        self.config_service = config_service
        self.on_completed = on_completed

        self.current_dry_run: Optional[DryRunResult] = None
        self._is_cancelled = False
        self._is_processing = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Header Title
        title_label = ctk.CTkLabel(
            self,
            text="📁 Organize Files & Triage Workspace",
            font=ctk.CTkFont(family=FONT_FAMILY, size=24, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        title_label.grid(row=0, column=0, padx=24, pady=(24, 4), sticky="w")

        subtitle_label = ctk.CTkLabel(
            self,
            text="Select a target directory to scan, preview categorical sorting, and safely execute organization.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13),
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        subtitle_label.grid(row=1, column=0, padx=24, pady=(0, 16), sticky="w")

        # Controls Container
        controls_frame = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_CARD_BORDER
        )
        controls_frame.grid(row=2, column=0, padx=24, pady=(0, 16), sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)

        # Folder Picker Row
        f_label = ctk.CTkLabel(
            controls_frame,
            text="Target Folder:",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        f_label.grid(row=0, column=0, padx=(16, 10), pady=(16, 10), sticky="w")

        self.folder_entry = ctk.CTkEntry(
            controls_frame,
            placeholder_text="Select a folder to scan...",
            height=38,
            corner_radius=10,
            fg_color=("#F1F5F9", "#151624"),
            border_color=COLOR_CARD_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12)
        )
        self.folder_entry.grid(row=0, column=1, padx=10, pady=(16, 10), sticky="ew")

        # Remember last selected folder setting
        last_folder = self.config_service.get("last_selected_folder", "")
        if last_folder and Path(last_folder).exists():
            self.folder_entry.insert(0, last_folder)

        browse_btn = ctk.CTkButton(
            controls_frame,
            text="Browse Folder",
            width=130,
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            command=self._handle_browse
        )
        browse_btn.grid(row=0, column=2, padx=(10, 16), pady=(16, 10))

        # Options Toggles
        toggles_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        toggles_frame.grid(row=1, column=0, columnspan=3, padx=16, pady=(0, 14), sticky="w")

        self.recursive_var = ctk.BooleanVar(value=self.config_service.get("include_subfolders", False))
        self.recursive_chk = ctk.CTkCheckBox(
            toggles_frame,
            text="Include Subfolders (Recursive)",
            variable=self.recursive_var,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_PRIMARY
        )
        self.recursive_chk.pack(side="left", padx=(0, 20))

        self.dup_var = ctk.BooleanVar(value=True)
        self.dup_chk = ctk.CTkCheckBox(
            toggles_frame,
            text="Check Duplicates during scan",
            variable=self.dup_var,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_PRIMARY
        )
        self.dup_chk.pack(side="left")

        # Action buttons
        btn_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=3, padx=16, pady=(0, 16), sticky="ew")

        self.scan_btn = ctk.CTkButton(
            btn_frame,
            text="🔍 Scan & Preview",
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            fg_color=COLOR_SUCCESS,
            hover_color="#059669",
            command=self._handle_start_scan
        )
        self.scan_btn.pack(side="left", padx=(0, 10))

        self.organize_btn = ctk.CTkButton(
            btn_frame,
            text="⚡ Organize Files Now",
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            state="disabled",
            command=self._handle_execute_organize
        )
        self.organize_btn.pack(side="left", padx=(0, 10))

        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌ Cancel",
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            fg_color=COLOR_DANGER,
            hover_color="#B91C1C",
            state="disabled",
            command=self._handle_cancel
        )
        self.cancel_btn.pack(side="left")

        # Progress bar & status
        self.status_label = ctk.CTkLabel(
            btn_frame,
            text="Ready to scan",
            text_color=COLOR_TEXT_MUTED,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12)
        )
        self.status_label.pack(side="right", padx=10)

        self.pbar = ctk.CTkProgressBar(controls_frame, height=6, corner_radius=3, progress_color=COLOR_PRIMARY)
        self.pbar.grid(row=3, column=0, columnspan=3, padx=16, pady=(0, 12), sticky="ew")
        self.pbar.set(0.0)

        # Dry Run Treeview Table Container
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

        style = ttk.Style()
        style.theme_use("default")
        # Configure adaptive table styling
        mode = ctk.get_appearance_mode()
        bg_col = "#FFFFFF" if mode == "Light" else "#151624"
        fg_col = "#0F172A" if mode == "Light" else "#F8FAFC"
        hdr_bg = "#F1F5F9" if mode == "Light" else "#1D1E30"
        hdr_fg = "#475569" if mode == "Light" else "#94A3B8"

        style.configure(
            "Treeview",
            background=bg_col,
            foreground=fg_col,
            rowheight=30,
            fieldbackground=bg_col,
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background=hdr_bg,
            foreground=hdr_fg,
            font=("Raleway", 10, "bold"),
            borderwidth=0
        )
        style.map("Treeview", background=[("selected", "#6366F1")])

        columns = ("filename", "category", "target_path", "size", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

        self.tree.heading("filename", text="Filename")
        self.tree.heading("category", text="Category")
        self.tree.heading("target_path", text="Destination Path")
        self.tree.heading("size", text="File Size")
        self.tree.heading("status", text="Collision Warning")

        self.tree.column("filename", width=200)
        self.tree.column("category", width=120)
        self.tree.column("target_path", width=350)
        self.tree.column("size", width=100, anchor="e")
        self.tree.column("status", width=150)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(12, 0), pady=12)
        vsb.grid(row=0, column=1, sticky="ns", padx=(0, 12), pady=12)

    def _handle_browse(self):
        folder = filedialog.askdirectory(title="Select Folder to Organize")
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)
            self.config_service.set("last_selected_folder", folder)

    def _handle_cancel(self):
        self._is_cancelled = True
        self.status_label.configure(text="Cancelling operation...")

    def _update_progress(self, current: int, total: int, msg: str):
        def _gui():
            pct = current / float(total) if total > 0 else 0
            self.pbar.set(pct)
            self.status_label.configure(text=msg)
        self.after(0, _gui)

    def _handle_start_scan(self):
        folder_str = self.folder_entry.get().strip()
        if not folder_str:
            messagebox.showwarning("No Folder Selected", "Please select a valid directory path to scan.")
            return

        target_path = Path(folder_str)
        if not target_path.exists() or not target_path.is_dir():
            messagebox.showerror("Invalid Directory", f"The directory '{folder_str}' does not exist.")
            return

        self.config_service.set("last_selected_folder", folder_str)
        self.config_service.set("include_subfolders", self.recursive_var.get())

        self._is_cancelled = False
        self._is_processing = True
        self.scan_btn.configure(state="disabled")
        self.organize_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.pbar.set(0.0)

        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        def worker():
            try:
                res = self.engine.scan_and_preview(
                    folder_input=target_path,
                    recursive=self.recursive_var.get(),
                    check_duplicates=self.dup_var.get(),
                    progress_callback=self._update_progress,
                    cancel_checker=lambda: self._is_cancelled
                )
                self.after(0, lambda: self._on_scan_completed(res))
            except Exception as e:
                self.after(0, lambda: self._on_scan_failed(str(e)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_scan_completed(self, result: DryRunResult):
        self.current_dry_run = result
        self._is_processing = False
        self.scan_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")

        if self._is_cancelled:
            self.status_label.configure(text="Scan cancelled by user.")
            return

        self.pbar.set(1.0)
        self.status_label.configure(text=f"Scan complete: {result.total_files} files ready to organize ({format_file_size(result.total_size_bytes)}).")

        # Populate tree
        for item in result.items:
            collision_str = "⚠️ Renaming collision" if item.is_collision else "OK"
            if item.is_duplicate:
                collision_str += " (Duplicate)"

            rel_target = item.safe_destination_path.relative_to(result.base_folder)
            self.tree.insert(
                "",
                "end",
                values=(
                    item.source_path.name,
                    item.category,
                    str(rel_target),
                    format_file_size(item.file_size),
                    collision_str
                )
            )

        if result.total_files > 0:
            self.organize_btn.configure(state="normal")
        else:
            self.organize_btn.configure(state="disabled")
            messagebox.showinfo("No Files Found", "No unorganized files matching categories were found in target folder.")

    def _on_scan_failed(self, err_msg: str):
        self._is_processing = False
        self.scan_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.status_label.configure(text="Scan failed.")
        messagebox.showerror("Scan Error", f"An error occurred during directory scan:\n{err_msg}")

    def _handle_execute_organize(self):
        if not self.current_dry_run or not self.current_dry_run.items:
            return

        if self.config_service.get("confirm_before_organizing", True):
            confirm = messagebox.askyesno(
                "Confirm Organization",
                f"Are you sure you want to organize {self.current_dry_run.total_files} files into category subfolders?\n\nYou can undo this action at any time from the Activity History tab."
            )
            if not confirm:
                return

        self._is_cancelled = False
        self._is_processing = True
        self.scan_btn.configure(state="disabled")
        self.organize_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")

        def worker():
            res = self.engine.execute_organization(
                dry_run_result=self.current_dry_run,
                progress_callback=self._update_progress,
                cancel_checker=lambda: self._is_cancelled
            )
            self.after(0, lambda: self._on_organize_completed(res))

        threading.Thread(target=worker, daemon=True).start()

    def _on_organize_completed(self, result):
        self._is_processing = False
        self.scan_btn.configure(state="normal")
        self.cancel_btn.configure(state="disabled")
        self.organize_btn.configure(state="disabled")
        self.pbar.set(1.0)
        self.status_label.configure(text=f"Batch {result.batch_id} complete! Organized {result.total_successful} files.")

        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        messagebox.showinfo(
            "Organization Complete",
            f"Successfully organized {result.total_successful} files ({format_file_size(result.total_bytes_moved)})!\n\nBatch ID: {result.batch_id}"
        )

        if self.on_completed:
            self.on_completed()
