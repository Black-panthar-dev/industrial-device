from collections.abc import Callable
from typing import Any

import customtkinter as ctk

from services.translation_service import t
from utils.theme import (
    COLOR_ACTIVE,
    COLOR_ACTIVE_HOVER,
    COLOR_BORDER,
    COLOR_HOVER,
    COLOR_ON_PRIMARY,
    COLOR_PRIMARY,
    COLOR_SCROLLBAR,
    COLOR_SCROLLBAR_HOVER,
    COLOR_SIDEBAR,
    COLOR_STATUS_NEUTRAL,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
    SIDEBAR_WIDTH,
)
from widgets.cards import SidebarStatusCard
from widgets.icons import create_icon


TOP_ITEMS = (
    ("Dashboard", "sidebar.dashboard", "dashboard"),
    ("Live Measurements", "sidebar.live_measurements", "activity"),
    ("Configuration", "sidebar.configuration", "settings"),
)
CONFIGURATION_ITEMS = (
    ("General", "sidebar.general", "general"),
    ("Measurements", "sidebar.measurements", "measurements"),
    ("Communications", "sidebar.communications", "communications"),
    ("Relays", "sidebar.relays", "relays"),
    ("Alarms", "sidebar.alarms", "alarms"),
    ("I/O", "sidebar.io", "io"),
    ("Data Logging", "sidebar.data_logging", "logging"),
)
SERVICE_ITEMS = (
    ("Commissioning", "sidebar.commissioning", "commissioning"),
    ("Diagnostics", "sidebar.diagnostics", "diagnostics"),
    ("Logs", "sidebar.logs", "logs"),
    ("Maintenance", "sidebar.maintenance", "maintenance"),
)


