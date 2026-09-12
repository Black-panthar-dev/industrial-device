"""Opt-in live Windows QA; run from the delivery folder with its Python interpreter.

Usage: python tools/qa_windows.py gui OUTPUT_DIR
       python tools/qa_windows.py launch OUTPUT_DIR
The launch check closes only newly opened Power Monitor windows.
"""

import ctypes
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def launch(output):
    user32 = ctypes.windll.user32
    callback_type = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    user32.PostMessageW.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_size_t, ctypes.c_ssize_t]

    def windows():
        found = set()

        @callback_type
        def visit(handle, _):
            title = ctypes.create_unicode_buffer(256)
            user32.GetWindowTextW(ctypes.c_void_p(handle), title, 256)
            if title.value == "Power Monitor":
                found.add(handle)
            return True

        user32.EnumWindows(visit, 0)
        return found

    results = []
    for name, command in (
        ("launcher", ["cmd.exe", "/c", "START_WINDOWS.bat"]),
        ("manual", [str(ROOT / ".venv/Scripts/python.exe"), "main.py"]),
    ):
        previous = windows()
        logfile = output / f"{name}.log"
        with logfile.open("w", encoding="utf-8") as log:
            process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                       stdin=subprocess.DEVNULL)
            opened = False
            deadline = time.monotonic() + 180
            while time.monotonic() < deadline and process.poll() is None:
                new = windows() - previous
                if new:
                    opened = True
                    time.sleep(2)
                    for handle in new:
                        user32.PostMessageW(handle, 0x0010, 0, 0)
                    break
                time.sleep(0.25)
            try:
                code = process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                process.terminate()
                code = process.wait(timeout=10)
        content = logfile.read_text(encoding="utf-8")
        results.append(dict(check=name, opened=opened, exit_code=code,
                            passed=opened and code == 0 and "Traceback" not in content,
                            log=str(logfile)))
        print(results[-1], flush=True)
    return results


