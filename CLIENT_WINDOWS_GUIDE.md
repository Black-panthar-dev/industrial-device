# Industrial Device Configurator — ML1 Windows Guide

## What is included

Milestone 1 (ML1) provides the desktop application shell, navigation, reusable
interface components, and the complete Settings screen. Device communication
and live hardware integration are not included in this milestone.

## Windows requirements

- Windows 10 or Windows 11
- Python 3.10 or newer (64-bit recommended)
- Internet access during the first launch to install Python dependencies
- Permission to create files inside the extracted application folder

## First-time setup and launch

1. Copy the supplied ZIP to the Windows computer.
2. Right-click the ZIP, select **Extract All**, and open the extracted folder.
3. Confirm Python 3.10 or newer is installed. If needed, download it from
   <https://www.python.org/downloads/windows/> and enable **Add python.exe to
   PATH** during installation.
4. Double-click `START_WINDOWS.bat`.
5. On the first launch, wait while the local `.venv` environment is created and
   the required components are installed. Later launches reuse this environment.

Do not run the application from inside the ZIP. Extract it first.

## Manual launch option

Open Command Prompt in the extracted folder and run:

```bat
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

## Using ML1

- Use the left sidebar to move between application areas.
- Open **Settings** using the gear button at the bottom-left.
- Settings may be imported from or exported to a local JSON file.
- Logo selection, export-folder selection, theme selection, reset, and Settings
  section navigation operate locally.
- Pages outside Settings are ML1 placeholders for future milestones.

## Display recommendation

The interface supports common Windows display scaling. If Windows changes the
scale while the application is open, close and reopen the application. A scale
of 100%, 125%, or 150% is recommended.

## Troubleshooting

### Windows says Python was not found

Install Python 3.10 or newer and select **Add python.exe to PATH**, then restart
the launcher.

### Dependency installation fails

Confirm the computer has internet access and that firewall or proxy rules allow
Python package downloads. Then run `START_WINDOWS.bat` again.

### Windows protects your PC

This source delivery is launched through a batch file rather than a signed
installer. Review the supplied files with your IT team. If Windows permits,
choose **More info** and proceed only after confirming the package came from the
expected provider.

### Support information to provide

When reporting a problem, include the Windows version, display scale, Python
version, a screenshot, and the complete error text shown in the launcher window.
