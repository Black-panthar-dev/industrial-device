# Industrial Device Configurator GUI

Industrial Device Configurator GUI is a Python 3 desktop application built with
CustomTkinter. Milestone 1 provides the application shell, sidebar navigation,
reusable UI components, placeholder pages, and the complete Settings screen.

> This milestone implements the GUI framework and Settings screen only. Hardware communication and real device integration are outside the current scope.

## Requirements

- Python 3.10 or newer
- A desktop environment capable of displaying Tkinter windows

## Setup

From the project directory, create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Windows launcher

Extract the project, then double-click `START_WINDOWS.bat`. The launcher checks
that Python 3.10 or newer is available, creates `.venv` when missing, activates
it, installs the pinned requirements, and starts Power Monitor.

The first launch requires internet access to install dependencies. Later
launches verify the same pinned versions before starting.

## Manual run

From the project directory, activate the virtual environment and run:

```powershell
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
```

If dependencies are already installed in the active Python environment, the
application can also be started directly:

```bash
python main.py
```

Use the left sidebar to switch between pages. Settings opens the implemented
preferences screen; the other navigation items currently open reusable
placeholder pages.

## Project structure

```text
industrial-device-configurator-gui/
├── main.py                     # Application entry point and page switching
├── requirements.txt            # Python dependencies
├── views/
│   ├── __init__.py
│   ├── placeholder_view.py     # Reusable page placeholder
│   └── settings_view.py        # Settings screen
├── widgets/
│   ├── __init__.py
│   ├── cards.py                # Reusable cards and information rows
│   ├── form_controls.py        # Reusable form inputs and buttons
│   ├── icons.py                # Pillow-rendered interface icons
│   └── sidebar.py              # Sidebar navigation
└── utils/
    ├── __init__.py
    └── theme.py                # Shared colors and theme constants
```

## Milestone 1 scope

This milestone is limited to the GUI framework and Settings screen. Settings
can be imported from and exported to local JSON files. Reset,
export-folder selection, theme selection, and section navigation are implemented
locally. Placeholder models document the future separation between local
application preferences and per-device JSON configuration files. The application
does not communicate with Power Monitor hardware. Hardware protocols, Modbus,
databases, installers, and production device logic are
intentionally not included.

## Translation structure

Visible interface text is centralized in `locales/en.json` and accessed through
`services/translation_service.py` with dotted keys such as
`t("settings.title")`. English is the only locale currently included; additional
JSON locale files can be added later without changing view layout code.
