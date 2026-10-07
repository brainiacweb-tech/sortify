"""Application preferences and settings view."""
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from app.services.config_service import ConfigService
from app.utils.constants import THEME_DARK, THEME_LIGHT, THEME_SYSTEM

class SettingsView(ctk.CTkFrame):
    """Application global settings view."""

    def __init__(self, master, config_service: ConfigService, on_theme_change: Optional[Callable[[str], None]] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.config_service = config_service
        self.on_theme_change = on_theme_change

        self.grid_columnconfigure(0, weight=1)

        # Header Title
        title_label = ctk.CTkLabel(self, text="🛠️ Application Settings", font=ctk.CTkFont(size=24, weight="bold"), anchor="w")
        title_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        subtitle_label = ctk.CTkLabel(self, text="Manage application preferences, default behaviors, and visual themes.", font=ctk.CTkFont(size=13), text_color="#8E9AAF", anchor="w")
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Preferences Box
        pref_box = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=12)
        pref_box.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        pref_box.grid_columnconfigure(0, weight=1)

        p_title = ctk.CTkLabel(pref_box, text="Appearance & Visual Theme", font=ctk.CTkFont(size=16, weight="bold"))
        p_title.pack(anchor="w", padx=20, pady=(15, 10))

        theme_row = ctk.CTkFrame(pref_box, fg_color="transparent")
        theme_row.pack(fill="x", padx=20, pady=(0, 15))

        lbl_t = ctk.CTkLabel(theme_row, text="Color Theme Mode:", font=ctk.CTkFont(size=13))
        lbl_t.pack(side="left", padx=(0, 15))

        cur_theme = self.config_service.get("theme", THEME_SYSTEM)
        self.theme_menu = ctk.CTkOptionMenu(theme_row, values=[THEME_DARK, THEME_LIGHT, THEME_SYSTEM], command=self._handle_theme_select)
        self.theme_menu.set(cur_theme)
        self.theme_menu.pack(side="left")

        # Behaviors Box
        beh_box = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=12)
        beh_box.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        beh_box.grid_columnconfigure(0, weight=1)

        b_title = ctk.CTkLabel(beh_box, text="Default Triage Behaviors", font=ctk.CTkFont(size=16, weight="bold"))
        b_title.pack(anchor="w", padx=20, pady=(15, 10))

        self.unk_var = ctk.BooleanVar(value=self.config_service.get("organize_unknown_files", True))
        chk_unk = ctk.CTkCheckBox(beh_box, text="Organize unknown files into 'Others' folder", variable=self.unk_var, command=self._save_toggles)
        chk_unk.pack(anchor="w", padx=20, pady=6)

        self.confirm_var = ctk.BooleanVar(value=self.config_service.get("confirm_before_organizing", True))
        chk_conf = ctk.CTkCheckBox(beh_box, text="Require confirmation prompt before executing file moves", variable=self.confirm_var, command=self._save_toggles)
        chk_conf.pack(anchor="w", padx=20, pady=6)

        self.date_var = ctk.BooleanVar(value=self.config_service.get("date_based_organization", False))
        chk_date = ctk.CTkCheckBox(beh_box, text="Enable date-based subfolders (e.g. Images/2026/October)", variable=self.date_var, command=self._save_toggles)
        chk_date.pack(anchor="w", padx=20, pady=(6, 15))

        # Reset Box
        rst_box = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=12)
        rst_box.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        rst_btn = ctk.CTkButton(rst_box, text="⚠️ Reset All Settings to Factory Defaults", fg_color="#DC2626", hover_color="#B91C1C", command=self._handle_reset_all)
        rst_btn.pack(anchor="w", padx=20, pady=15)

    def _handle_theme_select(self, theme_choice: str):
        self.config_service.set("theme", theme_choice)
        ctk.set_appearance_mode(theme_choice)
        if self.on_theme_change:
            self.on_theme_change(theme_choice)

    def _save_toggles(self):
        self.config_service.set("organize_unknown_files", self.unk_var.get())
        self.config_service.set("confirm_before_organizing", self.confirm_var.get())
        self.config_service.set("date_based_organization", self.date_var.get())

    def _handle_reset_all(self):
        confirm = messagebox.askyesno("Confirm Factory Reset", "Reset all application settings and custom rules to factory defaults?")
        if confirm:
            self.config_service.reset_all()
            ctk.set_appearance_mode(THEME_SYSTEM)
            messagebox.showinfo("Factory Reset", "Settings have been reset to default values.")
