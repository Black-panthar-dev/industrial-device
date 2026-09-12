# Continuation Notes for the Power Monitor GUI project

## Current status
The app entrypoint and launch behavior have been adjusted so the project is more reliable on Windows.

### What has already been changed
- The app now opens on the Settings page by default.
- The window title is now "Power Monitor".
- The app prints a simple startup message: "Power Monitor started successfully".
- The Windows launcher script was updated to use a corrected Python version check.
- The main entrypoint now attempts to relaunch itself with the project virtual environment if CustomTkinter is not available in the currently active Python interpreter.
- The Settings view has also been updated with a more responsive layout that reorganizes at smaller widths instead of squeezing the content.

## Important files
- [main.py](main.py) — app startup, default page, title, and virtual-environment fallback.
- [views/settings_view.py](views/settings_view.py) — responsive Settings layout behavior.
- [START_WINDOWS.bat](START_WINDOWS.bat) — Windows launcher logic.
- [requirements.txt](requirements.txt) — Python dependencies.
- [utils/theme.py](utils/theme.py) — shared colors and theme constants.
- [widgets/](widgets/) — reusable UI control components.

## What to know before continuing
- This is still Milestone 1 scope: GUI framework + Settings screen only.
- No hardware communication, Modbus, database, or installer work was added.
- The current app is a desktop GUI built with CustomTkinter and Tkinter.

## Current priorities if continuing work
1. Verify the app opens correctly on Windows using the launcher and the manual command.
2. Review the settings screen visually at different window sizes and DPI scaling levels.
3. Continue improving the responsive layout if any clipping remains.
4. Continue polishing dark mode, ComboBox styling, and keyboard navigation later.

## How to run locally
From the project folder:

```powershell
.
.venv\Scripts\python.exe main.py
```

Or:

```powershell
START_WINDOWS.bat
```

## Known caveat
The environment may still behave differently depending on whether the app is launched from the system Python or from the project virtual environment. The current fallback logic in [main.py](main.py) helps with that.

## Suggested next step
Open the project in the editor and test the app manually. If anything still fails to open, check whether the correct virtual environment exists and whether CustomTkinter is installed in it.
