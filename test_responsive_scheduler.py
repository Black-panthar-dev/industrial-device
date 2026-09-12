from types import SimpleNamespace

from utils.responsive import DebouncedResponsiveMixin


class FakeResponsiveView(DebouncedResponsiveMixin):
    RESIZE_DEBOUNCE_MS = 180

    def __init__(self) -> None:
        self.width = 1200
        self.scheduled: list[tuple[int, object]] = []
        self.cancelled: list[str] = []
        self.applied: list[tuple[bool, ...]] = []
        self._resize_job = None
        self._layout_mode = (False,)
        self._pending_layout_mode = None

    @staticmethod
    def get_layout_mode(width: float, _scaling: float = 1.0) -> tuple[bool, ...]:
        return (width < 1000,)

    @staticmethod
    def _get_widget_scaling() -> float:
        return 1.0

    def winfo_width(self) -> int:
        return self.width

    def after(self, delay: int, callback: object) -> str:
        self.scheduled.append((delay, callback))
        return f"job-{len(self.scheduled)}"

    def after_cancel(self, job: str) -> None:
        self.cancelled.append(job)

    def _apply_layout_mode(self, mode: tuple[bool, ...]) -> None:
        self.applied.append(mode)


def test_resize_within_current_breakpoint_does_not_schedule_work() -> None:
    view = FakeResponsiveView()
    view._schedule_responsive_layout(SimpleNamespace(width=1100))

    assert view.scheduled == []


def test_repeated_events_in_same_pending_breakpoint_reuse_one_timer() -> None:
    view = FakeResponsiveView()
    view._schedule_responsive_layout(SimpleNamespace(width=900))
    view._schedule_responsive_layout(SimpleNamespace(width=850))

    assert len(view.scheduled) == 1
    assert view.cancelled == []


def test_minimize_geometry_is_ignored() -> None:
    view = FakeResponsiveView()
    view._schedule_responsive_layout(SimpleNamespace(width=1))

    assert view.scheduled == []


def test_pending_reflow_is_cancelled_when_width_returns_to_current_mode() -> None:
    view = FakeResponsiveView()
    view._schedule_responsive_layout(SimpleNamespace(width=900))
    view._schedule_responsive_layout(SimpleNamespace(width=1100))

    assert view.cancelled == ["job-1"]
    assert view._resize_job is None
    assert view._pending_layout_mode is None
