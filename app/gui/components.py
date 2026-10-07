"""Reusable UI components for Smart File Organizer."""
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, List, Optional
from app.utils.constants import FONT_FAMILY

class StatCard(ctk.CTkFrame):
    """Modern metric stat card displaying value, title, and optional badge."""

    def __init__(self, master, title: str, value: str, icon_str: str = "📊", color: str = "#2B2D42", **kwargs):
        super().__init__(master, fg_color=color, corner_radius=12, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        
        # Header row: Icon & Title
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=16, pady=(16, 4), sticky="ew")

        icon_label = ctk.CTkLabel(header_frame, text=icon_str, font=ctk.CTkFont(family=FONT_FAMILY, size=22))
        icon_label.pack(side="left", padx=(0, 8))

        title_label = ctk.CTkLabel(header_frame, text=title, font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"), text_color="#A0AAB8")
        title_label.pack(side="left")

        # Value text
        self.value_label = ctk.CTkLabel(self, text=value, font=ctk.CTkFont(family=FONT_FAMILY, size=24, weight="bold"), text_color="#FFFFFF")
        self.value_label.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="w")

    def update_value(self, new_value: str):
        """Update value displayed on card."""
        self.value_label.configure(text=new_value)

class CategoryProgressBar(ctk.CTkFrame):
    """Progress bar showing percentage of files in a category."""

    def __init__(self, master, category_name: str, count: int, percentage: float, color: str = "#4A90E2", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.grid_columnconfigure(1, weight=1)

        label = ctk.CTkLabel(self, text=category_name, width=120, anchor="w", font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"))
        label.grid(row=0, column=0, padx=(0, 10), pady=4, sticky="w")

        pbar = ctk.CTkProgressBar(self, height=12, corner_radius=6, progress_color=color)
        pbar.grid(row=0, column=1, padx=10, pady=4, sticky="ew")
        pbar.set(percentage)

        count_label = ctk.CTkLabel(self, text=f"{count} files ({int(percentage * 100)}%)", width=100, anchor="e", font=ctk.CTkFont(family=FONT_FAMILY, size=12), text_color="#A0AAB8")
        count_label.grid(row=0, column=2, padx=(10, 0), pady=4, sticky="e")
