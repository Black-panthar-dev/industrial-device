"""Live navigation regression and timing check: python tools/qa_navigation.py."""

from pathlib import Path
from contextlib import ExitStack
import statistics
import sys
import time
import tkinter as tk
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import customtkinter as ctk

from main import IndustrialDeviceConfiguratorApp
from services.translation_service import t
from widgets.form_controls import LabeledEntry


def settle(app, seconds=0.3):
    deadline = time.perf_counter() + seconds
    while time.perf_counter() < deadline:
        app.update()
        time.sleep(0.01)


def main():
    ctk.set_appearance_mode("light")
    app = IndustrialDeviceConfiguratorApp()
    errors = []
    app.report_callback_exception = lambda *args: errors.append(args)
    try:
        settle(app)
        # A page first opened in dark mode must initialize its theme controls.
        ctk.set_appearance_mode("dark")
        app.show_page("General")
        assert app.pages["General"].theme_menu.get() == t("general.theme.dark")
        ctk.set_appearance_mode("light")
        names = list(app.sidebar.buttons)
        for name in names:
            app.show_page(name)
            settle(app)
        cached = dict(app.pages)
        field = next(control for control in cached["General"].focus_controls
                     if isinstance(control, LabeledEntry))
        field.entry.delete(0, "end")
        field.entry.insert(0, "Navigation QA retained value")
        mapping_events = []

        def watch_mapping(widget):
            for event in ("<Map>", "<Unmap>"):
                tk.Misc.bind(widget, event,
                             lambda e: mapping_events.append(str(e.widget)), add="+")
            for child in widget.winfo_children():
                watch_mapping(child)

        for page in cached.values():
            watch_mapping(page)
        samples = []
        with ExitStack() as stack:
            sync = stack.enter_context(patch.object(
                app, "_sync_theme_controls", wraps=app._sync_theme_controls))
            for page in cached.values():
                for method in ("grid", "grid_remove", "grid_forget"):
                    stack.enter_context(patch.object(page, method, side_effect=AssertionError(
                        "Cached navigation must not change page geometry management")))
            for _ in range(5):
                for name in names:
                    started = time.perf_counter()
                    app.show_page(name)
                    app.update()  # Include queued geometry and paint work.
                    samples.append((time.perf_counter() - started) * 1000)
                    assert app.current_page is cached[name]
                    assert all(page.winfo_ismapped() for page in cached.values())
                    assert app.content_area.winfo_children()[-1] is cached[name]
            sync.assert_not_called()
            with patch.object(app.sidebar, "set_active") as active:
                app.show_page(names[-1])
                active.assert_not_called()
        assert app.pages == cached
        assert not mapping_events, mapping_events
        assert field.entry.get() == "Navigation QA retained value"

        for mode in ("dark", "light"):
            ctk.set_appearance_mode(mode)
            settle(app)
            for name in ("General", "Measurements", "Communications"):
                assert cached[name].theme_menu.get() == t(f"{name.lower()}.theme.{mode}")
            for control in ("header_theme", "theme"):
                assert cached["Settings"].controls[control].get() == mode.title()

        assert not errors, errors
        ordered = sorted(samples)
        print(f"PASS: {len(cached)} cached screens, {len(samples)} switches; "
              f"median={statistics.median(samples):.1f} ms, "
              f"p95={ordered[int((len(ordered) - 1) * .95)]:.1f} ms, "
              f"max={max(samples):.1f} ms", flush=True)
        print("PASS: no page re-gridding, no widget map/unmap events, no navigation "
              "theme synchronization; input retained; active-page selection is a no-op; "
              "light/dark controls correct; no Tk callback errors", flush=True)
    finally:
        app.destroy()


if __name__ == "__main__":
    main()
