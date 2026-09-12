from datetime import datetime
import json
from pathlib import Path
from tkinter import filedialog
from typing import Any

import customtkinter as ctk

from services.translation_service import t
from utils.theme import (
    COLOR_BORDER,
    COLOR_DANGER,
    COLOR_DANGER_HOVER,
    COLOR_ON_PRIMARY,
    COLOR_PRIMARY,
    COLOR_SCROLLBAR,
    COLOR_SCROLLBAR_HOVER,
    COLOR_SECTION_ACTIVE,
    COLOR_SURFACE,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
)
from widgets.cards import InfoRow, SectionCard
from widgets.form_controls import (
    CheckboxRow,
    configure_focus_chain,
    LabeledDropdown,
    LabeledEntry,
    OutlineButton,
    PrimaryButton,
    ThemedComboBox,
)
from widgets.icons import create_icon


DEFAULT_SETTINGS: dict[str, str | bool] = {
    "language": "English",
    "theme": "Light",
    "start_page": "Dashboard",
    "units": "Metric (°C, m, mm, A, V, ...)",
    "date_format": "24/05/2024 (DD/MM/YYYY)",
    "time_format": "24-hour (23:59)",
    "default_com_port": "COM3",
    "default_baudrate": "115200",
    "auto_connect": True,
    "remember_device": True,
    "auto_save": True,
    "confirm_write": True,
    "confirm_reset": True,
    "expert_settings": False,
    "developer_mode": False,
    "require_password": True,
    "lock_advanced": False,
    "hide_sensitive": True,
    "report_language": "English",
    "company_name": "",
    "technician_name": "Technician",
    "export_folder": "C:\\",
    "report_format": "PDF",
}


