from collections.abc import Callable, Sequence
import sys
from typing import Any

import customtkinter as ctk

from utils.theme import (
    COLOR_ACTIVE,
    COLOR_BORDER,
    COLOR_DROPDOWN_HOVER,
    COLOR_HOVER,
    COLOR_ON_PRIMARY,
    COLOR_PRIMARY,
    COLOR_PRIMARY_HOVER,
    COLOR_SURFACE,
    COLOR_SURFACE_ALT,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
    TRANSPARENT_COLOR_KEY,
)


class _ModernComboPopup(ctk.CTkToplevel):
    """Rounded CustomTkinter popup used instead of the native Tk menu."""

    ITEM_HEIGHT = 36
    ITEM_GAP = 2
    PADDING = 4

    def __init__(self, owner: "ThemedComboBox") -> None:
        popup_background = (
            TRANSPARENT_COLOR_KEY if sys.platform.startswith("win") else COLOR_BORDER
        )
        super().__init__(owner, fg_color=popup_background)
        self.owner = owner
        self.overrideredirect(True)
        self.transient(owner.winfo_toplevel())
        self.attributes("-topmost", True)
        if sys.platform.startswith("win"):
            self.wm_attributes("-transparentcolor", TRANSPARENT_COLOR_KEY)

        values = list(owner.cget("values"))
        popup_width = max(150, round(owner.winfo_width() / owner._get_widget_scaling()))
        popup_height = (
            self.PADDING * 2
            + len(values) * self.ITEM_HEIGHT
            + max(0, len(values) - 1) * self.ITEM_GAP
        )
        x = owner.winfo_rootx()
        below_y = owner.winfo_rooty() + owner.winfo_height() + 4
        above_y = owner.winfo_rooty() - round(
            popup_height * owner._get_widget_scaling()
        ) - 4
        physical_height = round(popup_height * owner._get_widget_scaling())
        y = above_y if below_y + physical_height > owner.winfo_screenheight() else below_y
        self.geometry(f"{popup_width}x{popup_height}+{x}+{max(0, y)}")

        container = ctk.CTkFrame(
            self,
            fg_color=COLOR_SURFACE,
            border_color=COLOR_BORDER,
            border_width=1,
            corner_radius=8,
        )
        container.pack(fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)

        selected_value = owner.get()
        self.buttons: list[ctk.CTkButton] = []
        self.active_index = 0
        for row, value in enumerate(values):
            selected = value == selected_value
            button = ctk.CTkButton(
                container,
                text=value,
                height=self.ITEM_HEIGHT,
                corner_radius=5,
                fg_color=COLOR_ACTIVE if selected else "transparent",
                hover_color=COLOR_DROPDOWN_HOVER,
                text_color=COLOR_PRIMARY if selected else COLOR_TEXT,
                font=ctk.CTkFont(size=13, weight="bold" if selected else "normal"),
                anchor="w",
                command=lambda item=value: self._select(item),
            )
            button.grid(
                row=row,
                column=0,
                padx=self.PADDING,
                pady=(
                    self.PADDING if row == 0 else self.ITEM_GAP,
                    self.PADDING if row == len(values) - 1 else 0,
                ),
                sticky="ew",
            )
            enable_button_keyboard(button)
            target = button._canvas
            target.bind("<Up>", lambda _event, i=row: self._move_focus(i - 1), add="+")
            target.bind("<Down>", lambda _event, i=row: self._move_focus(i + 1), add="+")
            target.bind("<Escape>", lambda _event: self.close(), add="+")
            self.buttons.append(button)
            if selected:
                self.active_index = row

        self.bind("<Escape>", lambda _event: self.close())
        self.bind("<FocusOut>", self._schedule_focus_check)
        self.after_idle(self._finish_opening)

    def _finish_opening(self) -> None:
        if self.winfo_exists():
            self.lift()
            self._focus_active()

    def _move_focus(self, index: int) -> str:
        self.active_index = index % len(self.buttons)
        self._focus_active()
        return "break"

    def _focus_active(self) -> None:
        if self.buttons:
            self.buttons[self.active_index]._canvas.focus_force()

    def _schedule_focus_check(self, _event: Any = None) -> None:
        self.after(80, self._close_if_focus_left)

    def _close_if_focus_left(self) -> None:
        if not self.winfo_exists():
            return
        focused = self.focus_get()
        if focused is None or not str(focused).startswith(str(self)):
            self.close()

    def _select(self, value: str) -> None:
        self.owner._dropdown_callback(value)
        self.close()
        if self.owner.winfo_exists():
            self.owner.focus_set()

    def close(self) -> None:
        if self.owner._modern_popup is self:
            self.owner._modern_popup = None
        if self.winfo_exists():
            self.destroy()


