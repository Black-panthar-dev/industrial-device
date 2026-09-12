"""Milestone 2 Measurements configuration screen (GUI-only)."""

from typing import Any

import customtkinter as ctk

from services.translation_service import t
from utils.responsive import DebouncedResponsiveMixin
from utils.theme import COLOR_ON_PRIMARY, COLOR_PRIMARY, COLOR_SCROLLBAR, COLOR_SCROLLBAR_HOVER, COLOR_SUCCESS, COLOR_TEXT
from widgets.cards import SectionCard
from widgets.form_controls import CheckboxRow, LabeledDropdown, LabeledEntry, OutlineButton, PrimaryButton, ThemedComboBox, configure_focus_chain
from widgets.icons import create_icon
from widgets.ml2_components import ActionButtonRow, InlineInfoBanner, MetricValue, PageHeader, RadioGroup, ReadonlyField, SectionHeader, StatusPanel, StatusRow


class MeasurementsView(DebouncedResponsiveMixin, ctk.CTkFrame):
    """Configure dummy measurement options without device communication."""

    PANEL_REFLOW_WIDTH = 1120
    FORM_REFLOW_WIDTH = 720
    HEADER_REFLOW_WIDTH = 900
    RESIZE_DEBOUNCE_MS = 180

    def __init__(self, master: Any, **kwargs: Any) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._form_groups: list[tuple[ctk.CTkFrame, list[ctk.CTkBaseClass]]] = []
        self.focus_controls: list[Any] = []
        self._build_header()
        self._build_workspace()
        self.focus_targets = configure_focus_chain(self.focus_controls)
        self._initialize_responsive_layout()

    @classmethod
    def get_layout_mode(cls, scaled_width: int | float, widget_scaling: int | float = 1.0) -> tuple[bool, bool, bool]:
        width = scaled_width / max(float(widget_scaling), 0.01)
        return width < cls.PANEL_REFLOW_WIDTH, width < cls.FORM_REFLOW_WIDTH, width < cls.HEADER_REFLOW_WIDTH

    def _build_header(self) -> None:
        self.header = PageHeader(self, t("measurements.title"), t("measurements.subtitle"))
        self.header.grid(row=0, column=0, padx=30, pady=(24, 18), sticky="ew")
        self.theme_menu = ThemedComboBox(
            self.header.controls,
            values=[t("measurements.theme.light"), t("measurements.theme.dark")],
            width=108,
            command=self._change_theme,
        )
        self.theme_menu.set(t("measurements.theme.light"))
        self.header.add_control(self.theme_menu)
        self.export_button = OutlineButton(
            self.header.controls,
            text=t("measurements.export"),
            image=create_icon("download", 16, COLOR_PRIMARY),
            command=lambda: self._placeholder_action(t("measurements.export")),
        )
        self.header.add_control(self.export_button)
        self.import_button = PrimaryButton(
            self.header.controls,
            text=t("measurements.import"),
            image=create_icon("upload", 16, COLOR_ON_PRIMARY),
            command=lambda: self._placeholder_action(t("measurements.import")),
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
        self._build_voltage_section(0)
        self._build_current_section(1)
        self._build_processing_section(2)
        self._build_calculated_section(3)
        self._build_status_section(4)
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
        fields.grid_columnconfigure((0, 1), weight=1, uniform=f"measurements_{row}")
        return fields

    def _register_fields(self, parent: ctk.CTkFrame, controls: list[ctk.CTkBaseClass]) -> None:
        self._form_groups.append((parent, controls))
        self._layout_fields(parent, controls, 2)

    @staticmethod
    def _layout_fields(parent: ctk.CTkFrame, controls: list[ctk.CTkBaseClass], columns: int) -> None:
        for column in (0, 1):
            parent.grid_columnconfigure(column, weight=1 if column < columns else 0)
        for index, control in enumerate(controls):
            row, column = divmod(index, columns)
            padding = (0, 8) if column == 0 and columns > 1 else ((8, 0) if column else 0)
            control.grid(row=row, column=column, padx=padding, pady=(0, 13), sticky="ew")

    def _calibration_card(self, parent: ctk.CTkFrame, offset_label: str, offset_value: str | None = None) -> tuple[SectionCard, list[Any]]:
        card = SectionCard(parent, title=t("measurements.calibration"), compact=True)
        card.body.grid_columnconfigure((0, 1), weight=1, uniform="calibration")
        offset = LabeledEntry(card.body, offset_label, value=offset_value or t("measurements.values.offset"))
        gain = LabeledEntry(card.body, t("measurements.gain"), value=t("measurements.values.gain"))
        offset.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        gain.grid(row=0, column=1, padx=(6, 0), sticky="ew")
        return card, [offset, gain]

    def _build_voltage_section(self, row: int) -> None:
        fields = self._new_section(row, 1, "measurements.sections.voltage.title", "measurements.sections.voltage.subtitle")
        enabled = CheckboxRow(fields, t("measurements.enable_voltage"), checked=True)
        input_range = ReadonlyField(fields, t("measurements.input_range"), t("measurements.values.voltage_range"))
        calibration, calibration_controls = self._calibration_card(fields, t("measurements.offset_v"))
        self.live_voltage = MetricValue(fields, t("measurements.values.live_voltage"), t("measurements.units.volts"), label=t("measurements.live_voltage"))
        self._register_fields(fields, [enabled, input_range, calibration, self.live_voltage])
        self.focus_controls.extend((enabled, *calibration_controls))

    def _build_current_section(self, row: int) -> None:
        fields = self._new_section(row, 2, "measurements.sections.current.title", "measurements.sections.current.subtitle")
        enabled = CheckboxRow(fields, t("measurements.enable_current"), checked=True)
        modes = RadioGroup(
            fields,
            [(t("measurements.mode.internal"), "internal"), (t("measurements.mode.external"), "external"), (t("measurements.mode.auto"), "auto")],
            value="internal",
            orientation="horizontal",
        )
        internal = SectionCard(fields, title=t("measurements.internal_shunt"), compact=True)
        internal.body.grid_columnconfigure(0, weight=1)
        internal_range = ReadonlyField(internal.body, t("measurements.range_max"), t("measurements.values.internal_range"))
        internal_range.grid(row=0, column=0, pady=(0, 10), sticky="ew")
        internal_calibration, internal_controls = self._calibration_card(internal.body, t("measurements.offset_ma"))
        internal_calibration.grid(row=1, column=0, sticky="ew")
        external = SectionCard(fields, title=t("measurements.external_shunt"), compact=True)
        external.body.grid_columnconfigure((0, 1), weight=1, uniform="external")
        rated = LabeledDropdown(external.body, t("measurements.rated_current"), [t("measurements.options.current.10a"), t("measurements.options.current.20a"), t("measurements.options.current.50a")], value=t("measurements.options.current.10a"))
        voltage = LabeledDropdown(external.body, t("measurements.shunt_voltage"), [t("measurements.options.shunt_voltage.50mv"), t("measurements.options.shunt_voltage.100mv")], value=t("measurements.options.shunt_voltage.100mv"))
        resistance = ReadonlyField(external.body, t("measurements.shunt_resistance"), t("measurements.values.shunt_resistance"))
        rated.grid(row=0, column=0, padx=(0, 6), pady=(0, 10), sticky="ew")
        voltage.grid(row=0, column=1, padx=(6, 0), pady=(0, 10), sticky="ew")
        resistance.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        external_calibration, external_controls = self._calibration_card(external.body, t("measurements.offset_ma"))
        external_calibration.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.live_current = MetricValue(fields, t("measurements.values.live_current"), t("measurements.units.milliamps"), label=t("measurements.live_current"))
        self._register_fields(fields, [enabled, modes, internal, external, self.live_current])
        self.focus_controls.extend((enabled, modes, *internal_controls, rated, voltage, *external_controls))

    def _build_processing_section(self, row: int) -> None:
        fields = self._new_section(row, 3, "measurements.sections.processing.title", "measurements.sections.processing.subtitle")
        interval = LabeledDropdown(fields, t("measurements.interval"), [t("measurements.options.interval.1_second"), t("measurements.options.interval.5_seconds"), t("measurements.options.interval.10_seconds")], value=t("measurements.options.interval.1_second"))
        averaging = LabeledDropdown(fields, t("measurements.averaging"), [t("measurements.options.averaging.1"), t("measurements.options.averaging.4"), t("measurements.options.averaging.8"), t("measurements.options.averaging.16")], value=t("measurements.options.averaging.8"))
        filter_type = LabeledDropdown(fields, t("measurements.filter_type"), [t("measurements.options.filter.moving_average"), t("measurements.options.filter.median"), t("measurements.options.filter.none")], value=t("measurements.options.filter.moving_average"))
        threshold = LabeledEntry(fields, t("measurements.zero_threshold"), value=t("measurements.values.zero_threshold"), helper_text=t("measurements.zero_threshold.help"))
        self._register_fields(fields, [interval, averaging, filter_type, threshold])
        self.focus_controls.extend((interval, averaging, filter_type, threshold))

    def _build_calculated_section(self, row: int) -> None:
        fields = self._new_section(row, 4, "measurements.sections.calculated.title", "measurements.sections.calculated.subtitle")
        banner = InlineInfoBanner(fields, t("measurements.calculated.banner"))
        enabled = CheckboxRow(fields, t("measurements.enable_calculated"), checked=True)
        reset = ActionButtonRow(fields, [(t("measurements.reset_counters"), lambda: self._placeholder_action(t("measurements.reset_counters")))])
        self._register_fields(fields, [banner, enabled, reset])
        self.focus_controls.extend((enabled, *reset.buttons))

    def _build_status_section(self, row: int) -> None:
        fields = self._new_section(row, 5, "measurements.sections.status.title", "measurements.sections.status.subtitle")
        values = [
            ("measurements.measurement_status", t("measurements.values.ok")), ("measurements.last_update", t("measurements.values.last_update_full")),
            ("measurements.engine", t("measurements.values.running")), ("measurements.overrange", t("measurements.values.no")), ("measurements.sensor_error", t("measurements.values.no")),
        ]
        self._register_fields(fields, [ReadonlyField(fields, t(key), value) for key, value in values])

    def _status_panel(self, row: int, title_key: str, values: list[tuple[str, str]]) -> None:
        panel = StatusPanel(self.right_panel, t(title_key))
        panel.grid(row=row, column=0, pady=(0, 14), sticky="ew")
        for item_row, (label_key, value) in enumerate(values):
            if title_key == "measurements.live_panel.title":
                value_color = COLOR_PRIMARY
            elif title_key == "measurements.status_panel.title" and item_row == 0:
                value_color = COLOR_SUCCESS
            else:
                value_color = COLOR_TEXT
            StatusRow(panel.body, t(label_key), value, value_color=value_color).grid(row=item_row, column=0, sticky="ew")

    def _build_right_panel(self) -> None:
        self._status_panel(0, "measurements.live_panel.title", [
            ("measurements.voltage", t("measurements.values.voltage_display")), ("measurements.current", t("measurements.values.current_display")),
            ("measurements.power", t("measurements.values.power_display")), ("measurements.energy", t("measurements.values.energy_display")), ("measurements.charge", t("measurements.values.charge_display")),
        ])
        self._status_panel(1, "measurements.status_panel.title", [
            ("measurements.status", t("measurements.values.ok")), ("measurements.last_update", t("measurements.values.last_update_time")),
            ("measurements.overrange", t("measurements.values.no")), ("measurements.sensor_error", t("measurements.values.no")),
        ])
        self._status_panel(2, "measurements.information.title", [
            ("measurements.source", t("measurements.values.device")), ("measurements.interval", t("measurements.values.interval_short")),
            ("measurements.averaging", t("measurements.options.averaging.8")), ("measurements.filter", t("measurements.options.filter.moving_average")),
        ])

    def _apply_layout_mode(self, mode: tuple[bool, ...]) -> None:
        panel_below, one_column, header_stacked = mode
        self.header.set_control_columns(2 if one_column else 3)
        if panel_below:
            self.right_panel.grid_configure(row=1, column=0, padx=30, pady=(0, 30), sticky="ew")
            self.workspace.grid_columnconfigure(1, minsize=0, weight=0)
        else:
            self.right_panel.grid_configure(row=0, column=1, padx=(0, 30), pady=(0, 30), sticky="new")
            self.workspace.grid_columnconfigure(1, minsize=285, weight=0)
        for parent, controls in self._form_groups:
            self._layout_fields(parent, controls, 1 if one_column else 2)
        if header_stacked:
            self.header.controls.grid_configure(row=1, column=0, padx=0, pady=(14, 0), sticky="w")
        else:
            self.header.controls.grid_configure(row=0, column=1, padx=(24, 0), pady=0, sticky="ne")

    @staticmethod
    def _placeholder_action(action: str) -> None:
        print(t("measurements.placeholder_action", action=action))

    @staticmethod
    def _change_theme(value: str) -> None:
        ctk.set_appearance_mode("dark" if value == t("measurements.theme.dark") else "light")
