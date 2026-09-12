"""Shared, low-overhead responsive layout scheduling."""

from typing import Any


class DebouncedResponsiveMixin:
    """Debounce breakpoint changes without rebuilding a view's widgets."""

    RESIZE_DEBOUNCE_MS = 180

    def _initialize_responsive_layout(self) -> None:
        self._resize_job: str | None = None
        self._layout_mode: tuple[bool, ...] | None = None
        self._pending_layout_mode: tuple[bool, ...] | None = None
        self.bind("<Configure>", self._schedule_responsive_layout, add="+")
        self.after_idle(self._apply_responsive_layout)

    def _schedule_responsive_layout(self, event: Any = None) -> None:
        width = getattr(event, "width", self.winfo_width())
        if width <= 1:
            return

        mode = self.get_layout_mode(width, self._get_widget_scaling())
        if mode == self._layout_mode:
            self._cancel_pending_layout()
            return
        if mode == self._pending_layout_mode:
            return

        self._cancel_pending_layout()
        self._pending_layout_mode = mode
        self._resize_job = self.after(
            self.RESIZE_DEBOUNCE_MS, self._apply_responsive_layout
        )

    def _cancel_pending_layout(self) -> None:
        if self._resize_job is not None:
            self.after_cancel(self._resize_job)
        self._resize_job = None
        self._pending_layout_mode = None

    def _apply_responsive_layout(self) -> None:
        self._resize_job = None
        self._pending_layout_mode = None
        width = self.winfo_width()
        if width <= 1:
            return

        mode = self.get_layout_mode(width, self._get_widget_scaling())
        if mode == self._layout_mode:
            return
        self._layout_mode = mode
        self._apply_layout_mode(mode)

    def _apply_layout_mode(self, mode: tuple[bool, ...]) -> None:
        raise NotImplementedError
