"""Dashboard view displaying system overview and storage analytics (Explo Design System)."""
import customtkinter as ctk
from pathlib import Path
from typing import Callable, Optional
from PIL import Image
from app.gui.components import StatCard, CategoryProgressBar, QuickAccessCard, HeaderBar
from app.services.stats_service import StatsService
from app.utils.constants import (
    FONT_FAMILY,
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_CARD_HOVER,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_SUCCESS,
    COLOR_INFO,
    COLOR_WARNING,
    COLOR_PURPLE,
    COLOR_PINK,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED
)
from app.utils.helpers import format_file_size

class DashboardView(ctk.CTkFrame):
    """Main dashboard overview screen inspired by Explo layout."""

    def __init__(
        self,
        master,
        stats_service: StatsService,
        on_navigate_organize: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.stats_service = stats_service
        self.on_navigate_organize = on_navigate_organize

        self.grid_columnconfigure(0, weight=1)

        # 1. Top Header Bar (Search & User Badge)
        self.header_bar = HeaderBar(self, on_search=self._handle_search)
        self.header_bar.grid(row=0, column=0, padx=24, pady=(20, 10), sticky="ew")

        # 2. Hero Banner / Title Header
        hdr_frame = ctk.CTkFrame(self, fg_color="transparent")
        hdr_frame.grid(row=1, column=0, padx=24, pady=(5, 15), sticky="ew")
        hdr_frame.grid_columnconfigure(0, weight=1)

        t_lbl = ctk.CTkLabel(
            hdr_frame,
            text="Storage Analytics & Triage Center",
            font=ctk.CTkFont(family=FONT_FAMILY, size=24, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        t_lbl.grid(row=0, column=0, sticky="w")

        sub_lbl = ctk.CTkLabel(
            hdr_frame,
            text="Overview of categorized file distributions, storage optimization, and duplicate metrics.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        sub_lbl.grid(row=1, column=0, sticky="w")

        # 3. Quick Access Cards Row (Explo Style File Category Badges)
        qa_label = ctk.CTkLabel(
            self,
            text="QUICK ACCESS CATEGORIES",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        qa_label.grid(row=2, column=0, padx=24, pady=(5, 5), sticky="w")

        qa_frame = ctk.CTkFrame(self, fg_color="transparent")
        qa_frame.grid(row=3, column=0, padx=24, pady=(0, 15), sticky="ew")
        qa_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.qa_docs = QuickAccessCard(
            qa_frame,
            title="Documents",
            extension_tag="DOCX / PDF",
            count_text="Auto-categorized",
            color=COLOR_INFO,
            icon_str="📄",
            command=self._handle_quick_start
        )
        self.qa_docs.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.qa_sheets = QuickAccessCard(
            qa_frame,
            title="Spreadsheets",
            extension_tag="XLSX / CSV",
            count_text="Financial & Data",
            color=COLOR_SUCCESS,
            icon_str="📊",
            command=self._handle_quick_start
        )
        self.qa_sheets.grid(row=0, column=1, padx=4, sticky="ew")

        self.qa_media = QuickAccessCard(
            qa_frame,
            title="Media & Photos",
            extension_tag="PNG / MP4",
            count_text="Images & Video",
            color=COLOR_PURPLE,
            icon_str="🎨",
            command=self._handle_quick_start
        )
        self.qa_media.grid(row=0, column=2, padx=4, sticky="ew")

        self.qa_zip = QuickAccessCard(
            qa_frame,
            title="Archives",
            extension_tag="ZIP / RAR",
            count_text="Compressed Packages",
            color=COLOR_WARNING,
            icon_str="📦",
            command=self._handle_quick_start
        )
        self.qa_zip.grid(row=0, column=3, padx=(8, 0), sticky="ew")

        # 4. Metric Stat Cards Row
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=4, column=0, padx=24, pady=(0, 15), sticky="ew")
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.card_files = StatCard(
            self.cards_frame,
            title="Files Organized",
            value="0",
            icon_str="📁",
            accent_color=COLOR_SUCCESS
        )
        self.card_files.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        self.card_runs = StatCard(
            self.cards_frame,
            title="Triage Runs",
            value="0",
            icon_str="⚡",
            accent_color=COLOR_INFO
        )
        self.card_runs.grid(row=0, column=1, padx=4, sticky="ew")

        self.card_dups = StatCard(
            self.cards_frame,
            title="Duplicates Found",
            value="0",
            icon_str="🔍",
            accent_color=COLOR_PURPLE
        )
        self.card_dups.grid(row=0, column=2, padx=4, sticky="ew")

        self.card_action = StatCard(
            self.cards_frame,
            title="Engine Health",
            value="100% Active",
            icon_str="🛡️",
            accent_color=COLOR_PRIMARY
        )
        self.card_action.grid(row=0, column=3, padx=(8, 0), sticky="ew")

        # 5. Quick Action Banner
        banner = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_CARD_BORDER
        )
        banner.grid(row=5, column=0, padx=24, pady=(0, 15), sticky="ew")
        banner.grid_columnconfigure(0, weight=1)

        b_text_frame = ctk.CTkFrame(banner, fg_color="transparent")
        b_text_frame.grid(row=0, column=0, padx=20, pady=16, sticky="w")

        b_title = ctk.CTkLabel(
            b_text_frame,
            text="Ready to declutter your Downloads or Desktop?",
            font=ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        b_title.pack(anchor="w")

        b_sub = ctk.CTkLabel(
            b_text_frame,
            text="Sort thousands of messy files safely with dry-run preview and instant undo protection.",
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        b_sub.pack(anchor="w")

        btn = ctk.CTkButton(
            banner,
            text="🚀 Start New Organization",
            font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            height=40,
            corner_radius=10,
            command=self._handle_quick_start
        )
        btn.grid(row=0, column=1, padx=20, pady=16, sticky="e")

        # 6. Category Breakdown Box
        breakdown_box = ctk.CTkFrame(
            self,
            fg_color=COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_CARD_BORDER
        )
        breakdown_box.grid(row=6, column=0, padx=24, pady=(0, 20), sticky="ew")
        breakdown_box.grid_columnconfigure(0, weight=1)

        b_hdr = ctk.CTkLabel(
            breakdown_box,
            text="CATEGORY DISTRIBUTION BREAKDOWN",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        b_hdr.pack(anchor="w", padx=20, pady=(16, 8))

        self.categories_scroll = ctk.CTkScrollableFrame(
            breakdown_box,
            fg_color="transparent",
            height=160
        )
        self.categories_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 16))

        self.refresh_stats()

    def _handle_search(self, query: str):
        """Handle search queries from header bar."""
        pass

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
        colors = [
            COLOR_PRIMARY,
            COLOR_SUCCESS,
            COLOR_INFO,
            COLOR_WARNING,
            COLOR_PURPLE,
            COLOR_PINK
        ]

        if not stats.category_breakdown:
            empty_lbl = ctk.CTkLabel(
                self.categories_scroll,
                text="No categorized file history recorded yet. Run an organization scan to view metrics!",
                font=ctk.CTkFont(family=FONT_FAMILY, size=12),
                text_color=COLOR_TEXT_MUTED
            )
            empty_lbl.pack(pady=20)
            return

        for idx, (cat_name, count) in enumerate(stats.category_breakdown.items()):
            pct = count / float(total_files)
            col = colors[idx % len(colors)]
            bar = CategoryProgressBar(
                self.categories_scroll,
                category_name=cat_name,
                count=count,
                percentage=pct,
                color=col
            )
            bar.pack(fill="x", pady=4)
