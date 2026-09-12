import customtkinter as ctk

from services.translation_service import t
from utils.theme import COLOR_BORDER, COLOR_SURFACE, COLOR_TEXT, COLOR_TEXT_MUTED


class PlaceholderView(ctk.CTkFrame):
    """Simple placeholder for pages planned for later milestones."""

    def __init__(
        self,
        master: ctk.CTk,
        title: str,
        subtitle: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        )
        title_label.grid(
            row=0,
            column=0,
            padx=36,
            pady=(34, 6 if subtitle else 20),
            sticky="ew",
        )

        content_row = 1
        if subtitle:
            subtitle_label = ctk.CTkLabel(
                self,
                text=subtitle,
                font=ctk.CTkFont(size=14),
                text_color=COLOR_TEXT_MUTED,
                anchor="w",
            )
            subtitle_label.grid(
                row=1,
                column=0,
                padx=36,
                pady=(0, 20),
                sticky="ew",
            )
            content_row = 2

        placeholder_card = ctk.CTkFrame(
            self,
            fg_color=COLOR_SURFACE,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=10,
        )
        placeholder_card.grid(row=content_row, column=0, padx=36, sticky="ew")

        message = ctk.CTkLabel(
            placeholder_card,
            text=t("placeholder.page", title=title),
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLOR_TEXT,
        )
        message.pack(padx=28, pady=(26, 5), anchor="w")

        detail = ctk.CTkLabel(
            placeholder_card,
            text=t("placeholder.detail"),
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXT_MUTED,
        )
        detail.pack(padx=28, pady=(0, 26), anchor="w")
