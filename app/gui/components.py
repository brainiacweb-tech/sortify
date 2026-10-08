"""Reusable modern UI components with full Light/Dark/System theme tuple support."""
import customtkinter as ctk
import tkinter as tk
from typing import Callable, List, Optional
from app.utils.constants import (
    FONT_FAMILY,
    COLOR_CARD_BG,
    COLOR_CARD_BORDER,
    COLOR_CARD_HOVER,
    COLOR_PRIMARY,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_MUTED
)

class StatCard(ctk.CTkFrame):
    """Modern elevated metric stat card supporting Light/Dark/System themes."""

    def __init__(
        self,
        master,
        title: str,
        value: str,
        icon_str: str = "📊",
        accent_color: str = COLOR_PRIMARY,
        subtitle: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=COLOR_CARD_BG,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            **kwargs
        )

        self.grid_columnconfigure(1, weight=1)

        # Left Icon Badge Box
        icon_box = ctk.CTkFrame(self, fg_color=accent_color, width=44, height=44, corner_radius=12)
        icon_box.grid(row=0, column=0, rowspan=2, padx=(16, 12), pady=16)
        icon_box.grid_propagate(False)

        icon_label = ctk.CTkLabel(icon_box, text=icon_str, font=ctk.CTkFont(family=FONT_FAMILY, size=20))
        icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        title_label = ctk.CTkLabel(
            self,
            text=title.upper(),
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color=COLOR_TEXT_MUTED,
            anchor="w"
        )
        title_label.grid(row=0, column=1, padx=(0, 16), pady=(14, 0), sticky="w")

        # Value Label
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(family=FONT_FAMILY, size=22, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY,
            anchor="w"
        )
        self.value_label.grid(row=1, column=1, padx=(0, 16), pady=(0, 14), sticky="w")

    def update_value(self, new_value: str):
        """Update value displayed on card."""
        self.value_label.configure(text=new_value)


class QuickAccessCard(ctk.CTkFrame):
    """File category quick access card with dual theme support."""

    def __init__(
        self,
        master,
        title: str,
        extension_tag: str,
        count_text: str,
        color: str,
        icon_str: str = "📄",
        command: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=COLOR_CARD_BG,
            corner_radius=14,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            **kwargs
        )
        self.command = command

        self.grid_columnconfigure(0, weight=1)

        # Top Badge Header
        badge_frame = ctk.CTkFrame(self, fg_color=color, height=44, corner_radius=10)
        badge_frame.grid(row=0, column=0, padx=12, pady=(12, 8), sticky="ew")
        badge_frame.grid_propagate(False)

        badge_icon = ctk.CTkLabel(badge_frame, text=icon_str, font=ctk.CTkFont(family=FONT_FAMILY, size=20))
        badge_icon.place(relx=0.3, rely=0.5, anchor="center")

        badge_ext = ctk.CTkLabel(
            badge_frame,
            text=extension_tag,
            font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"),
            text_color="#FFFFFF"
        )
        badge_ext.place(relx=0.7, rely=0.5, anchor="center")

        # Title & Subtitle
        t_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        t_label.grid(row=1, column=0, padx=12, pady=(2, 0))

        sub_label = ctk.CTkLabel(
            self,
            text=count_text,
            font=ctk.CTkFont(family=FONT_FAMILY, size=11),
            text_color=COLOR_TEXT_MUTED
        )
        sub_label.grid(row=2, column=0, padx=12, pady=(0, 12))

        # Hover & Click Binding
        if self.command:
            self.bind("<Button-1>", lambda e: self.command())
            for child in self.winfo_children():
                child.bind("<Button-1>", lambda e: self.command())


class CategoryProgressBar(ctk.CTkFrame):
    """Progress bar showing percentage of files in a category with dual theme support."""

    def __init__(
        self,
        master,
        category_name: str,
        count: int,
        percentage: float,
        color: str = COLOR_PRIMARY,
        **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(1, weight=1)

        label = ctk.CTkLabel(
            self,
            text=category_name,
            width=130,
            anchor="w",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        label.grid(row=0, column=0, padx=(0, 10), pady=6, sticky="w")

        pbar = ctk.CTkProgressBar(
            self,
            height=10,
            corner_radius=5,
            progress_color=color,
            fg_color=("#E2E8F0", "#151624")
        )
        pbar.grid(row=0, column=1, padx=10, pady=6, sticky="ew")
        pbar.set(percentage)

        count_label = ctk.CTkLabel(
            self,
            text=f"{count} files ({int(percentage * 100)}%)",
            width=120,
            anchor="e",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12),
            text_color=COLOR_TEXT_SECONDARY
        )
        count_label.grid(row=0, column=2, padx=(10, 0), pady=6, sticky="e")


class HeaderBar(ctk.CTkFrame):
    """Top app header bar containing search bar and user profile indicator."""

    def __init__(self, master, on_search: Optional[Callable[[str], None]] = None, **kwargs):
        super().__init__(master, fg_color="transparent", height=50, **kwargs)
        self.on_search = on_search

        self.grid_columnconfigure(0, weight=1)

        # Search Bar Input
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="🔍 Search files, rules, or categories...",
            height=38,
            corner_radius=10,
            fg_color=COLOR_CARD_BG,
            border_color=COLOR_CARD_BORDER,
            text_color=COLOR_TEXT_PRIMARY,
            placeholder_text_color=COLOR_TEXT_MUTED,
            font=ctk.CTkFont(family=FONT_FAMILY, size=12)
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 20), sticky="ew")
        if self.on_search:
            self.search_entry.bind("<KeyRelease>", lambda e: self.on_search(self.search_entry.get()))

        # Notification & User Profile Badge Container
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="e")

        bell_btn = ctk.CTkButton(
            right_frame,
            text="🔔",
            width=38,
            height=38,
            corner_radius=10,
            fg_color=COLOR_CARD_BG,
            hover_color=COLOR_CARD_HOVER,
            border_width=1,
            border_color=COLOR_CARD_BORDER,
            text_color=COLOR_TEXT_PRIMARY
        )
        bell_btn.pack(side="left", padx=(0, 10))

        profile_badge = ctk.CTkFrame(
            right_frame,
            fg_color=COLOR_CARD_BG,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_CARD_BORDER
        )
        profile_badge.pack(side="left")

        avatar = ctk.CTkLabel(
            profile_badge,
            text="👤",
            font=ctk.CTkFont(size=14),
            width=28,
            height=28
        )
        avatar.pack(side="left", padx=(6, 2), pady=4)

        dev_label = ctk.CTkLabel(
            profile_badge,
            text="Francis Kusi",
            font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
            text_color=COLOR_TEXT_PRIMARY
        )
        dev_label.pack(side="left", padx=(2, 10), pady=4)
