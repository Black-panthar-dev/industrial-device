from typing import Any

import customtkinter as ctk

from utils.theme import (
    COLOR_BORDER,
    COLOR_PRIMARY,
    COLOR_SURFACE,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
    ThemeColor,
)


class SectionCard(ctk.CTkFrame):
    """A bordered content section with an optional heading and description.

    Add a section's controls to ``body`` so the card header and spacing remain
    consistent across screens.
    """

    def __init__(
        self,
        master: Any,
        title: str | None = None,
        description: str | None = None,
        compact: bool = False,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", COLOR_SURFACE)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", COLOR_BORDER)
        kwargs.setdefault("corner_radius", 10)
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        header_row = 0

        if title:
            self.title_label = ctk.CTkLabel(
                self,
                text=title,
                font=ctk.CTkFont(size=15 if compact else 16, weight="bold"),
                text_color=COLOR_TEXT,
                anchor="w",
                height=18 if compact else 24,
            )
            self.title_label.grid(
                row=header_row,
                column=0,
                padx=20 if compact else 24,
                pady=(12, 0) if compact else (18, 2),
                sticky="ew",
            )
            header_row += 1

        if description:
            self.description_label = ctk.CTkLabel(
                self,
                text=description,
                font=ctk.CTkFont(size=11 if compact else 12),
                text_color=COLOR_TEXT_MUTED,
                anchor="w",
                justify="left",
                wraplength=760,
                height=16 if compact else 24,
            )
            self.description_label.grid(
                row=header_row,
                column=0,
                padx=20 if compact else 24,
                pady=(2, 6) if compact else (2, 10),
                sticky="ew",
            )
            header_row += 1

        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.grid(
            row=header_row,
            column=0,
            padx=20 if compact else 24,
            pady=(
                (6 if header_row == 0 else 2, 12)
                if compact
                else (10 if header_row == 0 else 8, 18)
            ),
            sticky="nsew",
        )
        self.body.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(header_row, weight=1)


class InfoRow(ctk.CTkFrame):
    """A compact label/value row for read-only device information."""

    def __init__(
        self,
        master: Any,
        label: str,
        value: str,
        *,
        accent: bool = False,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("corner_radius", 0)
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1)
        self.label_widget = ctk.CTkLabel(
            self,
            text=label,
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.label_widget.grid(row=0, column=0, padx=(0, 20), pady=7, sticky="w")

        self.value_widget = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=COLOR_PRIMARY if accent else COLOR_TEXT,
            anchor="e",
        )
        self.value_widget.grid(row=0, column=1, pady=7, sticky="e")

    def set_value(self, value: str) -> None:
        self.value_widget.configure(text=value)


class SidebarStatusCard(ctk.CTkFrame):
    """A compact status panel sized for use in a sidebar."""

    def __init__(
        self,
        master: Any,
        title: str,
        status: str,
        *,
        detail: str | None = None,
        status_color: ThemeColor = COLOR_PRIMARY,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", COLOR_SURFACE)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", COLOR_BORDER)
        kwargs.setdefault("corner_radius", 9)
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(1, weight=1)
        self.status_indicator = ctk.CTkFrame(
            self,
            width=8,
            height=8,
            corner_radius=4,
            fg_color=status_color,
        )
        self.status_indicator.grid(row=0, column=0, padx=(14, 8), pady=(14, 2))
        self.status_indicator.grid_propagate(False)

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.title_label.grid(row=0, column=1, padx=(0, 14), pady=(12, 0), sticky="ew")

        self.status_label = ctk.CTkLabel(
            self,
            text=status,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        )
        self.status_label.grid(
            row=1, column=0, columnspan=2, padx=14, pady=(0, 2), sticky="ew"
        )

        if detail:
            self.detail_label = ctk.CTkLabel(
                self,
                text=detail,
                font=ctk.CTkFont(size=11),
                text_color=COLOR_TEXT_MUTED,
                anchor="w",
            )
            self.detail_label.grid(
                row=2,
                column=0,
                columnspan=2,
                padx=14,
                pady=(0, 12),
                sticky="ew",
            )
        else:
            self.status_label.grid_configure(pady=(0, 12))

    def set_status(self, status: str, color: ThemeColor | None = None) -> None:
        self.status_label.configure(text=status)
        if color is not None:
            self.status_indicator.configure(fg_color=color)
