"""Custom classification rules and category extension manager view."""
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from app.services.config_service import ConfigService

class RulesView(ctk.CTkFrame):
    """Category classification rules configuration view."""

    def __init__(self, master, config_service: ConfigService, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.config_service = config_service

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Header Title
        title_label = ctk.CTkLabel(self, text="⚙️ Classification Rules", font=ctk.CTkFont(size=24, weight="bold"), anchor="w")
        title_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        subtitle_label = ctk.CTkLabel(self, text="Customize extension mappings and target subfolders for automatic triage.", font=ctk.CTkFont(size=13), text_color="#8E9AAF", anchor="w")
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Add Custom Rule Form Box
        form_box = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=12)
        form_box.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        form_box.grid_columnconfigure((0, 1, 2), weight=1)

        f_title = ctk.CTkLabel(form_box, text="Add / Modify Rule", font=ctk.CTkFont(size=15, weight="bold"))
        f_title.grid(row=0, column=0, columnspan=3, padx=15, pady=(12, 10), sticky="w")

        self.cat_entry = ctk.CTkEntry(form_box, placeholder_text="Category Name (e.g., EBooks)", height=35)
        self.cat_entry.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")

        self.ext_entry = ctk.CTkEntry(form_box, placeholder_text="Extensions (e.g., epub, mobi, pdf)", height=35)
        self.ext_entry.grid(row=1, column=1, padx=10, pady=(0, 15), sticky="ew")

        self.folder_entry = ctk.CTkEntry(form_box, placeholder_text="Target Folder (Optional)", height=35)
        self.folder_entry.grid(row=1, column=2, padx=(10, 15), pady=(0, 15), sticky="ew")

        btn_row = ctk.CTkFrame(form_box, fg_color="transparent")
        btn_row.grid(row=2, column=0, columnspan=3, padx=15, pady=(0, 15), sticky="w")

        save_btn = ctk.CTkButton(btn_row, text="💾 Save Custom Rule", fg_color="#2563EB", hover_color="#1D4ED8", command=self._handle_save_rule)
        save_btn.pack(side="left", padx=(0, 10))

        reset_btn = ctk.CTkButton(btn_row, text="🔄 Reset Rules to Default", fg_color="#4B5563", hover_color="#374151", command=self._handle_reset_rules)
        reset_btn.pack(side="left")

        # Category Rules List Box
        rules_box = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=12)
        rules_box.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")
        rules_box.grid_columnconfigure(0, weight=1)
        rules_box.grid_rowconfigure(1, weight=1)

        r_title = ctk.CTkLabel(rules_box, text="Active Category Mappings", font=ctk.CTkFont(size=15, weight="bold"))
        r_title.grid(row=0, column=0, padx=15, pady=12, sticky="w")

        self.rules_scroll = ctk.CTkScrollableFrame(rules_box, fg_color="transparent")
        self.rules_scroll.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.refresh_rules()

    def refresh_rules(self):
        """Reload category mappings from ConfigService."""
        for child in self.rules_scroll.winfo_children():
            child.destroy()

        categories = self.config_service.get_all_categories()

        for cat_name, data in categories.items():
            card = ctk.CTkFrame(self.rules_scroll, fg_color="#0F172A", corner_radius=8)
            card.pack(fill="x", pady=5)
            card.grid_columnconfigure(1, weight=1)

            folder = data.get("folder", cat_name)
            exts = ", ".join(data.get("extensions", []))

            lbl_cat = ctk.CTkLabel(card, text=cat_name, font=ctk.CTkFont(size=14, weight="bold"), width=140, anchor="w")
            lbl_cat.grid(row=0, column=0, padx=15, pady=10, sticky="w")

            lbl_exts = ctk.CTkLabel(card, text=f"Folder: {folder}  |  Exts: {exts}", font=ctk.CTkFont(size=12), text_color="#94A3B8", anchor="w")
            lbl_exts.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    def _handle_save_rule(self):
        cat = self.cat_entry.get().strip()
        exts_str = self.ext_entry.get().strip()
        folder = self.folder_entry.get().strip()

        if not cat or not exts_str:
            messagebox.showwarning("Incomplete Form", "Category Name and Extensions fields are required.")
            return

        ext_list = [e.strip() for e in exts_str.split(",") if e.strip()]
        self.config_service.add_custom_rule(cat, ext_list, folder or None)

        self.cat_entry.delete(0, "end")
        self.ext_entry.delete(0, "end")
        self.folder_entry.delete(0, "end")

        messagebox.showinfo("Rule Saved", f"Successfully saved rule for '{cat}'.")
        self.refresh_rules()

    def _handle_reset_rules(self):
        confirm = messagebox.askyesno("Confirm Reset", "Reset all custom category rules back to system factory defaults?")
        if confirm:
            self.config_service.reset_rules_to_defaults()
            self.refresh_rules()
            messagebox.showinfo("Rules Reset", "Category rules have been reset to system defaults.")