class ThemedComboBox(ctk.CTkComboBox):
    """Application ComboBox with consistent closed and dropdown styling."""

    def __init__(self, master: Any, **kwargs: Any) -> None:
        kwargs.setdefault("height", 36)
        kwargs.setdefault("corner_radius", 7)
        kwargs.setdefault("fg_color", COLOR_SURFACE)
        kwargs.setdefault("border_color", COLOR_BORDER)
        kwargs.setdefault("border_width", 1)
        kwargs.setdefault("button_color", COLOR_SURFACE_ALT)
        kwargs.setdefault("button_hover_color", COLOR_DROPDOWN_HOVER)
        kwargs.setdefault("text_color", COLOR_TEXT)
        kwargs.setdefault("dropdown_fg_color", COLOR_SURFACE)
        kwargs.setdefault("dropdown_hover_color", COLOR_DROPDOWN_HOVER)
        kwargs.setdefault("dropdown_text_color", COLOR_TEXT)
        kwargs.setdefault("font", ctk.CTkFont(size=13))
        kwargs.setdefault("dropdown_font", ctk.CTkFont(size=13))
        kwargs.setdefault("state", "readonly")
        super().__init__(master, **kwargs)
        self._modern_popup: _ModernComboPopup | None = None
        self._entry.configure(takefocus=True)
        self._entry.bind("<Return>", self._open_from_keyboard, add="+")
        self._entry.bind("<KP_Enter>", self._open_from_keyboard, add="+")
        self._entry.bind("<space>", self._open_from_keyboard, add="+")
        self._entry.bind("<Down>", self._open_from_keyboard, add="+")
        self._entry.bind("<Escape>", self._close_from_keyboard, add="+")

    def _open_from_keyboard(self, _event: Any = None) -> str:
        self._open_dropdown_menu()
        return "break"

    def _close_from_keyboard(self, _event: Any = None) -> str:
        if self._modern_popup is not None:
            self._modern_popup.close()
        return "break"

    def _open_dropdown_menu(self) -> None:
        """Open the application popup instead of CustomTkinter's Tk menu."""
        if self._modern_popup is not None and self._modern_popup.winfo_exists():
            self._modern_popup.close()
            return
        self._modern_popup = _ModernComboPopup(self)

    def destroy(self) -> None:
        if self._modern_popup is not None and self._modern_popup.winfo_exists():
            self._modern_popup.close()
        super().destroy()

    def keyboard_focus_target(self) -> Any:
        return self._entry


def enable_button_keyboard(button: ctk.CTkButton) -> ctk.CTkButton:
    """Make a CustomTkinter button focusable and Enter/Space activatable."""
    if getattr(button, "_keyboard_activation_enabled", False):
        return button
    button._keyboard_activation_enabled = True
    target = button._canvas
    target.configure(takefocus=True)

    def show_focus(_event: Any = None) -> None:
        target.configure(
            highlightthickness=2,
            highlightcolor=button._apply_appearance_mode(COLOR_PRIMARY),
        )

    def hide_focus(_event: Any = None) -> None:
        target.configure(highlightthickness=0)

    def activate(_event: Any = None) -> str:
        button.invoke()
        return "break"

    target.bind("<Return>", activate, add="+")
    target.bind("<KP_Enter>", activate, add="+")
    target.bind("<space>", activate, add="+")
    target.bind("<FocusIn>", show_focus, add="+")
    target.bind("<FocusOut>", hide_focus, add="+")
    return button


