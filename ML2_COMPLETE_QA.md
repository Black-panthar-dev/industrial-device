# Complete ML2 QA — 12 September 2026

This audit applies the ML1 QA categories to the entire ML2 application, including
the existing Settings screen. It supplements `ML2_DELIVERY_QA.md` and compares
the ML2 configuration content with the three-page supplied `ML2.pdf`.

**Result: all functional audit categories passed after fixes and targeted
verification.** There were no detected clipping failures in 104 layout cases,
no application callback errors in the completed verification, and 39 lightweight
tests passed. Native Windows DPI certification remains outstanding as below.

## Environment and limits

- Windows 10, build 19045; physical desktop 1366 x 768 at 100%.
- Python 3.13.14, CustomTkinter 5.2.2, Pillow 10.4.0.
- Programmatic widget/window scaling at 125% and 150%, using virtual
  1920 x 1080 window geometry, is tested separately from native Windows DPI.
- Native Windows 1920 x 1080 at 125% and 150% remains unverified on this desktop.
- The PDF comparison covers sections, fields, sample values, actions and visual
  conventions. The application retains its ML1 typography, spacing and scrolling;
  this is not a claim of pixel-for-pixel PDF reproduction.

## Coverage

| Area | Verification |
|---|---|
| ML1 regression | Settings starts first; local JSON export/import/reset, folder selection, invalid-file handling and section navigation. |
| Navigation | All 15 sidebar destinations open, active states update, and cached pages are reused. |
| Theme | Light/Dark selection from each of the four configuration pages; cached/new pages, selectors and exported Settings theme agree. |
| Keyboard | 194 forward/reverse transitions across 97 targets, including wrapping and scroll visibility. |
| Dropdowns | 34 real popup checks: opening, arrow selection, Enter, Escape, and desktop bounds. |
| ML2 content | General 5 sections, Measurements 5, Communications 4; read-only fields, masked credentials, segmented controls and retained edits. |
| Actions | Actual GUI-only placeholder commands invoked; Settings file operations confined to QA files, with file dialogs substituted. |
| Layout | 11 window widths around breakpoints, plus 1920 x 1080 programmatic 125% and 150%; both themes, all four pages. |
| Scrolling | Focused controls remain visible; bottom of each workspace is reachable; top/middle/bottom screenshots saved. |
| Window transitions | Maximize, restore, minimize and restore on all four pages without recreating their widgets. |
| Lightweight tests | 39 tests passed after production changes. |

The recorded window-transition times include a deliberate 600 ms settling
period, and all pages were already loaded. They are not directly comparable
with the historical ML1 timing figures or an isolated rendering benchmark.

## Issues corrected during this audit

1. Theme selectors on cached pages could disagree with the actual application
   appearance. The application now synchronizes them, including Settings values
   and newly opened pages.
2. Tab could focus controls outside the visible scroll area. The shared focus
   chain now reveals focused controls while preserving its existing order.
3. The shared entry setter called an unsupported CustomTkinter method, breaking
   Settings import/reset/folder updates. It now uses the supported delete/insert
   operations. Settings file round-trips were exercised after the fix.
4. Applying a theme while its dropdown was still open could leave callbacks
   targeting a destroyed popup. Selection now closes the popup before applying
   the command.
5. Responsive placements used Tk grid updates that CustomTkinter did not retain
   across scaling refreshes. The four pages and shared header controls now use
   CustomTkinter's scaling-aware grid method, preserving current placements.
6. Settings section scrolling used the outer viewport's requested height instead
   of the content height. Section selection now reaches the correct section and
   updates its active styling.
7. The PDF comparison identified two sample-value discrepancies: General
   connection time and the RS232 transmit counter. These now read `00:01:24`
   and `2987`; the calculated-measurements banner uses the green success style.
8. The client guide and continuation notes still described ML1-only behavior.
   They now describe ML2 and its GUI-only boundaries.

The client-accepted ML1 screen structure and visual design were retained.
No device protocols, hardware access, database, or installer functionality was
introduced.

## Reproduce and inspect

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools\qa_ml2_complete.py qa_artifacts\complete
```

The live audit needs desktop access. It writes `complete.json`, screenshots and
temporary Settings files only under its output directory. Optional final
arguments `interactions`, `layouts`, `content`, and `visual` run targeted follow-ups.

Initial findings are preserved in `qa_artifacts/complete_initial`. Follow-up
results are recorded in `qa_artifacts/complete_final`. Its action-check failure
was a test expectation: a selected segmented tab intentionally does not re-fire
its command. The corrected content check passed in `qa_artifacts/complete_content`;
the other seven categories passed in the full run. No production change was
needed for that targeted rerun.

Use the 24 foreground captures in `qa_artifacts/complete_visual` for visual
evidence. Earlier non-foreground captures could show the editor and are not
valid screenshot evidence. The foreground pass also verifies bottom scroll
reachability on all four pages. Screenshots were inspected against the supplied
PDF's structure and visual conventions.

The consolidated evidence index is `qa_artifacts/complete_verified.json`.
Fresh-package startup evidence is in `qa_artifacts/complete_launch`.
Both `START_WINDOWS.bat` (including fresh environment creation and dependency
installation) and manual `main.py` startup opened the application and exited
normally with code 0. The new source ZIP excludes virtual environments,
bytecode, caches, local evidence, Git data, and the historical ML1 ZIP.
