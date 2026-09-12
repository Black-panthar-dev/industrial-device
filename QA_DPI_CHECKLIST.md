# Native Windows DPI QA

Run these checks at **100%**, **125%**, and **150%** Windows display scaling.
Sign out and back in if Windows requests it after changing the scale.

For each scale:

1. Start the application with `python main.py`.
2. Check the maximized window and the minimum supported `1200x720` size.
3. Resize slowly from wide to narrow and back to wide.
4. Confirm the right summary panel moves below the form before controls clip.
5. Confirm the inner Settings menu moves above the form at narrow widths.
6. Confirm every label, button, entry, ComboBox, and checkbox remains usable.
7. Scroll to Reports and confirm all fields and buttons can be reached.
8. Record the scale, resolution, and any failure with a screenshot.

Automated breakpoint checks can be run with:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

These tests verify DPI-normalized responsive decisions, but they do not replace
native visual inspection because Windows font rasterization and monitor DPI
behavior are controlled outside the application.