def keyboard_focus_target(control: Any) -> Any:
    """Return the native focusable child used by a reusable control."""
    accessor = getattr(control, "keyboard_focus_target", None)
    if accessor is not None:
        return accessor()
    if isinstance(control, ctk.CTkButton):
        enable_button_keyboard(control)
        return control._canvas
    raise TypeError(f"Unsupported keyboard control: {type(control).__name__}")


def configure_focus_chain(controls: Sequence[Any]) -> list[Any]:
    """Bind an explicit, wrapping Tab/Shift+Tab order for a control sequence."""
    targets: list[Any] = []
    for control in controls:
        multiple_accessor = getattr(control, "keyboard_focus_targets", None)
        if multiple_accessor is not None:
            targets.extend(multiple_accessor())
        else:
            targets.append(keyboard_focus_target(control))
    if not targets:
        return targets

    def move(index: int) -> str:
        targets[index % len(targets)].focus_set()
        return "break"

    for index, target in enumerate(targets):
        target.configure(takefocus=True)
        target.bind("<Tab>", lambda _event, i=index: move(i + 1), add="+")
        target.bind("<Shift-Tab>", lambda _event, i=index: move(i - 1), add="+")
        target.bind("<ISO_Left_Tab>", lambda _event, i=index: move(i - 1), add="+")
    return targets


class _LabeledControl(ctk.CTkFrame):
    """Shared label and helper-text layout for form controls."""

    def __init__(
        self,
        master: Any,
        label: str,
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
            height=16,
        )
        self.label_widget.grid(row=0, column=0, pady=(0, 3), sticky="ew")
        self._control_row = 1

        if helper_text:
            self.helper_label = ctk.CTkLabel(
                self,
                text=helper_text,
                font=ctk.CTkFont(size=10),
                text_color=COLOR_TEXT_MUTED,
                anchor="w",
                height=14,
            )
            self.helper_label.grid(row=2, column=0, pady=(5, 0), sticky="ew")


class LabeledDropdown(_LabeledControl):
    """A consistently styled dropdown with label and optional helper text."""

    def __init__(
        self,
        master: Any,
        label: str,
        values: Sequence[str],
        *,
        value: str | None = None,
        helper_text: str | None = None,
        command: Callable[[str], None] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, label, helper_text, **kwargs)
        dropdown_values = list(values)
        self.dropdown = ThemedComboBox(
            self,
            values=dropdown_values,
            command=command,
        )
        self.dropdown.grid(row=self._control_row, column=0, sticky="ew")
        if value is not None:
            self.dropdown.set(value)

    def get(self) -> str:
        return self.dropdown.get()

    def set(self, value: str) -> None:
        self.dropdown.set(value)

    def keyboard_focus_target(self) -> Any:
        return self.dropdown.keyboard_focus_target()


