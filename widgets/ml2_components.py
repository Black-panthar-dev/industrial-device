"""Reusable presentation components for Milestone 2 configuration screens."""

from collections.abc import Callable, Sequence
from typing import Any, Literal

import customtkinter as ctk
from utils.responsive import wrap_label_to_width

from utils.theme import (
    COLOR_BORDER,
    COLOR_INFO,
    COLOR_INFO_SURFACE,
    COLOR_ON_PRIMARY,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_READONLY,
    COLOR_SUCCESS,
    COLOR_SUCCESS_SURFACE,
    COLOR_SURFACE,
    COLOR_SURFACE_ALT,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
    ThemeColor,
)
from widgets.form_controls import OutlineButton
from widgets.icons import create_icon


class PageHeader(ctk.CTkFrame):
    """Responsive page heading with an optional top-right control area."""

    def __init__(
        self,
        master: Any,
        title: str,
        subtitle: str,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("corner_radius", 0)
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        text_area = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        text_area.grid(row=0, column=0, sticky="ew")
        text_area.grid_columnconfigure(0, weight=1)
        self.title_label = ctk.CTkLabel(
            text_area,
            text=title,
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="ew")
        self.subtitle_label = ctk.CTkLabel(
            text_area,
            text=subtitle,
            font=ctk.CTkFont(size=14),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
            justify="left",
            wraplength=760,
        )
        self.subtitle_label.grid(row=1, column=0, pady=(5, 0), sticky="ew")
        wrap_label_to_width(self.subtitle_label)

        self.controls = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self._control_count = 0
        self._control_columns = 3
        self._controls: list[ctk.CTkBaseClass] = []

    def add_control(self, control: ctk.CTkBaseClass) -> None:
        """Place a control created with ``header.controls`` as its parent."""
        self._controls.append(control)
        self._control_count = len(self._controls)
        if self._control_count == 1:
            self.controls.grid(row=0, column=1, padx=(24, 0), sticky="ne")
        self._layout_controls()

    def set_control_columns(self, columns: int) -> None:
        """Reflow controls without recreating them when horizontal space is limited."""
        columns = max(1, columns)
        if columns == self._control_columns:
            return
        self._control_columns = columns
        self._layout_controls()

    def _layout_controls(self) -> None:
        for column in range(max(self._control_count, self._control_columns)):
            self.controls.grid_columnconfigure(column, weight=0)
        for index, control in enumerate(self._controls):
            row, column = divmod(index, self._control_columns)
            control.grid_configure(
                row=row,
                column=column,
                padx=(8 if column else 0, 0),
                pady=(8 if row else 0, 0),
                sticky="ew",
            )


class StatusPanel(ctk.CTkFrame):
    """Bordered status-card container intended for a side or reflowed panel."""

    def __init__(self, master: Any, title: str | None = None, **kwargs: Any) -> None:
        kwargs.setdefault("fg_color", COLOR_SURFACE)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", COLOR_BORDER)
        kwargs.setdefault("corner_radius", 10)
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        row = 0
        if title:
            self.title_label = ctk.CTkLabel(
                self,
                text=title,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=COLOR_TEXT,
                anchor="w",
            )
            self.title_label.grid(row=0, column=0, padx=20, pady=(18, 6), sticky="ew")
            row = 1

        self.body = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.body.grid(row=row, column=0, padx=20, pady=(8, 18), sticky="nsew")
        self.body.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(row, weight=1)


class StatusRow(ctk.CTkFrame):
    """Compact icon, label, and value row for status panels."""

    def __init__(
        self,
        master: Any,
        label: str,
        value: str,
        *,
        icon: str | None = None,
        value_color: ThemeColor = COLOR_TEXT,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("corner_radius", 0)
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)

        self.icon_label = ctk.CTkLabel(
            self,
            text="" if icon else "•",
            image=create_icon(icon, 16, COLOR_TEXT_MUTED) if icon else None,
            width=18,
            text_color=COLOR_TEXT_MUTED,
        )
        self.icon_label.grid(row=0, column=0, padx=(0, 8), pady=7)
        self.label_widget = ctk.CTkLabel(
            self, text=label, text_color=COLOR_TEXT_MUTED, anchor="w"
        )
        self.label_widget.grid(row=0, column=1, pady=7, sticky="ew")
        self.value_widget = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=value_color,
            anchor="e",
        )
        self.value_widget.grid(row=0, column=2, padx=(12, 0), pady=7, sticky="e")

    def set_value(self, value: str) -> None:
        self.value_widget.configure(text=value)