def gui(output, keyboard=True):
    import customtkinter as ctk
    import tkinter.font as tkfont
    from PIL import ImageGrab
    from main import IndustrialDeviceConfiguratorApp
    from utils.theme import COLOR_ACTIVE
    from widgets.form_controls import ThemedComboBox

    app = IndustrialDeviceConfiguratorApp()
    errors = []
    app.report_callback_exception = lambda *exc: errors.append("".join(traceback.format_exception(*exc)))

    def settle(seconds=0.3):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            app.update()
            time.sleep(0.01)

    def walk(widget):
        yield widget
        for child in widget.winfo_children():
            yield from walk(child)

    results = {"screen": [app.winfo_screenwidth(), app.winfo_screenheight()],
               "widget_scaling": app.sidebar._get_widget_scaling(), "pages": [], "layouts": []}
    try:
        app.minsize(760, 540)
        app.geometry("1366x700+0+0")
        settle()
        for name in (("General", "Measurements", "Communications", "Settings") if keyboard else ()):
            app.sidebar.buttons[name].invoke()
            settle()
            page = app.current_page
            assert app.pages[name] is page and page.winfo_ismapped()
            assert all(button.cget("fg_color") == (COLOR_ACTIVE if key == name else "transparent")
                       for key, button in app.sidebar.buttons.items())
            targets = getattr(page, "focus_targets", getattr(page, "keyboard_focus_targets", []))
            assert targets
            for event, step in (("<Tab>", 1), ("<Shift-Tab>", -1)):
                for index, target in enumerate(targets):
                    target.focus_force()
                    app.update()
                    target.event_generate(event)
                    app.update()
                    assert app.focus_get() == targets[(index + step) % len(targets)], (name, event, index)
            combos = [w for w in walk(page) if isinstance(w, ThemedComboBox)]
            activated = 0
            for widget in list(walk(page)):
                if isinstance(widget, ctk.CTkButton) and widget._canvas in targets:
                    original = widget.cget("command")
                    calls = []
                    widget.configure(command=lambda: calls.append(True))
                    try:
                        for event in ("<Return>", "<space>"):
                            widget._canvas.focus_force()
                            app.update()
                            widget._canvas.event_generate(event)
                            app.update()
                        assert len(calls) == 2, (name, widget.cget("text"), calls)
                        activated += 1
                    finally:
                        widget.configure(command=original)
                elif isinstance(widget, ctk.CTkCheckBox) and widget._text_label in targets:
                    before = widget.get()
                    widget._text_label.focus_force()
                    app.update()
                    widget._text_label.event_generate("<space>")
                    app.update()
                    assert widget.get() != before
                    widget._text_label.event_generate("<space>")
                    app.update()
                    assert widget.get() == before
                    activated += 1
                elif isinstance(widget, ctk.CTkRadioButton) and widget._text_label in targets:
                    for event in ("<Return>", "<space>"):
                        widget._text_label.focus_force()
                        app.update()
                        widget._text_label.event_generate(event)
                        app.update()
                        assert widget.cget("variable").get() == widget.cget("value")
                    activated += 1
            for combo in combos:
                for event in ("<Return>", "<space>"):
                    combo._entry.focus_force()
                    app.update()
                    combo._entry.event_generate(event)
                    settle(0.05)
                    assert combo._modern_popup is not None, (name, event)
                    combo._modern_popup.close()
                    app.update()
            results["pages"].append(dict(page=name, opened=True, active_state=True,
                                          tab_targets=len(targets), reverse_tab=True,
                                          activated_controls=activated,
                                          combo_enter_space=len(combos)))
            print(results["pages"][-1], flush=True)

        # These are logical client sizes, not changes to Windows display settings.
        for width, height, label in ((1366, 768, "1366_100"), (1536, 864, "1920_125_equivalent"),
                                     (1280, 720, "1920_150_equivalent"), (760, 540, "narrow"),
                                     (1366, 768, "wide_restored")):
            app.geometry(f"{width}x{height}+0+0")
            settle()
            for mode in ("Light", "Dark"):
                ctk.set_appearance_mode(mode)
                for name in ("General", "Measurements", "Communications", "Settings"):
                    app.show_page(name)
                    settle()
                    page = app.current_page
                    overflow = []
                    clipped_text = []
                    clipped_combos = []
                    for widget in walk(page):
                        if isinstance(widget, (ctk.CTkLabel, ctk.CTkComboBox)) and widget.winfo_ismapped():
                            if widget.winfo_x() < -1 or widget.winfo_x() + widget.winfo_width() > widget.master.winfo_width() + 2:
                                overflow.append(str(widget))
                            if isinstance(widget, ctk.CTkLabel):
                                label_widget = widget._label
                                if (label_widget.winfo_reqwidth() > label_widget.winfo_width() + 2
                                        or label_widget.winfo_reqheight() > label_widget.winfo_height() + 2):
                                    clipped_text.append(widget.cget("text"))
                            elif isinstance(widget, ThemedComboBox):
                                available = widget._entry.winfo_width()
                                needed = tkfont.Font(font=widget._entry.cget("font")).measure(widget.get())
                                if needed > available:
                                    clipped_combos.append(dict(value=widget.get(), available=available, needed=needed))
                    record = dict(viewport=label, theme=mode, page=name,
                                  requested_client=[width, height],
                                  actual_client=[app.winfo_width(), app.winfo_height()],
                                  clipped_label_text=clipped_text,
                                  clipped_combo_text=clipped_combos,
                                  horizontal_overflow=overflow)
                    if name != "Settings":
                        expected = page.get_layout_mode(page.winfo_width(), page._get_widget_scaling())
                        assert page._layout_mode == expected
                        assert int(page.right_panel.grid_info()["row"]) == (1 if expected[0] else 0)
                        record["right_panel_below"] = expected[0]
                    results["layouts"].append(record)
                    ImageGrab.grab(bbox=(0, 0, min(app.winfo_width(), app.winfo_screenwidth()),
                                         min(app.winfo_height(), app.winfo_screenheight()))).save(
                        output / f"{label}_{mode}_{name}.png")
            print(f"Checked {label}", flush=True)
        results["callback_errors"] = errors
        assert not errors, errors
    finally:
        app.destroy()
    return results


if __name__ == "__main__":
    action = sys.argv[1]
    destination = Path(sys.argv[2]).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    os.chdir(ROOT)
    result = launch(destination) if action == "launch" else gui(destination, keyboard=action != "layouts")
    (destination / f"{action}.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    if action != "launch":
        failures = [record for record in result["layouts"]
                    if record["clipped_label_text"] or record["clipped_combo_text"]
                    or record["horizontal_overflow"]]
        assert not failures, f"Clipping detected; see {destination / (action + '.json')}"
