"""Main window application layout and sidebar view router with full Light/Dark/System theme support."""
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from typing import Dict, Type
from pathlib import Path
from PIL import Image
from app.core.duplicate_detector import DuplicateDetector
from app.core.file_classifier import FileClassifier
from app.core.organizer import OrganizerEngine
from app.core.undo_manager import UndoManager
from app.gui.dashboard import DashboardView
from app.gui.duplicates_view import DuplicatesView
from app.gui.history_view import HistoryView
from app.gui.organize_view import OrganizeView
from app.gui.rules_view import RulesView
from app.gui.settings_view import SettingsView
from app.services.config_service import ConfigService
from app.services.stats_service import StatsService
from app.utils.constants import (
    APP_NAME,
    APP_VERSION,
    DEVELOPER_NAME,
    FONT_FAMILY,
    COLOR_SIDEBAR_BG,
    COLOR_BG_MAIN,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED
)

class MainWindow(ctk.CTk):
    """Top-level main window orchestrating sidebar navigation and view routing."""

    def __init__(self):
        super().__init__()

        # Load custom Raleway font if available
        font_file = Path(__file__).parent.parent / "assets" / "Raleway-VariableFont.ttf"
        if font_file.exists():
            try:
                ctk.FontManager.load_font(str(font_file))
            except Exception:
                pass

        # Core Services & Engines
        self.config_service = ConfigService()
        self.file_classifier = FileClassifier(self.config_service)
        self.undo_manager = UndoManager()
        self.duplicate_detector = DuplicateDetector()
        self.stats_service = StatsService(self.undo_manager)
        self.organizer_engine = OrganizerEngine(
            config_service=self.config_service,
            file_classifier=self.file_classifier,
            undo_manager=self.undo_manager,
            duplicate_detector=self.duplicate_detector
        )

        # Apply user theme preference
        theme = self.config_service.get("theme", "System")
        ctk.set_appearance_mode(theme)

        # Window Setup
        self.title(f"{APP_NAME} v{APP_VERSION} - Developed by {DEVELOPER_NAME}")
        self.geometry("1180x780")
        self.minsize(980, 680)

        # Main Layout: 2 Columns (Sidebar & Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_content_area()

        # Route to Dashboard initial view
        self.navigate_to("dashboard")

    def _build_sidebar(self):
        """Construct sidebar navigation panel."""
        self.sidebar_frame = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color=COLOR_SIDEBAR_BG
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        # App Brand Header with Logo
        logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
        if logo_path.exists():
            try:
                pil_logo = Image.open(logo_path)
                ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(175, 58))
                brand_label = ctk.CTkLabel(self.sidebar_frame, image=ctk_logo, text="")
                brand_label.grid(row=0, column=0, padx=15, pady=(20, 2), sticky="w")
            except Exception:
                brand_label = ctk.CTkLabel(
                    self.sidebar_frame,
                    text=f"✨ {APP_NAME}",
                    font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"),
                    text_color=COLOR_TEXT_PRIMARY
                )
                brand_label.grid(row=0, column=0, padx=20, pady=(20, 2), sticky="w")
        else:
            brand_label = ctk.CTkLabel(
                self.sidebar_frame,
                text=f"✨ {APP_NAME}",
                font=ctk.CTkFont(family=FONT_FAMILY, size=20, weight="bold"),
                text_color=COLOR_TEXT_PRIMARY
            )
            brand_label.grid(row=0, column=0, padx=20, pady=(20, 2), sticky="w")

        dev_sub_label = ctk.CTkLabel(
            self.sidebar_frame,
            text=f"by {DEVELOPER_NAME}",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLOR_PRIMARY
        )
        dev_sub_label.grid(row=0, column=0, padx=20, pady=(80, 10), sticky="w")

        # Navigation Buttons
        self.nav_buttons: Dict[str, ctk.CTkButton] = {}

        nav_items = [
            ("dashboard", "📊 Dashboard"),
            ("organize", "📁 Organize Files"),
            ("duplicates", "🔍 Duplicates"),
            ("history", "📜 History & Undo"),
            ("rules", "⚙️ Custom Rules"),
            ("settings", "🛠️ Settings"),
        ]

        for idx, (view_id, label_text) in enumerate(nav_items, start=1):
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=label_text,
                height=42,
                corner_radius=10,
                font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
                fg_color="transparent",
                text_color=COLOR_TEXT_SECONDARY,
                hover_color=("#F1F5F9", "#1E1F30"),
                anchor="w",
                command=lambda v=view_id: self.navigate_to(v)
            )
            btn.grid(row=idx, column=0, padx=12, pady=4, sticky="ew")
            self.nav_buttons[view_id] = btn

        # Footer Version & About
        about_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="ℹ️ About Sortify",
            height=32,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            fg_color="transparent",
            text_color=COLOR_TEXT_MUTED,
            hover_color=("#F1F5F9", "#1E1F30"),
            command=self._show_about_dialog
        )
        about_btn.grid(row=8, column=0, padx=12, pady=(0, 10), sticky="ew")

        ver_lbl = ctk.CTkLabel(
            self.sidebar_frame,
            text=f"Version {APP_VERSION}",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=COLOR_TEXT_MUTED
        )
        ver_lbl.grid(row=9, column=0, padx=20, pady=(0, 15), sticky="w")

    def _build_content_area(self):
        """Construct main right content view router container."""
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.views: Dict[str, ctk.CTkFrame] = {}

        # Instantiate View Frames
        self.views["dashboard"] = DashboardView(
            self.content_frame,
            stats_service=self.stats_service,
            on_navigate_organize=lambda: self.navigate_to("organize")
        )

        self.views["organize"] = OrganizeView(
            self.content_frame,
            organizer_engine=self.organizer_engine,
            config_service=self.config_service,
            on_completed=self._on_activity_updated
        )

        self.views["duplicates"] = DuplicatesView(
            self.content_frame,
            duplicate_detector=self.duplicate_detector
        )

        self.views["history"] = HistoryView(
            self.content_frame,
            undo_manager=self.undo_manager,
            on_undo_completed=self._on_activity_updated
        )

        self.views["rules"] = RulesView(
            self.content_frame,
            config_service=self.config_service
        )

        self.views["settings"] = SettingsView(
            self.content_frame,
            config_service=self.config_service,
            on_theme_change=lambda t: ctk.set_appearance_mode(t)
        )

    def navigate_to(self, view_id: str):
        """Switch active view frame and highlight sidebar button."""
        if view_id not in self.views:
            return

        # Hide all frames
        for v in self.views.values():
            v.grid_forget()

        # Show target frame
        target_view = self.views[view_id]
        target_view.grid(row=0, column=0, sticky="nsew")

        # Update button highlights
        for vid, btn in self.nav_buttons.items():
            if vid == view_id:
                btn.configure(fg_color=COLOR_PRIMARY, text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color=COLOR_TEXT_SECONDARY)

        # Refresh state if entering dashboard or history
        if view_id == "dashboard" and hasattr(target_view, "refresh_stats"):
            target_view.refresh_stats()
        elif view_id == "history" and hasattr(target_view, "refresh_history"):
            target_view.refresh_history()

    def _on_activity_updated(self):
        """Callback triggered after an organization run or undo execution."""
        if "dashboard" in self.views:
            self.views["dashboard"].refresh_stats()
        if "history" in self.views:
            self.views["history"].refresh_history()

    def _show_about_dialog(self):
        messagebox.showinfo(
            f"About {APP_NAME}",
            f"{APP_NAME} v{APP_VERSION}\n"
            f"Developed by {DEVELOPER_NAME}\n\n"
            "Professional Python File Organizer & Triage Engine.\n"
            "Guaranteed 100% zero data loss with dry-run previews, conflict-resolving renaming, SHA-256 duplicate detection, and full action undo.\n\n"
            "Built with Python & CustomTkinter."
        )
