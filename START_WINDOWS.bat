@echo off
setlocal
cd /d "%~dp0"

echo Power Monitor - Milestone 2
echo ===========================

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if errorlevel 1 goto :python_version
    goto :environment_ready
)

where python >nul 2>nul
if errorlevel 1 goto :try_python_launcher

python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
if errorlevel 1 goto :try_python_launcher
set "PYTHON_CMD=python"
goto :python_ready

:try_python_launcher
where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
    goto :validate_python_launcher
)

if exist "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" (
    set "PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Launcher\py.exe" -3"
    goto :validate_python_launcher
)
goto :python_missing

:validate_python_launcher
%PYTHON_CMD% -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
if errorlevel 1 goto :python_version

:python_ready

echo Creating the local Python environment...
%PYTHON_CMD% -m venv .venv
if errorlevel 1 goto :setup_failed

:environment_ready
call ".venv\Scripts\activate.bat"
if errorlevel 1 goto :setup_failed

python -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 goto :setup_failed

python -c "import tkinter; tkinter.Tcl()" >nul 2>nul
if errorlevel 1 goto :tkinter_failed

echo Installing required components...
python -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 goto :setup_failed

echo Starting Power Monitor...
python main.py
if errorlevel 1 goto :run_failed
exit /b 0

:python_missing
echo.
echo Python was not found on PATH.
echo Install Python 3.10 or newer from https://www.python.org/downloads/windows/
echo Select "Add python.exe to PATH" during installation, then run this file again.
pause
exit /b 1

:python_version
echo.
echo Python 3.10 or newer is required.
echo Install a supported version, then run this file again.
pause
exit /b 1

:setup_failed
echo.
echo Setup did not complete. Confirm that Python 3.10 or newer is installed and
echo that this computer has internet access for dependency installation.
pause
exit /b 1

:tkinter_failed
echo.
echo Python is installed, but its Tkinter/Tcl components are damaged or missing.
echo Open Windows Settings ^> Apps ^> Installed apps, select Python, choose Modify,
echo and run Repair. Ensure "tcl/tk and IDLE" is selected, then run this file again.
pause
exit /b 1

:run_failed
echo.
echo Power Monitor closed because of an error. Review the message above or
echo send it to the software provider for support.
pause
exit /b 1
