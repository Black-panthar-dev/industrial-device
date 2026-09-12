# Power Monitor

Power Monitor is a Windows-oriented CustomTkinter desktop application for
configuring and monitoring an industrial power-monitoring device.

## Milestone 2 scope

Milestone 2 delivers the production GUI for:

- General device information, date and time, and operating settings.
- Voltage, current, processing, and calculated measurement settings.
- RS485/Modbus RTU, RS232, USB, expansion-module, and 4G settings.
- The existing Milestone 1 Settings screen and application shell.
- Responsive layouts, Light/Dark themes, centralized English translations,
  reusable controls, and keyboard navigation.

Milestone 2 is **GUI only**. Displayed device values and actions are dummy or
placeholder behavior. The codebase is structured for later device integration,
but real hardware access, Modbus, RS485/RS232/USB/4G communication, measurement
processing, database storage, and an installer are not implemented.

## Requirements

- Windows 10 or Windows 11.
- Python 3.10 or newer, including Tkinter/Tcl support.
- Internet access on first setup so Python packages can be installed.

Tested dependency versions:

- CustomTkinter 5.2.2
- Pillow 10.4.0
- pytest 9.1.1
- pypdfium2 5.13.0 (QA/document tooling only)

Runtime dependencies are pinned in `requirements.txt`. Test and document-tool
dependencies are pinned in `requirements-dev.txt`.

## Run on Windows

The simplest method is to extract the project and double-click
`START_WINDOWS.bat`.

The launcher:

1. Checks for Python 3.10 or newer.
2. Checks that Tkinter is available.
3. Creates the local `.venv` environment when necessary.
4. Installs the pinned runtime dependencies.
5. Starts Power Monitor with `python main.py`.

If setup or startup fails, the launcher keeps the window open and displays an
actionable error message.

## Run manually with Python

Open PowerShell in the project directory and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If the environment and dependencies already exist:

```powershell
.\.venv\Scripts\python.exe main.py
```

Open **Configuration** in the sidebar to access General, Measurements, and
Communications. Settings remains available from the sidebar.

## Run automated tests

Install the development dependencies and run pytest:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

The automated suite is lightweight and does not require a connected device,
Modbus adapter, serial/USB interface, network module, or database. It verifies
imports, ML2 view registration, translation keys, theme tokens, responsive
breakpoints, keyboard helpers, models, and reusable components. Live visual QA
procedures and results are documented in `ML2_QA_REPORT.md`.

## Project structure

```text
Power Monitor/
|-- main.py                       Application entry point and page routing
|-- START_WINDOWS.bat             Windows setup and launch helper
|-- requirements.txt              Pinned runtime dependencies
|-- requirements-dev.txt          Pinned test and QA dependencies
|-- locales/en.json               Centralized English interface strings
|-- services/                     Translation and local preference services
|-- utils/                        Theme and responsive-layout utilities
|-- views/
|   |-- general_view.py           General configuration screen
|   |-- measurements_view.py      Measurements configuration screen
|   |-- communications_view.py    Communications configuration screen
|   `-- settings_view.py          Application Settings screen
|-- widgets/                      Shared cards, controls, icons, and ML2 widgets
|-- test_*.py                     Automated delivery tests
|-- ML2_WORK_COMPLETED.md          Milestone implementation record
`-- ML2_QA_REPORT.md               Milestone QA record
```

## Translation and themes

Visible interface strings are loaded from `locales/en.json` through the shared
translation service. English is the current delivery locale. Light and Dark
colors are centralized in `utils/theme.py`; production ML2 views do not define
screen-specific hexadecimal colors.
