# Milestone 1 Windows QA Notes

QA completed on 21 July 2026. This was a verification pass only; no new
application features were added.

## Test environment

- Windows: Windows 10 Pro 21H1, build 19043.928
- Display: 1366 x 768 at native Windows 125% scaling
- Python: 3.13.14 (project `.venv`)
- Tk: 8.6.15
- CustomTkinter: 5.2.2
- Pillow: 10.4.0
- Dependency pins: `customtkinter==5.2.2` and `pillow==10.4.0`

## Resolutions and scaling covered

- 1366 x 768 at native Windows 125% scaling: live GUI launch, navigation,
  layout, theme, keyboard, ComboBox, and window-transition checks.
- 100% and 125%: manual visual checks performed during the Milestone 1 QA
  cycle.
- 1366 x 768 equivalents at 125% and 150%: automated logical-pixel geometry
  assertions.
- 1280 x 720 and 1920 x 1080: automated initial-size and minimum-size
  assertions.
- Responsive live widths covered wide, intermediate, and minimum-window modes.
  At constrained widths the existing right panel moved from the side to a row
  below the form; at the narrowest mode the inner Settings menu also moved
  above the form.

The test laptop does not expose a native 150% Windows scaling option. The 150%
result therefore covers DPI-aware layout calculations, not a native 150%
visual inspection.

## Passed checks

- [x] `python main.py` launches after activating the documented project
  virtual environment; the GUI process remained live during the startup probe.
- [x] `START_WINDOWS.bat` checks the environment and pinned requirements, then
  reaches `Starting Power Monitor...` with a live GUI process.
- [x] Settings is the first displayed page.
- [x] All 14 non-Settings sidebar destinations open successfully.
- [x] Non-Settings destinations use the translated reusable placeholder page.
- [x] Returning to Settings restores the existing Settings page correctly.
- [x] Responsive breakpoints use existing widgets and do not rebuild the page.
- [x] The right information/reset panel moves below the form when usable width
  is limited.
- [x] Forms change from three to two to one-column-safe arrangements at the
  tested DPI-aware breakpoints; controls remain scrollable and usable.
- [x] Native 125% visual/layout checks showed no clipped Settings controls.
- [x] Light and Dark modes update the current Settings page consistently.
- [x] ComboBoxes have readable text, 36-pixel logical height, borders, a
  distinct arrow-button area, hover colors, and theme-specific popup colors.
- [x] The Settings focus chain contains 33 controls in explicit visual order.
- [x] Live Tab and Shift+Tab tests moved forward and backward correctly.
- [x] Live Space testing toggled a focused checkbox.
- [x] Live Enter and Space testing activated a keyboard-enabled button.
- [x] Entries and ComboBoxes remain in the focus chain without Enter/Space
  crashes.
- [x] Maximize measured approximately 0.36-0.40 seconds, restore approximately
  0.37-0.39 seconds, and minimize approximately 0.01-0.02 seconds after layout
  warm-up. These transitions are acceptable on the test laptop.
- [x] Company Logo label and upload control are absent from Reports. The `PM`
  square in the sidebar is the application brand mark, not a company-logo
  upload placeholder.
- [x] English translations exist in `locales/en.json` and are loaded through
  `services/translation_service.py` using dotted translation keys.
- [x] `models/app_preferences.py` and `models/device_configuration.py` document
  the future separation of local preferences and per-device configuration.
- [x] Requirements are pinned to the requested versions.
- [x] README documents setup, manual launch, Windows BAT launch, translation
  structure, Milestone 1 scope, and the absence of hardware communication.
- [x] Automated suite: 12 tests passed.

## Known limitations

- The reusable ComboBox uses a CustomTkinter-styled custom popup to avoid the
  old native Windows Tk menu appearance. Popup placement and DPI rendering are
  still ultimately constrained by Tk/CustomTkinter and may vary slightly among
  Windows versions, multiple-monitor DPI configurations, and display drivers.
- A native Windows 150% visual pass remains recommended on hardware that offers
  that scaling level. Programmatic scaling and logical-pixel assertions cannot
  reproduce every per-monitor DPI behavior.
- Placeholder pages intentionally contain no device functionality in Milestone
  1. Hardware communication, Modbus, databases, and production device logic are
  outside this milestone.

