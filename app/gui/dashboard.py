"""Dashboard view displaying system overview and storage analytics."""
import customtkinter as ctk
from pathlib import Path
from typing import Callable, Optional
from PIL import Image
from app.gui.components import StatCard, CategoryProgressBar
from app.services.stats_service import StatsService
from app.utils.constants import FONT_FAMILY
from app.utils.helpers import format_file_size

class DashboardView(ctk.CTkFrame):
    """Main dashboard overview screen."""

    def __init__(self, master, stats_service: StatsService, on_navigate_organize: Optional[Callable[[], None]] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.stats_service = stats_service
        self.on_navigate_organize = on_navigate_organize

        self.grid_columnconfigure(0, weight=1)

        # Header Title with Logo
        hdr_frame = ctk.CTkFrame(self, fg_color="transparent")
        hdr_frame.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="ew")

        logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
        if logo_path.exists():
            try:
                pil_logo = Image.open(logo_path)
                ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(210, 70))
                logo_lbl = ctk.CTkLabel(hdr_frame, image=ctk_logo, text="")
                logo_lbl.pack(side="left", padx=(0, 15))
            except Exception:
                title_label = ctk.CTkLabel(hdr_frame, text="📊 SORTIFY Dashboard", font=ctk.CTkFont(family=FONT_FAMILY, size=26, weight="bold"))
                title_label.pack(side="left")
        else:
            title_label = ctk.CTkLabel(hdr_frame, text="📊 SORTIFY Dashboard", font=ctk.CTkFont(family=FONT_FAMILY, size=26, weight="bold"))
            title_label.pack(side="left")

        subtitle_label = ctk.CTkLabel(self, text="Developed by Francis Kusi  |  Overview of file triage activities and storage optimization metrics.", font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color="#3B82F6", anchor="w")
        subtitle_label.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="w")

        # Cards Container Frame
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.card_files = StatCard(self.cards_frame, title="Files Organized", value="0", icon_str="📁", color="#1E293B")
        self.card_files.grid(row=0, column=0, padx=8, pady=8, sticky="ew")

        self.card_runs = StatCard(self.cards_frame, title="Organization Runs", value="0", icon_str="⚡", color="#1E293B")
        self.card_runs.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        self.card_dups = StatCard(self.cards_frame, title="Duplicates Found", value="0", icon_str="🔍", color="#1E293B")
        self.card_dups.grid(row=0, column=2, padx=8, pady=8, sticky="ew")

        self.card_action = StatCard(self.cards_frame, title="Engine Status", value="Ready", icon_str="🛡️", color="#1E293B")
        self.card_action.grid(row=0, column=3, padx=8, pady=8, sticky="ew")

        # Quick Action Banner
        banner = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=12)
        banner.grid(row=3, column=0, padx=20, pady=15, sticky="ew")
        banner.grid_columnconfigure(0, weight=1)

        b_text = ctk.CTkLabel(banner, text="Declutter & organize your Downloads or Desktop folder in seconds.", font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"))
        b_text.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        btn = ctk.CTkButton(
            banner,
            text="🚀 Start New Organization",
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            height=40,
            command=self._handle_quick_start
        )
        btn.grid(row=0, column=1, padx=20, pady=20, sticky="e")

        # Category Breakdown Section
        breakdown_box = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=12)
        breakdown_box.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        breakdown_box.grid_columnconfigure(0, weight=1)

        b_title = ctk.CTkLabel(breakdown_box, text="Category Distribution", font=ctk.CTkFont(family=FONT_FAMILY, size=16, weight="bold"))
        b_title.pack(anchor="w", padx=20, pady=(15, 10))

        self.categories_scroll = ctk.CTkScrollableFrame(breakdown_box, fg_color="transparent", height=200)
        self.categories_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.refresh_stats()

    def _handle_quick_start(self):
        if self.on_navigate_organize:
            self.on_navigate_organize()

    def refresh_stats(self):
        """Reload analytics from StatsService."""
        stats = self.stats_service.get_dashboard_stats()
        self.card_files.update_value(str(stats.total_files_organized))
        self.card_runs.update_value(str(stats.total_runs))

        # Clear old category progress bars
        for child in self.categories_scroll.winfo_children():
            child.destroy()

        total_files = max(stats.total_files_organized, 1)
        colors = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#6366F1", "#14B8A6"]

        if not stats.category_breakdown:
            empty_lbl = ctk.CTkLabel(self.categories_scroll, text="No categorized files history yet. Run an organization scan to view metrics!", font=ctk.CTkFont(family=FONT_FAMILY, size=12), text_color="#A0AAB8")
            empty_lbl.pack(pady=20)
            return

        for idx, (cat_name, count) in enumerate(stats.category_breakdown.items()):
            pct = count / float(total_files)
            col = colors[idx % len(colors)]
            bar = CategoryProgressBar(self.categories_scroll, category_name=cat_name, count=count, percentage=pct, color=col)
            bar.pack(fill="x", pady=4)