class Sidebar(ctk.CTkFrame):
    """Client-style fixed navigation with configuration and status areas."""

    def __init__(
        self,
        master: Any,
        on_page_selected: Callable[[str], None],
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", COLOR_SIDEBAR)
        kwargs.setdefault("border_width", 0)
        super().__init__(
            master,
            width=SIDEBAR_WIDTH,
            corner_radius=0,
            **kwargs,
        )
        self.on_page_selected = on_page_selected
        self.buttons: dict[str, ctk.CTkButton] = {}
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_brand()
        self._build_navigation()
        self._build_footer()

        separator = ctk.CTkFrame(self, width=1, corner_radius=0, fg_color=COLOR_BORDER)
        separator.place(relx=1, rely=0, relheight=1, anchor="ne")

    def _build_brand(self) -> None:
        brand = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        brand.grid(row=0, column=0, padx=18, pady=(24, 23), sticky="ew")
        brand.grid_columnconfigure(1, weight=1)

        self._create_brand_logo(brand).grid(row=0, column=0, padx=(0, 10))
        ctk.CTkLabel(
            brand,
            text=t("app.title"),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).grid(row=0, column=1, sticky="ew")

    @staticmethod
    def _create_brand_logo(parent: Any) -> ctk.CTkFrame:
        """Create the temporary logo widget, isolated for a future assets image."""
        logo = ctk.CTkFrame(
            parent,
            width=40,
            height=40,
            corner_radius=10,
            fg_color=COLOR_PRIMARY,
        )
        logo.grid_propagate(False)
        logo.grid_rowconfigure(0, weight=1)
        logo.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            logo,
            text=t("app.brand_short"),
            text_color=COLOR_ON_PRIMARY,
            font=ctk.CTkFont(size=14, weight="bold"),
        ).grid(row=0, column=0, sticky="nsew")
        return logo

    def _build_navigation(self) -> None:
        navigation = ctk.CTkScrollableFrame(
            self,
            fg_color=COLOR_SIDEBAR,
            corner_radius=0,
            scrollbar_button_color=COLOR_SCROLLBAR,
            scrollbar_button_hover_color=COLOR_SCROLLBAR_HOVER,
        )
        navigation.grid(row=1, column=0, padx=(10, 5), sticky="nsew")
        navigation.grid_columnconfigure(0, weight=1)

        row = 0
        for page_name, label_key, icon in TOP_ITEMS:
            self._add_navigation_button(navigation, row, page_name, label_key, icon)
            row += 1

        for page_name, label_key, icon in CONFIGURATION_ITEMS:
            self._add_navigation_button(
                navigation, row, page_name, label_key, icon, indent=True, compact=True
            )
            row += 1

        divider = ctk.CTkFrame(navigation, height=1, fg_color=COLOR_BORDER)
        divider.grid(row=row, column=0, padx=8, pady=12, sticky="ew")
        row += 1

        for page_name, label_key, icon in SERVICE_ITEMS:
            self._add_navigation_button(navigation, row, page_name, label_key, icon)
            row += 1

        status = SidebarStatusCard(
            navigation,
            title=t("sidebar.device_status"),
            status=t("sidebar.no_device"),
            detail=t("sidebar.gui_only"),
            status_color=COLOR_STATUS_NEUTRAL,
        )
        status.grid(row=row, column=0, padx=7, pady=(22, 6), sticky="ew")

    def _add_navigation_button(
        self,
        parent: Any,
        row: int,
        page_name: str,
        label_key: str,
        icon: str,
        *,
        indent: bool = False,
        compact: bool = False,
    ) -> None:
        display_text = t(label_key)
        if page_name == "Configuration":
            display_text += "                              ⌃"
        button = ctk.CTkButton(
            parent,
            text=display_text,
            image=create_icon(icon, 16, COLOR_TEXT_MUTED),
            compound="left",
            height=32 if compact else 39,
            corner_radius=7,
            fg_color="transparent",
            hover_color=COLOR_HOVER,
            text_color=COLOR_TEXT,
            font=ctk.CTkFont(size=12 if compact else 13, weight="bold" if not compact else "normal"),
            anchor="w",
            command=lambda name=page_name: self._select_page(name),
        )
        button.grid(
            row=row,
            column=0,
            padx=(28 if indent else 5, 5),
            pady=1,
            sticky="ew",
        )
        self.buttons[page_name] = button

    def _build_footer(self) -> None:
        footer = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        footer.grid(row=2, column=0, padx=16, pady=(8, 15), sticky="ew")
        for column in (0, 1, 2):
            footer.grid_columnconfigure(column, weight=1)

        settings_button = ctk.CTkButton(
            footer,
            text="",
            image=create_icon("settings", 19, COLOR_PRIMARY),
            width=42,
            height=42,
            corner_radius=7,
            fg_color="transparent",
            hover_color=COLOR_HOVER,
            text_color=COLOR_PRIMARY,
            command=lambda: self._select_page("Settings"),
        )
        settings_button.grid(row=0, column=0, sticky="w")
        self.buttons["Settings"] = settings_button

        for column, (name, symbol) in enumerate(
            (("help", t("sidebar.help")), ("info", t("sidebar.about"))), start=1
        ):
            ctk.CTkButton(
                footer,
                text="",
                image=create_icon(name, 17, COLOR_TEXT_MUTED),
                width=36,
                height=36,
                corner_radius=18,
                fg_color="transparent",
                hover_color=COLOR_HOVER,
                text_color=COLOR_TEXT_MUTED,
                command=lambda action=symbol: self._show_information(action),
            ).grid(row=0, column=column)

    def _select_page(self, page_name: str) -> None:
        self.on_page_selected(page_name)

    def set_active(self, page_name: str) -> None:
        """Update the navigation highlight for the visible page."""
        for name, button in self.buttons.items():
            is_active = name == page_name
            button.configure(
                fg_color=COLOR_ACTIVE if is_active else "transparent",
                hover_color=COLOR_ACTIVE_HOVER if is_active else COLOR_HOVER,
                text_color=COLOR_PRIMARY if is_active else COLOR_TEXT,
            )

    @staticmethod
    def _show_information(action: str) -> None:
        print(t("sidebar.action_message", action=action))