class MetricValue(ctk.CTkFrame):
    """Prominent read-only metric with a separate unit and optional label."""

    def __init__(
        self,
        master: Any,
        value: str,
        unit: str,
        *,
        label: str | None = None,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", COLOR_SURFACE_ALT)
        kwargs.setdefault("corner_radius", 8)
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        if label:
            self.label_widget = ctk.CTkLabel(
                self, text=label, text_color=COLOR_TEXT_MUTED, anchor="w"
            )
            self.label_widget.grid(row=0, column=0, columnspan=2, padx=16, pady=(12, 0), sticky="ew")
        value_row = 1 if label else 0
        self.value_widget = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLOR_PRIMARY,
            anchor="e",
        )
        self.value_widget.grid(row=value_row, column=0, padx=(16, 5), pady=(5, 14), sticky="e")
        self.unit_widget = ctk.CTkLabel(
            self,
            text=unit,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=COLOR_TEXT_MUTED,
            anchor="w",
        )
        self.unit_widget.grid(row=value_row, column=1, padx=(0, 16), pady=(11, 14), sticky="w")

    def set_value(self, value: str, unit: str | None = None) -> None:
        self.value_widget.configure(text=value)
        if unit is not None:
            self.unit_widget.configure(text=unit)


class SectionHeader(ctk.CTkFrame):
    """Number badge followed by a section title and optional description."""

    def __init__(
        self,
        master: Any,
        number: int | str,
        title: str,
        *,
        description: str | None = None,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("corner_radius", 0)
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        badge = ctk.CTkLabel(
            self,
            text=str(number),
            width=26,
            height=26,
            corner_radius=13,
            fg_color=COLOR_PRIMARY,
            text_color=COLOR_ON_PRIMARY,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        badge.grid(row=0, column=0, rowspan=2 if description else 1, padx=(0, 10), sticky="n")
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        )
        self.title_label.grid(row=0, column=1, sticky="ew")
        if description:
            self.description_label = ctk.CTkLabel(
                self,
                text=description,
                text_color=COLOR_TEXT_MUTED,
                anchor="w",
                justify="left",
                wraplength=720,
            )
            self.description_label.grid(row=1, column=1, pady=(3, 0), sticky="ew")
            wrap_label_to_width(self.description_label)


class ReadonlyField(ctk.CTkFrame):
    """Labeled, disabled-looking value field for generated or device data."""

    def __init__(
        self,
        master: Any,
        label: str,
        value: str = "",
        *,
        helper_text: str | None = None,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("corner_radius", 0)
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.label_widget = ctk.CTkLabel(
            self,
            text=label,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLOR_TEXT,
            anchor="w",
        )
        self.label_widget.grid(row=0, column=0, pady=(0, 3), sticky="ew")
        self.variable = ctk.StringVar(value=value)
        self.field = ctk.CTkEntry(
            self,
            textvariable=self.variable,
            state="disabled",
            height=36,
            corner_radius=7,
            fg_color=COLOR_READONLY,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT_MUTED,
        )
        self.field.grid(row=1, column=0, sticky="ew")
        if helper_text:
            self.helper_label = ctk.CTkLabel(
                self, text=helper_text, text_color=COLOR_TEXT_MUTED, anchor="w"
            )
            self.helper_label.grid(row=2, column=0, pady=(4, 0), sticky="ew")
            wrap_label_to_width(self.helper_label)

    def get(self) -> str:
        return self.variable.get()

    def set(self, value: str) -> None:
        self.variable.set(value)


class ActionButtonRow(ctk.CTkFrame):
    """Wrapping-friendly container that builds consistent outline actions."""

    def __init__(
        self,
        master: Any,
        actions: Sequence[tuple[str, Callable[[], None] | None]],
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("corner_radius", 0)
        super().__init__(master, **kwargs)
        self.buttons: list[OutlineButton] = []
        for _column, (text, command) in enumerate(actions):
            button = OutlineButton(self, text=text, command=command or (lambda: None))
            self.buttons.append(button)
        self.set_columns(max(1, len(self.buttons)))

    def set_columns(self, columns: int) -> None:
        """Reflow action buttons across the requested number of columns."""
        columns = max(1, min(columns, len(self.buttons) or 1))
        for column in range(max(len(self.buttons), columns)):
            self.grid_columnconfigure(column, weight=1 if column < columns else 0)
        for index, button in enumerate(self.buttons):
            row, column = divmod(index, columns)
            button.grid(
                row=row,
                column=column,
                padx=(0 if column == 0 else 6, 0),
                pady=(0 if row == 0 else 6, 0),
                sticky="ew",
            )


class InlineInfoBanner(ctk.CTkFrame):
    """Theme-aware blue or green inline message banner."""

    def __init__(
        self,
        master: Any,
        message: str,
        *,
        tone: Literal["info", "success"] = "info",
        **kwargs: Any,
    ) -> None:
        accent = COLOR_SUCCESS if tone == "success" else COLOR_INFO
        surface = COLOR_SUCCESS_SURFACE if tone == "success" else COLOR_INFO_SURFACE
        kwargs.setdefault("fg_color", surface)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("border_color", accent)
        kwargs.setdefault("corner_radius", 8)
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.indicator = ctk.CTkLabel(
            self,
            text="i" if tone == "info" else "✓",
            width=22,
            height=22,
            corner_radius=11,
            fg_color=accent,
            text_color=COLOR_ON_PRIMARY,
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.indicator.grid(row=0, column=0, padx=(12, 9), pady=12)
        self.message_label = ctk.CTkLabel(
            self,
            text=message,
            text_color=COLOR_TEXT,
            anchor="w",
            justify="left",
            wraplength=720,
        )
        self.message_label.grid(row=0, column=1, padx=(0, 12), pady=12, sticky="ew")
        wrap_label_to_width(self.message_label)


class RadioGroup(ctk.CTkFrame):
    """Labeled group of keyboard-focusable radio choices."""

    def __init__(
        self,
        master: Any,
        options: Sequence[tuple[str, str]],
        *,
        value: str | None = None,
        command: Callable[[], None] | None = None,
        orientation: Literal["horizontal", "vertical"] = "vertical",
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("corner_radius", 0)
        super().__init__(master, **kwargs)
        initial = value if value is not None else (options[0][1] if options else "")
        self.variable = ctk.StringVar(value=initial)
        self.buttons: list[ctk.CTkRadioButton] = []
        for index, (label, option_value) in enumerate(options):
            row = 0 if orientation == "horizontal" else index
            column = index if orientation == "horizontal" else 0
            self.grid_columnconfigure(column, weight=1)
            button = ctk.CTkRadioButton(
                self,
                text=label,
                value=option_value,
                variable=self.variable,
                command=command,
                width=max(95, 28 + len(label) * 5),
                radiobutton_width=18,
                radiobutton_height=18,
                border_color=COLOR_BORDER,
                fg_color=COLOR_PRIMARY,
                hover_color=COLOR_PRIMARY_HOVER,
                text_color=COLOR_TEXT,
                font=ctk.CTkFont(size=11),
            )
            button.grid(
                row=row,
                column=column,
                padx=(0, 6) if orientation == "horizontal" else 0,
                pady=5,
                sticky="w",
            )
            button._text_label.configure(takefocus=True)
            button._text_label.bind(
                "<space>", lambda _event, item=button: self._select_from_keyboard(item), add="+"
            )
            button._text_label.bind(
                "<Return>", lambda _event, item=button: self._select_from_keyboard(item), add="+"
            )
            button._text_label.bind(
                "<FocusIn>", lambda _event, item=button: self._show_radio_focus(item), add="+"
            )
            button._text_label.bind(
                "<FocusOut>", lambda _event, item=button: self._hide_radio_focus(item), add="+"
            )
            self.buttons.append(button)

    @staticmethod
    def _select_from_keyboard(button: ctk.CTkRadioButton) -> str:
        button.invoke()
        return "break"

    def get(self) -> str:
        return self.variable.get()

    def set(self, value: str) -> None:
        self.variable.set(value)

    def keyboard_focus_targets(self) -> list[Any]:
        return [button._text_label for button in self.buttons]

    @staticmethod
    def _show_radio_focus(button: ctk.CTkRadioButton) -> None:
        button._text_label.configure(
            highlightthickness=2,
            highlightcolor=button._apply_appearance_mode(COLOR_PRIMARY),
        )

    @staticmethod
    def _hide_radio_focus(button: ctk.CTkRadioButton) -> None:
        button._text_label.configure(highlightthickness=0)
