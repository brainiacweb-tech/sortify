"""History view for reviewing organization activity logs and executing single-click undos."""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from pathlib import Path
from typing import Callable, Optional
from app.core.undo_manager import UndoManager, BatchRecord

class HistoryView(ctk.CTkFrame):
    """Activity history journal and reverse undo manager view."""

    def __init__(self, master, undo_manager: UndoManager, on_undo_completed: Optional[Callable[[], None]] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.undo_manager = undo_manager
        self.on_undo_completed = on_undo_completed

        self.selected_batch: Optional[BatchRecord] = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header Title
        title_label = ctk.CTkLabel(self, text="📜 Activity History & Undo Journal", font=ctk.CTkFont(size=24, weight="bold"), anchor="w")
        title_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        subtitle_label = ctk.CTkLabel(self, text="Audit every past organization run and safely reverse file moves with 100% precision.", font=ctk.CTkFont(size=13), text_color="#8E9AAF", anchor="w")
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Main Container split: Batches List (Left) and Move Details Table (Right)
        main_split = ctk.CTkFrame(self, fg_color="transparent")
        main_split.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        main_split.grid_columnconfigure(0, weight=1)
        main_split.grid_columnconfigure(1, weight=2)
        main_split.grid_rowconfigure(0, weight=1)

        # Left Panel: Batches List
        batches_box = ctk.CTkFrame(main_split, fg_color="#1E293B", corner_radius=12)
        batches_box.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")
        batches_box.grid_columnconfigure(0, weight=1)
        batches_box.grid_rowconfigure(1, weight=1)

        b_hdr = ctk.CTkFrame(batches_box, fg_color="transparent")
        b_hdr.grid(row=0, column=0, padx=15, pady=12, sticky="ew")

        b_title = ctk.CTkLabel(b_hdr, text="Past Organization Runs", font=ctk.CTkFont(size=15, weight="bold"))
        b_title.pack(side="left")

        self.undo_btn = ctk.CTkButton(b_hdr, text="↩️ Undo Batch", width=110, height=30, fg_color="#DC2626", hover_color="#B91C1C", state="disabled", command=self._handle_undo_click)
        self.undo_btn.pack(side="right")

        self.batches_scroll = ctk.CTkScrollableFrame(batches_box, fg_color="transparent")
        self.batches_scroll.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Right Panel: Move Operations Detail Table
        details_box = ctk.CTkFrame(main_split, fg_color="#1E293B", corner_radius=12)
        details_box.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="nsew")
        details_box.grid_columnconfigure(0, weight=1)
        details_box.grid_rowconfigure(1, weight=1)

        d_title = ctk.CTkLabel(details_box, text="File Move Details", font=ctk.CTkFont(size=15, weight="bold"))
        d_title.grid(row=0, column=0, padx=15, pady=12, sticky="w")

        columns = ("source", "destination", "category", "status")
        self.tree = ttk.Treeview(details_box, columns=columns, show="headings")

        self.tree.heading("source", text="Original Source Path")
        self.tree.heading("destination", text="Organized Destination Path")
        self.tree.heading("category", text="Category")
        self.tree.heading("status", text="Status")

        self.tree.column("source", width=250)
        self.tree.column("destination", width=250)
        self.tree.column("category", width=100)
        self.tree.column("status", width=100)

        vsb = ttk.Scrollbar(details_box, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=(0, 10))
        vsb.grid(row=1, column=1, sticky="ns", padx=(0, 10), pady=(0, 10))

        self.refresh_history()

    def refresh_history(self):
        """Reload history journal and rebuild batch list widgets."""
        for child in self.batches_scroll.winfo_children():
            child.destroy()

        for item in self.tree.get_children():
            self.tree.delete(item)

        batches = self.undo_manager.get_history()

        if not batches:
            empty_lbl = ctk.CTkLabel(self.batches_scroll, text="No organization runs logged yet.", text_color="#A0AAB8")
            empty_lbl.pack(pady=20)
            self.undo_btn.configure(state="disabled")
            return

        for batch in batches:
            card = ctk.CTkFrame(self.batches_scroll, fg_color="#0F172A", corner_radius=8)
            card.pack(fill="x", pady=5)
            card.grid_columnconfigure(0, weight=1)

            status_text = "UNDONE" if batch.undone else "ACTIVE"
            status_color = "#64748B" if batch.undone else "#10B981"

            lbl_time = ctk.CTkLabel(card, text=f"📅 {batch.timestamp}", font=ctk.CTkFont(size=12, weight="bold"))
            lbl_time.grid(row=0, column=0, padx=10, pady=(8, 2), sticky="w")

            lbl_status = ctk.CTkLabel(card, text=status_text, font=ctk.CTkFont(size=11, weight="bold"), text_color=status_color)
            lbl_status.grid(row=0, column=1, padx=10, pady=(8, 2), sticky="e")

            lbl_info = ctk.CTkLabel(card, text=f"{len(batch.moves)} files • {Path(batch.base_folder).name}", font=ctk.CTkFont(size=11), text_color="#94A3B8")
            lbl_info.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 8), sticky="w")

            # Bind click event
            card.bind("<Button-1>", lambda e, b=batch: self._select_batch(b))
            lbl_time.bind("<Button-1>", lambda e, b=batch: self._select_batch(b))
            lbl_info.bind("<Button-1>", lambda e, b=batch: self._select_batch(b))

    def _select_batch(self, batch: BatchRecord):
        self.selected_batch = batch
        for item in self.tree.get_children():
            self.tree.delete(item)

        for m in batch.moves:
            src_p = Path(m.source).name
            dest_p = Path(m.destination).name
            st = "Restored" if m.restored else m.status
            self.tree.insert("", "end", values=(src_p, dest_p, m.original_category, st))

        if not batch.undone and batch.moves:
            self.undo_btn.configure(state="normal")
        else:
            self.undo_btn.configure(state="disabled")

    def _handle_undo_click(self):
        if not self.selected_batch or self.selected_batch.undone:
            return

        confirm = messagebox.askyesno(
            "Confirm Undo",
            f"Are you sure you want to undo organization batch {self.selected_batch.batch_id}?\n\nThis will move {len(self.selected_batch.moves)} files back to their original locations."
        )
        if not confirm:
            return

        success, msg, results = self.undo_manager.undo_batch(self.selected_batch.batch_id)
        if success:
            messagebox.showinfo("Undo Successful", msg)
        else:
            messagebox.showerror("Undo Failed", msg)

        self.refresh_history()
        if self.on_undo_completed:
            self.on_undo_completed()