class SettingsView(ctk.CTkFrame):
    """Application preferences screen.

    Controls are intentionally local-only until persistence is introduced in a
    later milestone. Action buttons currently report their action to stdout.
    """

    SECTION_NAMES = tuple(
        t(f"settings.{name}")
        for name in ("general", "connection", "application", "security", "reports")
    )
    # Breakpoints use logical pixels (physical width / CustomTkinter scaling).
    # The right panel needs more room than the old threshold allowed; moving it
    # below earlier protects the form from being compressed.
    RIGHT_PANEL_REFLOW_WIDTH = 1250
    MENU_REFLOW_WIDTH = 900
    THREE_COLUMN_FORM_WIDTH = 780
    TWO_COLUMN_FORM_WIDTH = 520
    HEADER_REFLOW_WIDTH = 900
    RESIZE_DEBOUNCE_MS = 500

    @classmethod
    def get_layout_mode(
        cls, scaled_width: int | float, widget_scaling: int | float = 1.0
    ) -> tuple[bool, bool, bool, int]:
        """Return responsive layout choices for a physical width and DPI scale.

        Keeping this calculation independent from Tk widgets makes the 100%,
        125%, and 150% breakpoint behavior directly testable.
        """
        width = scaled_width / max(float(widget_scaling), 0.01)
        panel_below = width < cls.RIGHT_PANEL_REFLOW_WIDTH
        stacked_header = width < cls.HEADER_REFLOW_WIDTH
        stack_workspace = width < cls.MENU_REFLOW_WIDTH

        form_width = width - (60 if stack_workspace else 275)
        if not panel_below:
            form_width -= 300
        if form_width >= cls.THREE_COLUMN_FORM_WIDTH:
            form_columns = 3
        elif form_width >= cls.TWO_COLUMN_FORM_WIDTH:
            form_columns = 2
        else:
            form_columns = 1

        return panel_below, stack_workspace, stacked_header, form_columns

    def __init__(self, master: Any, **kwargs: Any) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.controls: dict[str, Any] = {}
        self.section_widgets: dict[str, ctk.CTkFrame] = {}
        self.summary_rows: dict[str, InfoRow] = {}
        self.last_import = "Not yet"
        self.last_export = "Not yet"
        self._resize_job: str | None = None
        self._last_configure_signature: tuple[int, float] | None = None
        self._layout_mode: tuple[bool, bool, bool, int] | None = None

        self._build_header()
        self._build_workspace()
        self._configure_keyboard_navigation()
        self.bind("<Configure>", self._schedule_responsive_layout, add="+")
        self.after_idle(self._apply_responsive_layout)

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        header.grid(row=0, column=0, padx=30, pady=(24, 18), sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        self.header = header

        heading = ctk.CTkFrame(header, fg_color="transparent", corner_radius=0)
        heading.grid(row=0, column=0, sticky="w")
        self.header_heading = heading

        ctk.CTkLabel(
            heading,
            text=t("settings.title"),
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            heading,
            text=t("settings.subtitle"),
            font=ctk.CTkFont(size=13),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        ).pack(pady=(2, 0), anchor="w")

        actions = ctk.CTkFrame(header, fg_color="transparent", corner_radius=0)
        actions.grid(row=0, column=1, padx=(20, 0), sticky="e")
        self.header_actions = actions

        theme_menu = ThemedComboBox(
            actions,
            values=["Light", "Dark"],
            width=112,
            command=self._change_theme,
        )
        theme_menu.set("Light")
        theme_menu.grid(row=0, column=0, padx=(0, 8))
        self.controls["header_theme"] = theme_menu

        export_button = OutlineButton(
            actions,
            text=t("settings.export"),
            image=create_icon("download", 16, COLOR_PRIMARY),
            height=36,
            command=self._export_settings,
        )
        export_button.grid(row=0, column=1, padx=4)
        self.export_button = export_button

        import_button = PrimaryButton(
            actions,
            text=t("settings.import"),
            image=create_icon("upload", 16, COLOR_ON_PRIMARY),
            height=36,
            command=self._import_settings,
        )
        import_button.grid(row=0, column=2, padx=(4, 0))
        self.import_button = import_button

    def _build_workspace(self) -> None:
        workspace = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=COLOR_SCROLLBAR,
            scrollbar_button_hover_color=COLOR_SCROLLBAR_HOVER,
        )
        workspace.grid(row=1, column=0, sticky="nsew")
        self.workspace = workspace
        # CTkScrollableFrame normally forces its full inner widget tree to the
        # canvas width on every Configure event. Keep the current inner width
        # while a resize is active and fit it once from our debounced handler.
        workspace._parent_canvas.unbind("<Configure>")
        workspace.grid_columnconfigure(0, weight=0, minsize=205)
        workspace.grid_columnconfigure(1, weight=1)
        workspace.grid_columnconfigure(2, weight=0, minsize=0)
        workspace.grid_rowconfigure(0, weight=1)

        self._build_section_menu(workspace)

        center = ctk.CTkFrame(workspace, fg_color="transparent", corner_radius=0)
        center.grid(row=0, column=1, padx=(12, 14), pady=(0, 28), sticky="nsew")
        self.center = center
        center.grid_columnconfigure(0, weight=1)
        settings_surface = ctk.CTkFrame(
            center,
            fg_color=COLOR_SURFACE,
            border_width=1,
            border_color=COLOR_BORDER,
            corner_radius=12,
        )
        settings_surface.grid(row=0, column=0, sticky="nsew")
        self.settings_surface = settings_surface
        settings_surface.grid_columnconfigure(0, weight=1)
        self._build_general_section(settings_surface, 0)
        self._build_connection_section(settings_surface, 1)
        self._build_application_section(settings_surface, 2)
        self._build_security_section(settings_surface, 3)
        self._build_reports_section(settings_surface, 4)

        right_panel = ctk.CTkFrame(workspace, fg_color="transparent", corner_radius=0)
        right_panel.grid(row=0, column=2, padx=(0, 28), pady=(0, 28), sticky="new")
        right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel = right_panel
        self._build_right_panel(right_panel)

    def _build_section_menu(self, parent: Any) -> None:
        menu = SectionCard(parent)
        menu.configure(width=205)
        menu.grid(row=0, column=0, padx=(30, 0), pady=(0, 28), sticky="new")
        self.section_menu = menu
        self.section_buttons: list[ctk.CTkButton] = []

        for row, section_name in enumerate(self.SECTION_NAMES):
            active = row == 0
            button = ctk.CTkButton(
                menu.body,
                text=section_name,
                image=create_icon(
                    ("general", "connection", "application", "security", "reports")[row],
                    17,
                    COLOR_PRIMARY if active else COLOR_TEXT_MUTED,
                ),
                compound="left",
                height=48,
                corner_radius=6,
                fg_color=COLOR_SECTION_ACTIVE if active else "transparent",
                hover_color=COLOR_SECTION_ACTIVE,
                text_color=COLOR_PRIMARY if active else COLOR_TEXT,
                font=ctk.CTkFont(size=12, weight="bold" if active else "normal"),
                anchor="w",
                command=lambda name=section_name: self._scroll_to_section(name),
            )
            button.grid(row=row, column=0, pady=2, sticky="ew")
            self.section_buttons.append(button)

    def _build_general_section(self, parent: Any, row: int) -> None:
        card = self._new_section(
            parent,
            t("settings.general"),
            t("settings.general.description"),
            row,
        )
        body = card.body
        self.general_body = body
        for column in (0, 1, 2):
            body.grid_columnconfigure(column, weight=1, uniform="general")

        fields = (
            ("language", t("settings.language"), ["English", "Spanish", "French", "German"], "English"),
            ("theme", t("settings.theme"), ["Light", "Dark"], "Light"),
            ("start_page", t("settings.start_page"), ["Dashboard", "Live Measurements", "Configuration"], "Dashboard"),
            ("units", t("settings.units"), ["Metric (°C, m, mm, A, V, ...)", "Imperial (°F, ft, in, A, V, ...)"], "Metric (°C, m, mm, A, V, ...)"),
            ("date_format", t("settings.date_format"), ["24/05/2024 (DD/MM/YYYY)", "05/24/2024 (MM/DD/YYYY)", "2024-05-24 (YYYY-MM-DD)"], "24/05/2024 (DD/MM/YYYY)"),
            ("time_format", t("settings.time_format"), ["24-hour (23:59)", "12-hour (11:59 PM)"], "24-hour (23:59)"),
        )
        for index, (key, label, values, value) in enumerate(fields):
            if key == "theme":
                command = self._change_theme
            elif key in {"language", "units", "start_page"}:
                command = lambda _value: self._sync_summary()
            else:
                command = None
            control = LabeledDropdown(
                body, label, values, value=value, command=command
            )
            control.grid(
                row=index // 3,
                column=index % 3,
                padx=(0, 8) if index % 3 == 0 else ((8, 0) if index % 3 == 2 else 8),
                pady=2,
                sticky="ew",
            )
            self.controls[key] = control
        self.general_controls = [self.controls[key] for key, *_rest in fields]

    def _build_connection_section(self, parent: Any, row: int) -> None:
        card = self._new_section(
            parent, t("settings.connection"), t("settings.connection.description"), row
        )
        body = card.body
        self.connection_body = body
        for column in (0, 1, 2):
            body.grid_columnconfigure(column, weight=1, uniform="connection")

        port = LabeledDropdown(
            body, t("settings.default_com_port"), ["COM1", "COM2", "COM3", "COM4"], value="COM3"
        )
        port.grid(row=0, column=0, padx=(0, 8), pady=2, sticky="ew")
        baudrate = LabeledDropdown(
            body,
            t("settings.default_baudrate"),
            ["9600", "19200", "38400", "57600", "115200"],
            value="115200",
        )
        baudrate.grid(row=0, column=1, padx=(8, 0), pady=2, sticky="ew")
        self.controls.update(default_com_port=port, default_baudrate=baudrate)

        checks = ctk.CTkFrame(body, fg_color="transparent", corner_radius=0)
        checks.grid(row=0, column=2, padx=(18, 0), pady=(12, 0), sticky="nsew")
        checks.grid_columnconfigure(0, weight=1)
        self._add_checkbox(checks, 0, "auto_connect", t("settings.auto_connect"), True)
        self._add_checkbox(checks, 1, "remember_device", t("settings.remember_device"), True)
        self.connection_controls = (port, baudrate, checks)

    def _build_application_section(self, parent: Any, row: int) -> None:
        card = self._new_section(
            parent, t("settings.application"), t("settings.application.description"), row
        )
        self.application_body = card.body
        for column in (0, 1):
            card.body.grid_columnconfigure(column, weight=1, uniform="application")
        options = (
            ("auto_save", t("settings.auto_save"), True),
            ("confirm_write", t("settings.confirm_write"), True),
            ("confirm_reset", t("settings.confirm_reset"), True),
            ("expert_settings", t("settings.expert_settings"), False),
            ("developer_mode", t("settings.developer_mode"), False),
        )
        for option_row, (key, text, checked) in enumerate(options):
            column = 0 if option_row < 3 else 1
            grid_row = option_row if column == 0 else option_row - 3
            self._add_checkbox(card.body, grid_row, key, text, checked, column=column)
        self.application_controls = [self.controls[key] for key, *_rest in options]

    def _build_security_section(self, parent: Any, row: int) -> None:
        card = self._new_section(
            parent, t("settings.security"), t("settings.security.description"), row
        )
        self.security_body = card.body
        for column in (0, 1):
            card.body.grid_columnconfigure(column, weight=1, uniform="security")
        options = (
            ("require_password", t("settings.require_password"), True, None),
            ("lock_advanced", t("settings.lock_advanced"), False, None),
            (
                "hide_sensitive",
                t("settings.hide_sensitive"),
                True,
                t("settings.sensitive_description"),
            ),
        )
        for option_row, (key, text, checked, description) in enumerate(options):
            column = 0 if option_row < 2 else 1
            grid_row = option_row if column == 0 else 0
            self._add_checkbox(
                card.body,
                grid_row,
                key,
                text,
                checked,
                description=description,
                column=column,
            )
        self.security_controls = [self.controls[key] for key, *_rest in options]

    def _build_reports_section(self, parent: Any, row: int) -> None:
        card = self._new_section(
            parent,
            t("settings.reports"),
            t("settings.reports.description"),
            row,
        )
        body = card.body
        self.reports_body = body
        for column in (0, 1, 2):
            body.grid_columnconfigure(column, weight=1, uniform="reports")

        report_language = LabeledDropdown(
            body,
            t("settings.report_language"),
            ["English", "Spanish", "French", "German"],
            value="English",
        )
        report_language.grid(row=0, column=0, padx=(0, 8), pady=2, sticky="ew")
        report_format = LabeledDropdown(
            body, t("settings.report_format"), ["PDF", "CSV", "XLSX"], value="PDF"
        )
        report_format.grid(row=1, column=2, padx=(8, 0), pady=2, sticky="ew")

        company = LabeledEntry(body, t("settings.company_name"), placeholder_text=t("settings.company_name"))
        company.grid(row=0, column=1, padx=8, pady=2, sticky="ew")
        technician = LabeledEntry(body, t("settings.technician_name"), value="Technician")
        technician.grid(row=0, column=2, padx=(8, 0), pady=2, sticky="ew")

        folder_group = ctk.CTkFrame(body, fg_color="transparent", corner_radius=0)
        folder_group.grid(row=1, column=0, padx=(0, 8), pady=2, sticky="ew")
        folder_group.grid_columnconfigure(0, weight=1)
        folder = LabeledEntry(folder_group, t("settings.export_folder"), value="C:\\")
        folder.grid(row=0, column=0, sticky="ew")
        browse_button = OutlineButton(
            folder_group,
            text=t("settings.browse"),
            width=84,
            command=self._select_export_folder,
        )
        browse_button.grid(
            row=0, column=1, padx=(8, 0), pady=(19, 0), sticky="e"
        )
        self.browse_button = browse_button

        self.controls.update(
            report_language=report_language,
            report_format=report_format,
            company_name=company,
            technician_name=technician,
            export_folder=folder,
        )
        self.reports_controls = (
            report_language,
            company,
            technician,
            folder_group,
            report_format,
        )

    def _schedule_responsive_layout(self, _event: Any = None) -> None:
        """Debounce window resize work so dragging does not trigger redraw churn."""
        width = int(getattr(_event, "width", self.winfo_width()))
        signature = (width, float(self._get_widget_scaling()))
        if signature == self._last_configure_signature:
            return
        self._last_configure_signature = signature

        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(
            self.RESIZE_DEBOUNCE_MS, self._run_scheduled_responsive_layout
        )

    def _run_scheduled_responsive_layout(self) -> None:
        self._resize_job = None
        self._apply_responsive_layout()

    def _apply_responsive_layout(self) -> None:
        """Reposition existing widgets for the available logical pixel width."""
        self._fit_workspace_to_canvas()
        scaled_width = self.winfo_width()
        if scaled_width <= 1:
            return
        # CustomTkinter applies the detected Windows DPI factor to widgets.
        # Compare breakpoints in logical pixels so 100%, 125%, and 150%
        # produce the same layout decisions for the same usable space.
        mode = self.get_layout_mode(scaled_width, self._get_widget_scaling())
        if mode == self._layout_mode:
            return
        self._layout_mode = mode

        panel_below, stack_workspace, stacked_header, form_columns = mode

        self._layout_header(stacked_header)
        self._layout_workspace(panel_below, stack_workspace)
        self._layout_forms(form_columns)

    def _fit_workspace_to_canvas(self) -> None:
        """Resize scroll content once after native window resizing settles."""
        canvas = self.workspace._parent_canvas
        canvas.itemconfigure(
            self.workspace._create_window_id,
            width=max(1, canvas.winfo_width()),
        )

    def destroy(self) -> None:
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
            self._resize_job = None
        super().destroy()

    def _layout_header(self, stacked: bool) -> None:
        if stacked:
            self.header_heading.grid_configure(row=0, column=0, sticky="w")
            self.header_actions.grid_configure(
                row=1, column=0, padx=(0, 0), pady=(12, 0), sticky="w"
            )
        else:
            self.header_heading.grid_configure(row=0, column=0, sticky="w")
            self.header_actions.grid_configure(
                row=0, column=1, padx=(20, 0), pady=(0, 0), sticky="e"
            )

    def _layout_workspace(self, panel_below: bool, stack_workspace: bool) -> None:
        if stack_workspace:
            self._layout_section_menu(compact=True)
            self.workspace.grid_columnconfigure(0, weight=1, minsize=205)
            self.workspace.grid_columnconfigure(1, weight=1)
            self.workspace.grid_columnconfigure(2, weight=1, minsize=0)
            self.workspace.grid_rowconfigure(0, weight=0)
            self.workspace.grid_rowconfigure(1, weight=1)
            self.workspace.grid_rowconfigure(2, weight=0)
            self.section_menu.grid_configure(
                row=0, column=0, columnspan=3, padx=(30, 30), pady=(0, 16), sticky="ew"
            )
            self.center.grid_configure(
                row=1, column=0, columnspan=3, padx=(30, 30), pady=(0, 18), sticky="nsew"
            )
            self.right_panel.grid_configure(
                row=2, column=0, columnspan=3, padx=(30, 30), pady=(0, 28), sticky="ew"
            )
            return

        self._layout_section_menu(compact=False)
        self.workspace.grid_columnconfigure(0, weight=0, minsize=205)
        self.workspace.grid_columnconfigure(1, weight=1)
        self.workspace.grid_columnconfigure(2, weight=0, minsize=0)
        self.workspace.grid_rowconfigure(0, weight=1)
        self.workspace.grid_rowconfigure(1, weight=0)
        self.section_menu.grid_configure(
            row=0,
            column=0,
            columnspan=1,
            padx=(30, 0),
            pady=(0, 28),
            sticky="new",
        )
        if panel_below:
            self.center.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                padx=(12, 14),
                pady=(0, 18),
                sticky="nsew",
            )
            self.right_panel.grid_configure(
                row=1,
                column=1,
                columnspan=1,
                padx=(12, 28),
                pady=(0, 28),
                sticky="ew",
            )
        else:
            self.workspace.grid_columnconfigure(2, weight=0, minsize=270)
            self.center.grid_configure(
                row=0,
                column=1,
                columnspan=1,
                padx=(12, 14),
                pady=(0, 28),
                sticky="nsew",
            )
            self.right_panel.grid_configure(
                row=0,
                column=2,
                columnspan=1,
                padx=(0, 28),
                pady=(0, 28),
                sticky="new",
            )

    def _layout_section_menu(self, *, compact: bool) -> None:
        """Use a short, wrapping section selector when it sits above the form."""
        columns = 3 if compact else 1
        for column in range(3):
            self.section_menu.body.grid_columnconfigure(
                column,
                weight=1 if column < columns else 0,
                uniform="sections" if compact else "",
            )
        for index, button in enumerate(self.section_buttons):
            button.configure(height=40 if compact else 48)
            button.grid_configure(
                row=index // columns,
                column=index % columns,
                padx=4 if compact else 0,
                pady=3 if compact else 2,
            )

    def _layout_forms(self, columns: int) -> None:
        self._configure_form_columns(self.general_body, columns, 3, "general")
        self._grid_controls(self.general_controls, columns)

        self._configure_form_columns(
            self.connection_body, columns, 3, "connection"
        )
        port, baudrate, checks = self.connection_controls
        port.grid_configure(row=0, column=0, padx=(0, 8), pady=2, sticky="ew")
        baudrate.grid_configure(
            row=0 if columns > 1 else 1,
            column=1 if columns > 1 else 0,
            padx=(8, 0) if columns > 1 else (0, 8),
            pady=2,
            sticky="ew",
        )
        checks.grid_configure(
            row=2 if columns == 1 else (1 if columns == 2 else 0),
            column=0 if columns < 3 else 2,
            columnspan=columns if columns < 3 else 1,
            padx=(0, 0) if columns < 3 else (18, 0),
            pady=(8, 0) if columns < 3 else (12, 0),
            sticky="nsew",
        )

        self._configure_form_columns(
            self.application_body, 1 if columns == 1 else 2, 2, "application"
        )
        self._grid_controls(self.application_controls, 1 if columns == 1 else 2)
        self._configure_form_columns(
            self.security_body, 1 if columns == 1 else 2, 2, "security"
        )
        self._grid_controls(self.security_controls, 1 if columns == 1 else 2)
        self._configure_form_columns(self.reports_body, columns, 3, "reports")
        self._grid_controls(self.reports_controls, columns)

    @staticmethod
    def _configure_form_columns(
        body: Any, active_columns: int, total_columns: int, uniform: str
    ) -> None:
        for column in range(total_columns):
            active = column < active_columns
            body.grid_columnconfigure(
                column,
                weight=1 if active else 0,
                minsize=0,
                uniform=uniform if active else "",
            )

    @staticmethod
    def _grid_controls(controls: list[Any] | tuple[Any, ...], columns: int) -> None:
        for index, control in enumerate(controls):
            column = index % columns
            control.grid_configure(
                row=index // columns,
                column=column,
                padx=(
                    (0, 8)
                    if column == 0 and columns > 1
                    else ((8, 0) if column == columns - 1 and columns > 1 else 8)
                ),
                pady=2,
                sticky="ew",
            )

    def _build_right_panel(self, parent: Any) -> None:
        about = SectionCard(parent)
        about.grid(row=0, column=0, sticky="ew")
        about_header = ctk.CTkFrame(about.body, fg_color="transparent")
        about_header.grid(row=0, column=0, sticky="ew")
        about_header.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            about_header,
            text="ⓘ",
            font=ctk.CTkFont(size=18),
            text_color=COLOR_TEXT_MUTED,
        ).grid(row=0, column=0, padx=(0, 10))
        ctk.CTkLabel(
            about_header,
            text=t("settings.about"),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).grid(row=0, column=1, sticky="ew")
        ctk.CTkLabel(
            about.body,
            text=t("settings.about_text"),
            font=ctk.CTkFont(size=12),
            text_color=COLOR_TEXT_MUTED,
            justify="left",
            anchor="w",
        ).grid(row=1, column=0, pady=(12, 2), sticky="ew")

        self._right_divider(about.body, 2)
        ctk.CTkLabel(
            about.body,
            text=t("settings.current_configuration"),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).grid(row=3, column=0, pady=(2, 8), sticky="ew")
        rows = (
            (t("settings.language"), "English"),
            (t("settings.theme"), "Light"),
            (t("settings.units"), "Metric"),
            (t("settings.start_page"), "Dashboard"),
            (t("settings.auto_connect_summary"), "Enabled"),
            (t("settings.last_import"), self.last_import),
            (t("settings.last_export"), self.last_export),
        )
        for row, (label, value) in enumerate(rows):
            info = InfoRow(about.body, label, value, accent=False)
            info.grid(row=row + 4, column=0, sticky="ew")
            self.summary_rows[label] = info

        self._right_divider(about.body, 11)
        ctk.CTkLabel(
            about.body,
            text=t("settings.reset_title"),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        ).grid(row=12, column=0, sticky="ew")
        ctk.CTkLabel(
            about.body,
            text=t("settings.reset_description"),
            font=ctk.CTkFont(size=11),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        ).grid(row=13, column=0, pady=(5, 13), sticky="ew")
        reset_button = OutlineButton(
            about.body,
            text=t("settings.reset_button"),
            border_color=COLOR_DANGER,
            text_color=COLOR_DANGER,
            hover_color=COLOR_DANGER_HOVER,
            image=create_icon("refresh", 15, COLOR_DANGER),
            command=self._reset_settings,
        )
        reset_button.grid(row=14, column=0, sticky="ew")
        self.reset_button = reset_button

    def _new_section(
        self, parent: Any, title: str, description: str, row: int
    ) -> SectionCard:
        card = SectionCard(
            parent,
            title=title,
            description=description,
            compact=True,
            fg_color="transparent",
            border_width=0,
            corner_radius=0,
        )
        card.grid(
            row=row * 2,
            column=0,
            padx=8,
            pady=(8, 0) if row == 0 else ((0, 8) if row == 4 else 0),
            sticky="ew",
        )
        if row < 4:
            ctk.CTkFrame(parent, height=1, fg_color=COLOR_BORDER, corner_radius=0).grid(
                row=row * 2 + 1, column=0, padx=8, sticky="ew"
            )
        self.section_widgets[title] = card
        return card

    def _add_checkbox(
        self,
        parent: Any,
        row: int,
        key: str,
        text: str,
        checked: bool,
        *,
        description: str | None = None,
        column: int = 0,
    ) -> None:
        checkbox = CheckboxRow(
            parent,
            text,
            checked=checked,
            description=description,
            command=self._sync_summary if key == "auto_connect" else None,
        )
        checkbox.grid(
            row=row, column=column, pady=2, sticky="ew"
        )
        self.controls[key] = checkbox

    @staticmethod
    def _right_divider(parent: Any, row: int) -> None:
        ctk.CTkFrame(parent, height=1, fg_color=COLOR_BORDER, corner_radius=0).grid(
            row=row, column=0, pady=18, sticky="ew"
        )

    def _configure_keyboard_navigation(self) -> None:
        """Define one stable keyboard order matching the Settings content."""
        ordered_controls = [
            self.controls["header_theme"],
            self.export_button,
            self.import_button,
            *self.section_buttons,
            *self.general_controls,
            self.controls["default_com_port"],
            self.controls["default_baudrate"],
            self.controls["auto_connect"],
            self.controls["remember_device"],
            *self.application_controls,
            *self.security_controls,
            self.controls["report_language"],
            self.controls["company_name"],
            self.controls["technician_name"],
            self.controls["export_folder"],
            self.browse_button,
            self.controls["report_format"],
            self.reset_button,
        ]
        self.keyboard_focus_targets = configure_focus_chain(ordered_controls)

    def _scroll_to_section(self, section_name: str) -> None:
        """Scroll the settings workspace to the selected inner section."""
        section = self.section_widgets[section_name]
        self.update_idletasks()
        target_y = self.settings_surface.winfo_y() + section.winfo_y()
        content_height = max(1, self.workspace._parent_frame.winfo_reqheight())
        self.workspace._parent_canvas.yview_moveto(target_y / content_height)

    def _collect_settings(self) -> dict[str, str | bool]:
        return {
            key: control.get()
            for key, control in self.controls.items()
            if key in DEFAULT_SETTINGS
        }

    def _apply_settings(self, values: dict[str, Any]) -> None:
        for key, default in DEFAULT_SETTINGS.items():
            if key not in values or key not in self.controls:
                continue
            value = values[key]
            if isinstance(default, bool):
                if isinstance(value, bool):
                    self.controls[key].set(value)
            elif isinstance(value, str):
                if key == "theme" and value not in {"Light", "Dark"}:
                    value = "Light"
                self.controls[key].set(value)
        theme = str(self.controls["theme"].get())
        self.controls["header_theme"].set(theme)
        ctk.set_appearance_mode(theme.lower())
        self._sync_summary()

    def _export_settings(self) -> None:
        filename = filedialog.asksaveasfilename(
            parent=self.winfo_toplevel(),
            title="Export Settings",
            defaultextension=".json",
            filetypes=(("JSON settings", "*.json"),),
            initialfile="industrial-device-settings.json",
        )
        if not filename:
            return
        try:
            Path(filename).write_text(
                json.dumps(self._collect_settings(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as error:
            self._show_notice("Export failed", str(error), error=True)
            return
        self.last_export = datetime.now().strftime("%b %d, %Y %H:%M")
        self.summary_rows[t("settings.last_export")].set_value(self.last_export)
        self._show_notice("Settings exported", f"Saved to:\n{filename}")

    def _import_settings(self) -> None:
        filename = filedialog.askopenfilename(
            parent=self.winfo_toplevel(),
            title="Import Settings",
            filetypes=(("JSON settings", "*.json"),),
        )
        if not filename:
            return
        try:
            values = json.loads(Path(filename).read_text(encoding="utf-8"))
            if not isinstance(values, dict):
                raise ValueError("The settings file must contain a JSON object.")
        except (OSError, json.JSONDecodeError, ValueError) as error:
            self._show_notice("Import failed", str(error), error=True)
            return
        self._apply_settings(values)
        self.last_import = datetime.now().strftime("%b %d, %Y %H:%M")
        self.summary_rows[t("settings.last_import")].set_value(self.last_import)
        self._show_notice("Settings imported", f"Loaded from:\n{filename}")

    def _reset_settings(self) -> None:
        self._apply_settings(DEFAULT_SETTINGS)
        self._show_notice("Settings reset", "All settings were restored to defaults.")

    def _select_export_folder(self) -> None:
        folder = filedialog.askdirectory(
            parent=self.winfo_toplevel(), title="Select Default Export Folder"
        )
        if folder:
            self.controls["export_folder"].set(folder)

    def _change_theme(self, value: str) -> None:
        ctk.set_appearance_mode(value.lower())
        self.controls["header_theme"].set(value)
        if "theme" in self.controls:
            self.controls["theme"].set(value)
        self._sync_summary()

    def _sync_summary(self) -> None:
        values = self._collect_settings()
        summary_values = {
            t("settings.language"): str(values.get("language", "")),
            t("settings.theme"): str(values.get("theme", "")),
            t("settings.units"): "Metric" if str(values.get("units", "")).startswith("Metric") else "Imperial",
            t("settings.start_page"): str(values.get("start_page", "")),
            t("settings.auto_connect_summary"): "Enabled" if values.get("auto_connect") else "Disabled",
        }
        for label, value in summary_values.items():
            if label in self.summary_rows:
                self.summary_rows[label].set_value(value)

    def _show_notice(self, title: str, message: str, *, error: bool = False) -> None:
        """Display a small CustomTkinter-only feedback dialog."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("390x165")
        dialog.resizable(False, False)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            dialog,
            text=title,
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=COLOR_DANGER if error else COLOR_TEXT,
            anchor="w",
        ).grid(row=0, column=0, padx=22, pady=(20, 5), sticky="ew")
        ctk.CTkLabel(
            dialog,
            text=message,
            font=ctk.CTkFont(size=12),
            text_color=COLOR_TEXT_MUTED,
            justify="left",
            anchor="w",
            wraplength=345,
        ).grid(row=1, column=0, padx=22, sticky="ew")
        PrimaryButton(dialog, text="OK", width=82, command=dialog.destroy).grid(
            row=2, column=0, padx=22, pady=18, sticky="e"
        )
