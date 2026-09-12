"""Milestone 2 General device-configuration screen (GUI-only)."""

from typing import Any

import customtkinter as ctk

from services.translation_service import t
from utils.theme import COLOR_ON_PRIMARY, COLOR_PRIMARY, COLOR_SCROLLBAR, COLOR_SCROLLBAR_HOVER
from widgets.cards import SectionCard
from widgets.form_controls import CheckboxRow, LabeledDropdown, LabeledEntry, OutlineButton, PrimaryButton, ThemedComboBox, configure_focus_chain
from widgets.icons import create_icon
from widgets.ml2_components import ActionButtonRow, InlineInfoBanner, PageHeader, ReadonlyField, SectionHeader, StatusPanel, StatusRow


class GeneralView(ctk.CTkFrame):
    """Configure general device values using dummy/local-only controls."""

    PANEL_REFLOW_WIDTH = 1120
    FORM_REFLOW_WIDTH = 720
    HEADER_REFLOW_WIDTH = 900
    RESIZE_DEBOUNCE_MS = 180

    def __init__(self, master: Any, **kwargs: Any) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._resize_job: str | None = None
        self._layout_mode: tuple[bool, bool, bool] | None = None
        self._form_groups: list[tuple[ctk.CTkFrame, list[ctk.CTkBaseClass]]] = []
        self.focus_controls: list[Any] = []
        self._build_header()
        self._build_workspace()
        self.focus_targets = configure_focus_chain(self.focus_controls)
        self.bind("<Configure>", self._schedule_responsive_layout, add="+")
        self.after_idle(self._apply_responsive_layout)

    @classmethod
    def get_layout_mode(cls, scaled_width: int | float, widget_scaling: int | float = 1.0) -> tuple[bool, bool, bool]:
        width = scaled_width / max(float(widget_scaling), 0.01)
        return width < cls.PANEL_REFLOW_WIDTH, width < cls.FORM_REFLOW_WIDTH, width < cls.HEADER_REFLOW_WIDTH

    def _build_header(self) -> None:
        self.header = PageHeader(self, t("general.title"), t("general.subtitle"))
        self.header.grid(row=0, column=0, padx=30, pady=(24, 18), sticky="ew")
        self.theme_menu = ThemedComboBox(
            self.header.controls,
            values=[t("general.theme.light"), t("general.theme.dark")],
            width=108,
            command=self._change_theme,
        )
        self.theme_menu.set(t("general.theme.light"))
        self.header.add_control(self.theme_menu)
        self.export_button = OutlineButton(
            self.header.controls,
            text=t("general.export"),
            image=create_icon("download", 16, COLOR_PRIMARY),
            command=lambda: self._placeholder_action(t("general.export")),
        )
        self.header.add_control(self.export_button)
        self.import_button = PrimaryButton(
            self.header.controls,
            text=t("general.import"),
            image=create_icon("upload", 16, COLOR_ON_PRIMARY),
            command=lambda: self._placeholder_action(t("general.import")),
        )
        self.header.add_control(self.import_button)
        self.focus_controls.extend((self.theme_menu, self.export_button, self.import_button))

    def _build_workspace(self) -> None:
        self.workspace = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=COLOR_SCROLLBAR,
            scrollbar_button_hover_color=COLOR_SCROLLBAR_HOVER,
        )
        self.workspace.grid(row=1, column=0, sticky="nsew")
        self.workspace.grid_columnconfigure(0, weight=1)
        self.workspace.grid_columnconfigure(1, weight=0, minsize=285)
        self.main_content = ctk.CTkFrame(self.workspace, fg_color="transparent", corner_radius=0)
        self.main_content.grid(row=0, column=0, padx=(30, 14), pady=(0, 30), sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self._build_identification_section(0)
        self._build_datetime_section(1)
        self._build_operation_section(2)
        self._build_information_section(3)
        self._build_actions_section(4)
        self.right_panel = ctk.CTkFrame(self.workspace, fg_color="transparent", corner_radius=0)
        self.right_panel.grid(row=0, column=1, padx=(0, 30), pady=(0, 30), sticky="new")
        self.right_panel.grid_columnconfigure(0, weight=1)
        self._build_right_panel()

    def _new_section(self, row: int, number: int, title_key: str, subtitle_key: str) -> ctk.CTkFrame:
        card = SectionCard(self.main_content)
        card.grid(row=row, column=0, pady=(0, 14), sticky="ew")
        header = SectionHeader(card.body, number, t(title_key), description=t(subtitle_key))
        header.grid(row=0, column=0, pady=(0, 16), sticky="ew")
        fields = ctk.CTkFrame(card.body, fg_color="transparent", corner_radius=0)
        fields.grid(row=1, column=0, sticky="ew")
        fields.grid_columnconfigure((0, 1), weight=1, uniform=f"general_{row}")
        return fields

    def _register_fields(self, parent: ctk.CTkFrame, controls: list[ctk.CTkBaseClass]) -> None:
        self._form_groups.append((parent, controls))
        self._layout_fields(parent, controls, columns=2)

    @staticmethod
    def _layout_fields(parent: ctk.CTkFrame, controls: list[ctk.CTkBaseClass], columns: int) -> None:
        for column in (0, 1):
            parent.grid_columnconfigure(column, weight=1 if column < columns else 0)
        for index, control in enumerate(controls):
            row, column = divmod(index, columns)
            padding = (0, 8) if column == 0 and columns > 1 else ((8, 0) if column else 0)
            control.grid(row=row, column=column, padx=padding, pady=(0, 13), sticky="ew")

    def _build_identification_section(self, row: int) -> None:
        fields = self._new_section(row, 1, "general.sections.device_identification.title", "general.sections.device_identification.subtitle")
        device_name = LabeledEntry(fields, t("general.device_name"), value=t("general.value.device_name"))
        site_name = LabeledEntry(fields, t("general.site_name"), value=t("general.value.site_name"))
        self._register_fields(fields, [
            device_name,
            site_name,
            ReadonlyField(fields, t("general.serial_number"), t("general.value.serial_number")),
            ReadonlyField(fields, t("general.hardware_version"), t("general.value.hardware_version")),
            ReadonlyField(fields, t("general.firmware_version"), t("general.value.firmware_version")),
        ])
        self.focus_controls.extend((device_name, site_name))

    def _build_datetime_section(self, row: int) -> None:
        fields = self._new_section(row, 2, "general.sections.date_time.title", "general.sections.date_time.subtitle")
        self.ntp_status = ReadonlyField(fields, t("general.ntp_status"), t("general.value.synchronized"))
        timezone = LabeledDropdown(fields, t("general.timezone"), [t("general.value.timezone"), t("general.options.timezone.utc"), t("general.options.timezone.karachi")], value=t("general.value.timezone"))
        sync = ActionButtonRow(fields, [(t("general.sync_pc"), lambda: self._placeholder_action(t("general.sync_pc")))])
        use_ntp = CheckboxRow(fields, t("general.use_ntp"), checked=True)
        self._register_fields(fields, [
            ReadonlyField(fields, t("general.device_datetime"), t("general.value.device_datetime")),
            timezone,
            sync,
            use_ntp,
            self.ntp_status,
        ])
        self.focus_controls.extend((timezone, *sync.buttons, use_ntp))

    def _build_operation_section(self, row: int) -> None:
        fields = self._new_section(row, 3, "general.sections.general_operation.title", "general.sections.general_operation.subtitle")
        measurement_interval = LabeledDropdown(fields, t("general.measurement_interval"), [t("general.options.interval.1_second"), t("general.options.interval.5_seconds"), t("general.options.interval.10_seconds")], value=t("general.options.interval.1_second"))
        logging_interval = LabeledDropdown(fields, t("general.logging_interval"), [t("general.options.interval.30_seconds"), t("general.options.interval.60_seconds"), t("general.options.interval.5_minutes")], value=t("general.options.interval.60_seconds"))
        watchdog = CheckboxRow(fields, t("general.enable_watchdog"), checked=True)
        scheduled_reboot = CheckboxRow(fields, t("general.scheduled_reboot"), checked=False)
        reboot_frequency = LabeledDropdown(fields, t("general.reboot_frequency"), [t("general.options.frequency.daily"), t("general.options.frequency.weekly"), t("general.options.frequency.monthly")], value=t("general.options.frequency.daily"))
        reboot_time = LabeledEntry(fields, t("general.reboot_time"), value=t("general.value.reboot_time"))
        controls = [measurement_interval, logging_interval, watchdog, scheduled_reboot, reboot_frequency, reboot_time]
        self._register_fields(fields, controls)
        self.focus_controls.extend(controls)

    def _build_information_section(self, row: int) -> None:
        fields = self._new_section(row, 4, "general.sections.device_information.title", "general.sections.device_information.subtitle")
        self._register_fields(fields, [
            ReadonlyField(fields, t("general.status"), t("general.value.connected")),
            ReadonlyField(fields, t("general.uptime"), t("general.value.uptime")),
            ReadonlyField(fields, t("general.last_reset"), t("general.value.last_reset")),
            ReadonlyField(fields, t("general.battery_voltage"), t("general.value.unavailable")),
            ReadonlyField(fields, t("general.signal_quality"), t("general.value.unavailable")),
        ])

    def _build_actions_section(self, row: int) -> None:
        fields = self._new_section(row, 5, "general.sections.configuration_actions.title", "general.sections.configuration_actions.subtitle")
        keys = ("general.read_device", "general.write_device", "general.load_file", "general.save_file")
        self.action_buttons = ActionButtonRow(fields, [(t(key), lambda action=t(key): self._placeholder_action(action)) for key in keys])
        self.action_buttons.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.focus_controls.extend(self.action_buttons.buttons)

    def _status_panel(self, row: int, title_key: str, values: list[tuple[str, str]]) -> None:
        panel = StatusPanel(self.right_panel, t(title_key))
        panel.grid(row=row, column=0, pady=(0, 14), sticky="ew")
        for item_row, (label_key, value) in enumerate(values):
            status = StatusRow(panel.body, t(label_key), value)
            status.grid(row=item_row, column=0, sticky="ew")

    def _build_right_panel(self) -> None:
        self._status_panel(0, "general.connection.title", [
            ("general.status", t("general.value.connected")), ("general.port", t("general.value.port")),
            ("general.baudrate", t("general.value.baudrate")), ("general.connection_time", t("general.value.connection_time")),
        ])
        self._status_panel(1, "general.summary.title", [
            ("general.device_name", t("general.value.device_name")), ("general.serial_number", t("general.value.serial_number")),
            ("general.firmware_version", t("general.value.firmware_version")), ("general.hardware_version", t("general.value.hardware_version")),
        ])
        self._status_panel(2, "general.configuration_status.title", [
            ("general.last_read", t("general.value.last_read")), ("general.last_written", t("general.value.last_written")),
            ("general.configuration_source", t("general.value.device")),
        ])
        InlineInfoBanner(self.right_panel, t("general.connection_banner")).grid(row=3, column=0, sticky="ew")

    def _schedule_responsive_layout(self, _event: Any = None) -> None:
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(self.RESIZE_DEBOUNCE_MS, self._apply_responsive_layout)

    def _apply_responsive_layout(self) -> None:
        self._resize_job = None
        mode = self.get_layout_mode(self.winfo_width(), self._get_widget_scaling())
        if mode == self._layout_mode:
            return
        self._layout_mode = mode
        panel_below, one_column, header_stacked = mode
        if panel_below:
            self.right_panel.grid_configure(row=1, column=0, padx=30, pady=(0, 30), sticky="ew")
            self.workspace.grid_columnconfigure(1, minsize=0, weight=0)
        else:
            self.right_panel.grid_configure(row=0, column=1, padx=(0, 30), pady=(0, 30), sticky="new")
            self.workspace.grid_columnconfigure(1, minsize=285, weight=0)
        for parent, controls in self._form_groups:
            self._layout_fields(parent, controls, columns=1 if one_column else 2)
        self.action_buttons.set_columns(2 if one_column else 4)
        if header_stacked:
            self.header.controls.grid_configure(row=1, column=0, padx=0, pady=(14, 0), sticky="w")
        else:
            self.header.controls.grid_configure(row=0, column=1, padx=(24, 0), pady=0, sticky="ne")

    @staticmethod
    def _placeholder_action(action: str) -> None:
        print(t("general.placeholder_action", action=action))

    @staticmethod
    def _change_theme(value: str) -> None:
        ctk.set_appearance_mode("dark" if value == t("general.theme.dark") else "light")
