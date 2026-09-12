"""Milestone 2 Communications configuration screen (GUI-only)."""

from typing import Any

import customtkinter as ctk

from services.translation_service import t
from utils.theme import COLOR_ON_PRIMARY, COLOR_PRIMARY, COLOR_SCROLLBAR, COLOR_SCROLLBAR_HOVER, COLOR_TEXT
from widgets.cards import SectionCard
from widgets.form_controls import CheckboxRow, LabeledDropdown, LabeledEntry, OutlineButton, PrimaryButton, ThemedComboBox, configure_focus_chain, enable_button_keyboard
from widgets.icons import create_icon
from widgets.ml2_components import InlineInfoBanner, PageHeader, ReadonlyField, SectionHeader, StatusPanel, StatusRow


class CommunicationsView(ctk.CTkFrame):
    """Configure dummy communication interfaces without protocol logic."""

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
        self.header = PageHeader(self, t("communications.title"), t("communications.subtitle"))
        self.header.grid(row=0, column=0, padx=30, pady=(24, 18), sticky="ew")
        self.theme_menu = ThemedComboBox(
            self.header.controls,
            values=[t("communications.theme.light"), t("communications.theme.dark")],
            width=108,
            command=self._change_theme,
        )
        self.theme_menu.set(t("communications.theme.light"))
        self.header.add_control(self.theme_menu)
        self.export_button = OutlineButton(
            self.header.controls,
            text=t("communications.export"),
            image=create_icon("download", 16, COLOR_PRIMARY),
            command=lambda: self._placeholder_action(t("communications.export")),
        )
        self.header.add_control(self.export_button)
        self.import_button = PrimaryButton(
            self.header.controls,
            text=t("communications.import"),
            image=create_icon("upload", 16, COLOR_ON_PRIMARY),
            command=lambda: self._placeholder_action(t("communications.import")),
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
        self.workspace.grid_columnconfigure(1, weight=0, minsize=300)
        self.main_content = ctk.CTkFrame(self.workspace, fg_color="transparent", corner_radius=0)
        self.main_content.grid(row=0, column=0, padx=(30, 14), pady=(0, 30), sticky="nsew")
        self.main_content.grid_columnconfigure(0, weight=1)
        self._build_rs485_section(0)
        self._build_rs232_section(1)
        self._build_usb_section(2)
        self._build_module_section(3)
        self.right_panel = ctk.CTkFrame(self.workspace, fg_color="transparent", corner_radius=0)
        self.right_panel.grid(row=0, column=1, padx=(0, 30), pady=(0, 30), sticky="new")
        self.right_panel.grid_columnconfigure(0, weight=1)
        self._build_right_panel()

    def _new_section(self, row: int, number: int, title_key: str, subtitle_key: str) -> ctk.CTkFrame:
        card = SectionCard(self.main_content)
        card.grid(row=row, column=0, pady=(0, 14), sticky="ew")
        SectionHeader(card.body, number, t(title_key), description=t(subtitle_key)).grid(row=0, column=0, pady=(0, 16), sticky="ew")
        fields = ctk.CTkFrame(card.body, fg_color="transparent", corner_radius=0)
        fields.grid(row=1, column=0, sticky="ew")
        fields.grid_columnconfigure((0, 1), weight=1, uniform=f"communications_{row}")
        return fields

    def _register_fields(self, parent: ctk.CTkFrame, controls: list[ctk.CTkBaseClass]) -> None:
        self._form_groups.append((parent, controls))
        self._layout_fields(parent, controls, 2)

    @staticmethod
    def _layout_fields(parent: ctk.CTkFrame, controls: list[ctk.CTkBaseClass], columns: int) -> None:
        uniform_group = "" if columns == 1 else "communications_reflow"
        for column in (0, 1):
            parent.grid_columnconfigure(
                column,
                weight=1 if column < columns else 0,
                uniform=uniform_group,
            )
        for index, control in enumerate(controls):
            row, column = divmod(index, columns)
            padding = (0, 8) if column == 0 and columns > 1 else ((8, 0) if column else 0)
            control.grid(row=row, column=column, padx=padding, pady=(0, 13), sticky="ew")

    def _interface_status(self, parent: Any, status_label: str, packets: tuple[str, str]) -> StatusPanel:
        panel = StatusPanel(parent, t("communications.interface_status"))
        values = [
            (status_label, t("communications.values.ready")),
            ("communications.rx_packets", packets[0]),
            ("communications.tx_packets", packets[1]),
            ("communications.errors", t("communications.values.zero")),
        ]
        for row, (key, value) in enumerate(values):
            StatusRow(panel.body, t(key), value, value_color=COLOR_PRIMARY if row == 0 else COLOR_TEXT).grid(row=row, column=0, sticky="ew")
        return panel

    def _build_rs485_section(self, row: int) -> None:
        fields = self._new_section(row, 1, "communications.sections.rs485.title", "communications.sections.rs485.subtitle")
        enabled = CheckboxRow(fields, t("communications.enable_rs485"), checked=True)
        address = LabeledEntry(fields, t("communications.modbus_address"), value=t("communications.values.modbus_address"))
        baud = LabeledDropdown(fields, t("communications.baudrate"), [t("communications.options.baudrate.9600"), t("communications.options.baudrate.19200"), t("communications.options.baudrate.57600"), t("communications.options.baudrate.115200")], value=t("communications.options.baudrate.115200"))
        data = LabeledDropdown(fields, t("communications.data_bits"), [t("communications.options.data_bits.7"), t("communications.options.data_bits.8")], value=t("communications.options.data_bits.8"))
        parity = LabeledDropdown(fields, t("communications.parity"), [t("communications.options.parity.none"), t("communications.options.parity.even"), t("communications.options.parity.odd")], value=t("communications.options.parity.none"))
        stop = LabeledDropdown(fields, t("communications.stop_bits"), [t("communications.options.stop_bits.1"), t("communications.options.stop_bits.2")], value=t("communications.options.stop_bits.1"))
        timeout = LabeledEntry(fields, t("communications.response_timeout"), value=t("communications.values.response_timeout"), helper_text=t("communications.response_timeout.help"))
        status = self._interface_status(fields, "communications.rs485_status", (t("communications.values.rs485_rx"), t("communications.values.rs485_tx")))
        self._register_fields(fields, [enabled, address, baud, data, parity, stop, timeout, status])
        self.focus_controls.extend((enabled, address, baud, data, parity, stop, timeout))

    def _build_rs232_section(self, row: int) -> None:
        fields = self._new_section(row, 2, "communications.sections.rs232.title", "communications.sections.rs232.subtitle")
        enabled = CheckboxRow(fields, t("communications.enable_rs232"), checked=True)
        baud = LabeledDropdown(fields, t("communications.baudrate"), [t("communications.options.baudrate.9600"), t("communications.options.baudrate.19200"), t("communications.options.baudrate.57600"), t("communications.options.baudrate.115200")], value=t("communications.options.baudrate.115200"))
        data = LabeledDropdown(fields, t("communications.data_bits"), [t("communications.options.data_bits.7"), t("communications.options.data_bits.8")], value=t("communications.options.data_bits.8"))
        parity = LabeledDropdown(fields, t("communications.parity"), [t("communications.options.parity.none"), t("communications.options.parity.even"), t("communications.options.parity.odd")], value=t("communications.options.parity.none"))
        stop = LabeledDropdown(fields, t("communications.stop_bits"), [t("communications.options.stop_bits.1"), t("communications.options.stop_bits.2")], value=t("communications.options.stop_bits.1"))
        flow = LabeledDropdown(fields, t("communications.flow_control"), [t("communications.options.flow.none"), t("communications.options.flow.rts_cts"), t("communications.options.flow.xon_xoff")], value=t("communications.options.flow.none"))
        status = self._interface_status(fields, "communications.rs232_status", (t("communications.values.rs232_rx"), t("communications.values.rs232_tx")))
        self._register_fields(fields, [enabled, baud, data, parity, stop, flow, status])
        self.focus_controls.extend((enabled, baud, data, parity, stop, flow))

    def _build_usb_section(self, row: int) -> None:
        fields = self._new_section(row, 3, "communications.sections.usb.title", "communications.sections.usb.subtitle")
        controls: list[ctk.CTkBaseClass] = [
            ReadonlyField(fields, t("communications.usb_status"), t("communications.values.connected")),
            ReadonlyField(fields, t("communications.port"), t("communications.values.usb_port")),
            ReadonlyField(fields, t("communications.mode"), t("communications.values.configuration")),
            ReadonlyField(fields, t("communications.usb_serial"), t("communications.values.usb_serial")),
            InlineInfoBanner(fields, t("communications.usb.banner")),
        ]
        self._register_fields(fields, controls)

    def _build_module_section(self, row: int) -> None:
        fields = self._new_section(row, 4, "communications.sections.module.title", "communications.sections.module.subtitle")
        module_info = StatusPanel(fields, t("communications.module_information"))
        for item_row, (key, value) in enumerate([
            ("communications.detected_module", t("communications.values.module")), ("communications.module_status", t("communications.values.connected")),
            ("communications.firmware_version", t("communications.values.module_firmware")), ("communications.imei", t("communications.values.imei")),
        ]):
            StatusRow(module_info.body, t(key), value).grid(row=item_row, column=0, sticky="ew")

        settings = SectionCard(fields)
        settings.body.grid_columnconfigure((0, 1), weight=1, uniform="four_g")
        self.module_tabs = ctk.CTkSegmentedButton(
            settings.body,
            values=[t("communications.4g_settings"), t("communications.module_information")],
            selected_color=COLOR_PRIMARY,
            selected_hover_color=COLOR_PRIMARY,
            command=lambda value: self._placeholder_action(value),
        )
        self.module_tabs.set(t("communications.4g_settings"))
        self.module_tabs.grid(row=0, column=0, columnspan=2, pady=(0, 14), sticky="ew")
        for button in self.module_tabs._buttons_dict.values():
            enable_button_keyboard(button)
            self.focus_controls.append(button)

        apn = LabeledEntry(settings.body, t("communications.apn"), value=t("communications.values.apn"))
        username = LabeledEntry(settings.body, t("communications.username"), placeholder_text=t("communications.username.placeholder"))
        password = LabeledEntry(settings.body, t("communications.password"), value=t("communications.values.password"), show="*")
        pin = LabeledEntry(settings.body, t("communications.pin"), value=t("communications.values.pin"), show="*")
        network = LabeledDropdown(settings.body, t("communications.network_mode"), [t("communications.options.network.auto"), t("communications.options.network.4g"), t("communications.options.network.3g")], value=t("communications.options.network.auto"))
        operator = LabeledDropdown(settings.body, t("communications.preferred_operator"), [t("communications.options.operator.auto"), t("communications.values.operator")], value=t("communications.options.operator.auto"))
        signal = ReadonlyField(settings.body, t("communications.signal_strength"), t("communications.values.signal_strength"))
        registration = ReadonlyField(settings.body, t("communications.registration_status"), t("communications.values.registration"))
        inputs = [apn, username, password, pin, network, operator, signal, registration]
        for index, control in enumerate(inputs):
            input_row, column = divmod(index, 2)
            control.grid(row=input_row + 1, column=column, padx=(0, 6) if column == 0 else (6, 0), pady=(0, 10), sticky="ew")
        InlineInfoBanner(settings.body, t("communications.4g.banner")).grid(row=5, column=0, columnspan=2, sticky="ew")
        self.focus_controls.extend((apn, username, password, pin, network, operator))
        self._register_fields(fields, [module_info, settings])

    def _status_panel(self, row: int, title_key: str, values: list[tuple[str, str]]) -> None:
        panel = StatusPanel(self.right_panel, t(title_key))
        panel.grid(row=row, column=0, pady=(0, 14), sticky="ew")
        for item_row, (label_key, value) in enumerate(values):
            StatusRow(panel.body, t(label_key), value).grid(row=item_row, column=0, sticky="ew")

    def _build_right_panel(self) -> None:
        self._status_panel(0, "communications.status_panel.title", [
            ("communications.rs485_modbus", t("communications.values.ready")), ("communications.rs232", t("communications.values.ready")),
            ("communications.usb", t("communications.values.connected")), ("communications.expansion_module", t("communications.values.module_connected")),
        ])
        self._status_panel(1, "communications.network_status.title", [
            ("communications.operator", t("communications.values.operator")), ("communications.signal_strength", t("communications.values.signal_strength")),
            ("communications.network_type", t("communications.values.network_type")), ("communications.ip_address", t("communications.values.ip_address")),
            ("communications.internet", t("communications.values.available")), ("communications.last_communication", t("communications.values.last_communication")),
        ])
        self._status_panel(2, "communications.configuration_status.title", [
            ("communications.last_read", t("communications.values.last_read")), ("communications.last_written", t("communications.values.last_written")),
            ("communications.configuration_source", t("communications.values.device")),
        ])
        InlineInfoBanner(self.right_panel, t("communications.changes.banner")).grid(row=3, column=0, sticky="ew")

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
            self.workspace.grid_columnconfigure(1, minsize=300, weight=0)
        for parent, controls in self._form_groups:
            self._layout_fields(parent, controls, 1 if one_column else 2)
        if header_stacked:
            self.header.controls.grid_configure(row=1, column=0, padx=0, pady=(14, 0), sticky="w")
        else:
            self.header.controls.grid_configure(row=0, column=1, padx=(24, 0), pady=0, sticky="ne")

    @staticmethod
    def _placeholder_action(action: str) -> None:
        print(t("communications.placeholder_action", action=action))

    @staticmethod
    def _change_theme(value: str) -> None:
        ctk.set_appearance_mode("dark" if value == t("communications.theme.dark") else "light")
