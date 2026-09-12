"""Opt-in desktop ML2 audit, including ML1 Settings regression checks.

Run: python tools/qa_ml2_complete.py OUTPUT_DIRECTORY
Programmatic scaling is explicitly not a native Windows DPI certification.
"""

import contextlib
import io
import json
from pathlib import Path
import sys
import time
import traceback
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import customtkinter as ctk
import tkinter.font as tkfont
from PIL import ImageGrab
from main import IndustrialDeviceConfiguratorApp
from services.translation_service import t
from views.settings_view import DEFAULT_SETTINGS
from widgets.form_controls import LabeledEntry, ThemedComboBox
from widgets.ml2_components import ReadonlyField, SectionHeader
from utils.theme import COLOR_ACTIVE, COLOR_SECTION_ACTIVE


def walk(widget):
    yield widget
    for child in widget.winfo_children():
        yield from walk(child)


def run(output, phase="all"):
    app = IndustrialDeviceConfiguratorApp()
    errors = []
    app.report_callback_exception = lambda *exc: errors.append("".join(traceback.format_exception(*exc)))
    report = {"screen": [app.winfo_screenwidth(), app.winfo_screenheight()],
              "checks": [], "layouts": [], "callback_errors": errors}

    def settle(duration=0.3):
        end = time.monotonic() + duration
        while time.monotonic() < end:
            app.update()
            time.sleep(0.01)

    def check(name, action):
        try:
            detail = action()
            result = dict(name=name, passed=True, detail=detail)
        except Exception:
            result = dict(name=name, passed=False, error=traceback.format_exc())
        report["checks"].append(result)
        (output / "complete.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(name, "PASS" if result["passed"] else "FAIL", flush=True)

    def select(name):
        app.sidebar.buttons[name].invoke()
        settle()
        return app.current_page

    def visible(target, workspace):
        ancestor = target
        while ancestor is not None and ancestor is not workspace:
            ancestor = getattr(ancestor, "master", None)
        if ancestor is None:
            return True
        canvas = workspace._parent_canvas
        return (target.winfo_rooty() >= canvas.winfo_rooty() - 2 and
                target.winfo_rooty() + target.winfo_height() <= canvas.winfo_rooty() + canvas.winfo_height() + 2)

    def themes():
        assert app.current_page is app.pages["Settings"]
        general = select("General")
        general.theme_menu._dropdown_callback("Dark")
        for name in ("Measurements", "Communications", "Settings"):
            select(name)  # Includes pages created for the first time in Dark mode.
        for source in ("General", "Measurements", "Communications", "Settings"):
            page = select(source)
            menu = page.controls["header_theme"] if source == "Settings" else page.theme_menu
            for mode in ("Light", "Dark"):
                menu._dropdown_callback(mode)
                settle()
                assert ctk.get_appearance_mode() == mode
                for name, cached in app.pages.items():
                    other = cached.controls["header_theme"] if name == "Settings" else cached.theme_menu
                    assert other.get() == mode, (source, mode, name, other.get())
                assert app.pages["Settings"]._collect_settings()["theme"] == mode
        return "All 4 sources, both themes; cached and new pages, Settings export value."

    def navigation():
        for name, button in app.sidebar.buttons.items():
            page = select(name)
            assert page.winfo_ismapped()
            assert all(b.cget("fg_color") == (COLOR_ACTIVE if key == name else "transparent")
                       for key, b in app.sidebar.buttons.items())
            app.show_page("Settings")
            app.show_page(name)
            assert app.current_page is page
        return len(app.sidebar.buttons)

    def focus():
        count = 0
        for name in ("General", "Measurements", "Communications", "Settings"):
            page = select(name)
            targets = getattr(page, "focus_targets", getattr(page, "keyboard_focus_targets", []))
            for event, step in (("<Tab>", 1), ("<Shift-Tab>", -1)):
                targets[0].focus_force()
                app.update()
                index = 0
                for _ in targets:
                    assert app.focus_get() == targets[index]
                    assert visible(targets[index], page.workspace), (name, event, index)
                    targets[index].event_generate(event)
                    app.update()
                    index = (index + step) % len(targets)
                    count += 1
        return count

    def popups():
        count = 0
        for name in ("General", "Measurements", "Communications", "Settings"):
            page = select(name)
            for combo in [w for w in walk(page) if isinstance(w, ThemedComboBox)]:
                original = combo.get()
                combo._entry.focus_force()
                app.update()
                combo._entry.event_generate("<Return>")
                settle(0.1)
                popup = combo._modern_popup
                assert popup is not None
                assert popup.winfo_rooty() >= 0
                assert popup.winfo_rooty() + popup.winfo_height() <= app.winfo_screenheight() + 2
                first = popup.active_index
                popup.buttons[first]._canvas.event_generate("<Down>")
                app.update()
                expected_index = (first + 1) % len(popup.buttons)
                assert popup.active_index == expected_index
                popup.buttons[expected_index]._canvas.event_generate("<Return>")
                app.update()
                assert combo._modern_popup is None
                assert combo.get() == combo.cget("values")[expected_index]
                combo._dropdown_callback(original)
                combo._entry.focus_force()
                app.update()
                combo._entry.event_generate("<space>")
                settle(0.1)
                popup = combo._modern_popup
                popup.buttons[popup.active_index]._canvas.event_generate("<Escape>")
                app.update()
                assert combo._modern_popup is None and combo.get() == original
                count += 1
        return count

    def settings_files():
        settings = select("Settings")
        for index, (name, section) in enumerate(settings.section_widgets.items()):
            settings.section_buttons[index].invoke()
            settle()
            canvas = settings.workspace._parent_canvas
            top = section.winfo_rooty() - canvas.winfo_rooty()
            assert -2 <= top < canvas.winfo_height(), (name, top)
            assert all(button.cget("fg_color") == (COLOR_SECTION_ACTIVE if item == index else "transparent")
                       for item, button in enumerate(settings.section_buttons))
        saved = settings._collect_settings()
        file = output / "settings_roundtrip.json"
        with patch.object(settings, "_show_notice") as notice:
            sample = dict(saved, company_name="QA company", technician_name="QA technician",
                          export_folder=str(output), theme="Dark", auto_connect=False)
            settings._apply_settings(sample)
            assert settings._collect_settings() == sample
            with patch("views.settings_view.filedialog.asksaveasfilename", return_value=str(file)):
                settings._export_settings()
            assert json.loads(file.read_text(encoding="utf-8")) == sample
            settings._reset_settings()
            assert settings._collect_settings() == DEFAULT_SETTINGS
            with patch("views.settings_view.filedialog.askopenfilename", return_value=str(file)):
                settings._import_settings()
            assert settings._collect_settings() == sample
            with patch("views.settings_view.filedialog.askdirectory", return_value=str(output / "reports")):
                settings._select_export_folder()
            assert settings.controls["export_folder"].get() == str(output / "reports")
            file.write_text("[]", encoding="utf-8")
            before = settings._collect_settings()
            with patch("views.settings_view.filedialog.askopenfilename", return_value=str(file)):
                settings._import_settings()
            assert settings._collect_settings() == before
            assert notice.call_args.kwargs.get("error") is True
            settings._apply_settings(saved)
        return "Export/import/reset/browse and invalid-file handling; dialogs substituted with QA paths."

    def content_and_actions():
        counts = {}
        for name, expected_sections in (("General", 5), ("Measurements", 5), ("Communications", 4)):
            page = select(name)
            widgets = list(walk(page))
            assert sum(isinstance(w, SectionHeader) for w in widgets) == expected_sections
            for w in widgets:
                if isinstance(w, ReadonlyField):
                    assert w.field.cget("state") == "disabled"
            field = next(w for w in widgets if isinstance(w, LabeledEntry))
            original = field.get()
            field.set("QA retained value")
            select("Settings")
            select(name)
            assert field.get() == "QA retained value"
            field.set(original)
            calls = 0
            for w in widgets:
                if (isinstance(w, ctk.CTkButton) and getattr(w, "_keyboard_activation_enabled", False)
                        and not isinstance(w.master, ctk.CTkSegmentedButton)):
                    with contextlib.redirect_stdout(io.StringIO()) as log:
                        w.invoke()
                    assert log.getvalue().strip(), (name, w.cget("text"))
                    calls += 1
            if name == "Communications":
                masked = [w for w in widgets if isinstance(w, LabeledEntry) and w.entry.cget("show") == "*"]
                assert len(masked) == 2
                tabs = page.module_tabs
                for value, button in tabs._buttons_dict.items():
                    with contextlib.redirect_stdout(io.StringIO()):
                        button.invoke()
                    assert tabs.get() == value
            counts[name] = dict(sections=expected_sections, placeholder_actions=calls)
        return counts

    def transitions():
        times = []
        for name in ("General", "Measurements", "Communications", "Settings"):
            page = select(name)
            before = {str(w) for w in walk(page)}
            for state in ("zoomed", "normal", "iconic", "normal"):
                started = time.monotonic()
                app.state(state)
                settle(0.6)
                times.append(dict(page=name, state=state, seconds=round(time.monotonic()-started, 3)))
            assert {str(w) for w in walk(page)} == before
        return times

    def visual():
        ctk.set_widget_scaling(1)
        ctk.set_window_scaling(1)
        app.state("normal")
        app.geometry("760x540+0+0")
        app.attributes("-topmost", True)
        settle(0.6)
        try:
            for mode in ("Light", "Dark"):
                ctk.set_appearance_mode(mode)
                for name in ("General", "Measurements", "Communications", "Settings"):
                    page = select(name)
                    canvas = page.workspace._parent_canvas
                    canvas.yview_moveto(1)
                    settle()
                    assert canvas.yview()[1] >= 0.999, (name, canvas.yview())
                    for part, fraction in (("top",0), ("middle",0.5), ("bottom",1)):
                        canvas.yview_moveto(fraction)
                        app.lift()
                        settle(0.15)
                        ImageGrab.grab(bbox=(0,0,780,580)).save(output/f"{name}_{mode}_{part}.png")
        finally:
            app.attributes("-topmost", False)
        return "24 foreground screenshots; bottom scroll position reached on all 4 pages."

    def layouts():
        # Permit virtual off-screen sizes for geometry checks. These remain
        # programmatic scaling tests, not native Windows DPI tests.
        app.maxsize(2600, 1800)
        cases = [(width, 700, 1.0) for width in (760, 900, 949, 950, 1050, 1129, 1130, 1280, 1349, 1350, 1366)]
        cases += [(1920, 1080, 1.25), (1920, 1080, 1.5)]
        for physical_width, physical_height, scale in cases:
            ctk.set_widget_scaling(scale)
            ctk.set_window_scaling(scale)
            app.geometry(f"{round(physical_width/scale)}x{round(physical_height/scale)}+0+0")
            settle(0.6)
            for mode in ("Light", "Dark"):
                ctk.set_appearance_mode(mode)
                for name in ("General", "Measurements", "Communications", "Settings"):
                    page = select(name)
                    failures = []
                    for w in walk(page):
                        if not w.winfo_ismapped():
                            continue
                        native = None
                        if isinstance(w, ctk.CTkLabel):
                            native = w._label
                        elif isinstance(w, (ctk.CTkButton, ctk.CTkCheckBox, ctk.CTkRadioButton)):
                            native = w._text_label
                        if native is not None:
                            if native.winfo_reqwidth() > native.winfo_width()+2 or native.winfo_reqheight() > native.winfo_height()+2:
                                failures.append(dict(type=type(w).__name__, text=w.cget("text"),
                                                     requested=[native.winfo_reqwidth(),native.winfo_reqheight()],
                                                     actual=[native.winfo_width(),native.winfo_height()]))
                        if isinstance(w, ThemedComboBox):
                            needed = tkfont.Font(font=w._entry.cget("font")).measure(w.get())
                            if needed > w._entry.winfo_width():
                                failures.append(dict(type="ComboBox", text=w.get()))
                    record = dict(size=[physical_width,physical_height], scale=scale, mode=mode, page=name,
                                  actual=[app.winfo_width(),app.winfo_height()], failures=failures)
                    report["layouts"].append(record)
            print("Geometry", physical_width, scale, flush=True)
            (output / "complete.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        visual()
        failures = [r for r in report["layouts"] if r["failures"]]
        assert not failures, f"{len(failures)} layout cases have clipping; see report."
        return len(report["layouts"])

    try:
        app.minsize(760,540)
        app.geometry("760x540+0+0")
        settle()
        if phase not in {"layouts", "content", "visual"}:
            check("theme synchronization and new-page theme", themes)
            check("all sidebar destinations and cached-page reuse", navigation)
            check("visible forward/reverse keyboard traversal", focus)
            check("popup selection, Escape and screen bounds", popups)
            check("ML1 Settings file actions", settings_files)
            check("ML2 content, retained edits and placeholder actions", content_and_actions)
            check("maximize/minimize/restore without widget recreation", transitions)
        if phase == "content":
            check("ML2 content, retained edits and placeholder actions", content_and_actions)
        if phase == "visual":
            check("foreground visual evidence and scroll reachability", visual)
        if phase not in {"interactions", "content", "visual"}:
            check("breakpoint/scaling geometry and scroll reachability", layouts)
    finally:
        app.destroy()
        (output / "complete.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    assert not errors and all(r["passed"] for r in report["checks"]), "QA failures: see complete.json"


if __name__ == "__main__":
    destination = Path(sys.argv[1]).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    run(destination, sys.argv[2] if len(sys.argv) > 2 else "all")
