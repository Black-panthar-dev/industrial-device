# ML2 delivery QA — 12 September 2026

Result: **23 passed (some with stated limits), 0 failed, 2 incomplete.** Fresh
installation, launching, navigation and keyboard checks passed. The label and
ComboBox clipping failures have been fixed and rechecked. Native 1920 x 1080
checks remain outstanding.

Initial application source tested: commit `211ecd3`. The follow-up verification
includes local clipping fixes in the General/Measurements layouts and shared
label-wrapping behavior, plus the live QA harness and documentation.

## Requested checklist

| # | Check | Result | Evidence / limits |
|---|---|---|---|
| 1 | Fresh folder test | PASS | Source-only ZIP extracted into a clean QA folder, initially without `.venv`; complete-audit candidate is `qa_artifacts/complete_fresh`. |
| 2 | Run START_WINDOWS.bat | PASS | Created a fresh environment, installed dependencies, opened Power Monitor; closed normally, exit 0. |
| 3 | Run python main.py manually | PASS | Fresh `.venv/Scripts/python.exe main.py` opened Power Monitor; closed normally, exit 0. |
| 4 | General opens | PASS | Live sidebar invocation and mapped page assertion. |
| 5 | Measurements opens | PASS | Live sidebar invocation and mapped page assertion. |
| 6 | Communications opens | PASS | Live sidebar invocation and mapped page assertion. |
| 7 | Settings still opens | PASS | Live sidebar invocation and mapped page assertion. |
| 8 | Sidebar active states | PASS | Selected item uses active color and all other items clear it on each navigation. |
| 9 | Light mode | PASS | All four pages rendered; cross-page selectors and Settings theme values synchronized. |
| 10 | Dark mode | PASS | All four pages rendered, including pages first created in Dark mode; foreground screenshots saved. |
| 11 | 1366x768 at 100% | PASS | Actual display 1366x768; widget scaling 1.0. Windows limited client height to 749 pixels. No clipping detected after fixes. |
| 12 | 1920x1080 at 125% | PARTIAL | Full virtual 1920x1080 geometry passed at programmatic 125% scaling after allowing off-screen window sizes. Native Windows 1920x1080/125% remains unverified. |
| 13 | 1920x1080 at 150% | PARTIAL | Full virtual 1920x1080 geometry passed at programmatic 150% scaling. Native Windows 1920x1080/150% remains unverified. |
| 14 | No clipped labels | PASS | Live allocated-width/text-size checks pass in both themes at all tested actual window sizes. Narrow subtitles and banner prose now wrap; collapsed form columns fixed. |
| 15 | No clipped ComboBoxes | PASS | Selected text fits its entry area in all tested layouts, including narrow General timezone and Measurements shunt voltage/filter controls. |
| 16 | Right panel below when narrow | PASS | All three ML2 pages re-grid their right panel below at 1280x720 and 760x540. |
| 17 | Tab order | PASS | Generated Tab events traverse and wrap all 18/22/24/33 targets; focused controls now scroll into view. |
| 18 | Shift+Tab | PASS | Reverse traversal and wrap checked on every explicit target. |
| 19 | Enter/Space | PASS | All 34 ComboBoxes open with both keys. Focus-chain buttons, checkboxes and radios activate as appropriate. Button commands temporarily replaced with counters to avoid persistence/reset actions. |
| 20 | No terminal errors | PASS for application | Startup logs clean; completed live verification has no Tk callback errors. Initial diagnostics and corrected harness failures are retained separately. |
| 21 | README updated | PASS | ML2 scope, startup, dependencies, tests, and live QA instructions documented. |
| 22 | requirements.txt pinned | PASS | `customtkinter==5.2.2`, `pillow==10.4.0`; fresh environment `pip check` passes. Transitive dependencies are not lockfile-pinned. |
| 23 | Tests included | PASS | All 39 automated tests pass in the project environment. Delivery ZIP includes test files and opt-in live QA harness. |
| 24 | No venv in ZIP | PASS | ZIP entry audit excludes `.venv` and `venv` directories. The launcher creates the environment only after extraction. |
| 25 | No __pycache__ in ZIP | PASS | ZIP entry audit excludes `__pycache__` and Python bytecode. |

## Resolved findings and evidence

The complete follow-up audit in `ML2_COMPLETE_QA.md` additionally covers theme
synchronization, visible keyboard focus, Settings file and section actions,
popup lifecycle, scaling-refresh placement, and comparison with `ML2.pdf`.

- General and Measurements retained a two-column Tk uniform group after moving
  controls to one column. Clearing the group in one-column mode gives controls
  the full available width; two-column mode restores equal column sizing.
- Page subtitles, section descriptions, information banners and field helper
  text now wrap to the allocated logical width. The handler observes the outer
  label frame rather than CustomTkinter's internal text widget, avoiding a
  text-size feedback loop.
- Initial failures included narrow General timezone text, Measurements shunt
  voltage/filter text, collapsed calibration/shunt controls, subtitles, and
  Measurements/Communications information banners. All passed the follow-up
  text-size checks, including content below the initial scroll position.
- Checking only widget rectangles is insufficient: a label can fit inside its
  parent while its actual text is clipped. The harness now records both.

Local evidence is under `qa_artifacts/results`: `launch.json`, `launcher.log`,
`manual.log`, `gui.json`, `layouts.json`, `combo_text.json`, and screenshots for
each page/theme/size. Screenshots are limited to the available desktop; they
cannot certify off-screen pixels or native 1920x1080 scaling.

Post-fix evidence is under `qa_artifacts/fixed` and `qa_artifacts/fixed_fresh`.
The live harness now returns a failure if label text, ComboBox text or widget
boundaries exceed their allocation, and also checks the return from a narrow
window to a wide one. Original failure evidence remains available separately.

The fresh launcher selected Python 3.12. The existing automated-test environment
uses Python 3.13. No clean Windows installation or disconnected-network setup
was simulated; this was a clean project folder on the current Windows machine.

The new delivery archive is `qa_artifacts/Power_Monitor_Milestone_2_Client.zip`.
It contains source, documentation and tests; excludes local evidence, Git data,
virtual environments, caches and the historical ML1 ZIP. It is a QA candidate,
not a declaration that all checklist items passed.