class LabeledEntry(_LabeledControl):
    """A consistently styled text entry with label and optional helper text."""

    def __init__(
        self,
        master: Any,
        label: str,
        *,
        value: str = "",
        placeholder_text: str = "",
        helper_text: str | None = None,
        textvariable: Any | None = None,
        show: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(master, label, helper_text, **kwargs)
        self.entry = ctk.CTkEntry(
            self,
            height=32,
            corner_radius=7,
            fg_color=COLOR_SURFACE,
            border_color=COLOR_BORDER,
            text_color=COLOR_TEXT,
            placeholder_text=placeholder_text,
            textvariable=textvariable,
            show=show,
        )
        self.entry.grid(row=self._control_row, column=0, sticky="ew")
        self.entry._entry.configure(takefocus=True)
        self.entry._entry.bind(
            "<KeyPress>", self._prepare_keyboard_input, add="+"
        )
        if value and textvariable is None:
            self.entry.insert(0, value)

    def get(self) -> str:
        return self.entry.get()

    def set(self, value: str) -> None:
        self.entry.set(value)

    def insert(self, value: str) -> None:
        """Insert text through CTkEntry's placeholder-aware public API."""
        self.entry.insert("end", value)

    def keyboard_focus_target(self) -> Any:
        return self.entry._entry

    def _prepare_keyboard_input(self, _event: Any = None) -> None:
        # CTkEntry normally clears placeholders on FocusIn. Doing it again on
        # KeyPress also covers generated input and unusual focus transitions.
        self.entry._deactivate_placeholder()


class CheckboxRow(ctk.CTkFrame):
    """A checkbox with an optional supporting description."""

    def __init__(
        self,
        master: Any,
        text: str,
        *,
        description: str | None = None,
        checked: bool = False,
        variable: Any | None = None,
        command: Callable[[], None] | None = None,
        **kwargs: Any,
    ) -> None:
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("corner_radius", 0)
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.variable = variable or ctk.BooleanVar(value=checked)
        self.checkbox = ctk.CTkCheckBox(
            self,
            text=text,
            variable=self.variable,
            command=command,
            checkbox_width=18,
            checkbox_height=18,
            corner_radius=4,
            border_color=COLOR_BORDER,
            fg_color=COLOR_PRIMARY,
            hover_color=COLOR_PRIMARY_HOVER,
            text_color=COLOR_TEXT,
            font=ctk.CTkFont(size=11, weight="bold"),
        )
        self.checkbox.grid(row=0, column=0, sticky="w")
        self.checkbox._text_label.configure(takefocus=True)
        self.checkbox._text_label.bind("<space>", self._toggle_from_keyboard, add="+")
        self.checkbox._text_label.bind("<FocusIn>", self._show_keyboard_focus, add="+")
        self.checkbox._text_label.bind("<FocusOut>", self._hide_keyboard_focus, add="+")

        if description:
            self.description_label = ctk.CTkLabel(
                self,
                text=description,
                font=ctk.CTkFont(size=10),
                text_color=COLOR_TEXT_MUTED,
                anchor="w",
                height=14,
            )
            self.description_label.grid(
                row=1, column=0, padx=(27, 0), pady=(3, 0), sticky="ew"
            )

    def get(self) -> bool:
        return bool(self.variable.get())

    def set(self, checked: bool) -> None:
        self.variable.set(checked)

    def _toggle_from_keyboard(self, _event: Any = None) -> str:
        self.checkbox.toggle()
        return "break"

    def keyboard_focus_target(self) -> Any:
        return self.checkbox._text_label

    def _show_keyboard_focus(self, _event: Any = None) -> None:
        self.checkbox._text_label.configure(
            highlightthickness=2,
            highlightcolor=self.checkbox._apply_appearance_mode(COLOR_PRIMARY),
        )

    def _hide_keyboard_focus(self, _event: Any = None) -> None:
        self.checkbox._text_label.configure(highlightthickness=0)


class PrimaryButton(ctk.CTkButton):
    """Primary blue action button."""

    def __init__(self, master: Any, text: str, **kwargs: Any) -> None:
        kwargs.setdefault("height", 36)
        kwargs.setdefault("corner_radius", 6)
        kwargs.setdefault("fg_color", COLOR_PRIMARY)
        kwargs.setdefault("hover_color", COLOR_PRIMARY_HOVER)
        kwargs.setdefault("text_color", COLOR_ON_PRIMARY)
        kwargs.setdefault("font", ctk.CTkFont(size=13, weight="bold"))
        super().__init__(master, text=text, **kwargs)
        enable_button_keyboard(self)


class OutlineButton(ctk.CTkButton):
    """Secondary outlined action button."""

    def __init__(self, master: Any, text: str, **kwargs: Any) -> None:
        kwargs.setdefault("height", 36)
        kwargs.setdefault("corner_radius", 6)
        kwargs.setdefault("fg_color", COLOR_SURFACE)
        kwargs.setdefault("hover_color", COLOR_HOVER)
        kwargs.setdefault("border_width", 2)
        kwargs.setdefault("border_color", COLOR_PRIMARY)
        kwargs.setdefault("text_color", COLOR_PRIMARY)
        kwargs.setdefault("font", ctk.CTkFont(size=13, weight="bold"))
        super().__init__(master, text=text, **kwargs)
        enable_button_keyboard(self)
