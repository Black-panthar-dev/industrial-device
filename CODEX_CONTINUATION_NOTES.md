# Power Monitor continuation notes

## Current scope

ML2 extends the client-accepted ML1 shell and Settings screen with General,
Measurements, and Communications configuration pages. ML2 is GUI-only: dummy
device values and placeholder actions, with no hardware, Modbus, serial/USB,
network, database, or installer integration. ML1 Settings retains local JSON
import/export, reset, folder selection, and its existing presentation.

The app opens Settings by default. Launch with `START_WINDOWS.bat` or
`.\.venv\Scripts\python.exe main.py` from the extracted project directory.

## QA and implementation references

- `ML2_WORK_COMPLETED.md`: chunk implementation record.
- `ML2_DELIVERY_QA.md`: 25-item delivery checklist and follow-up findings.
- `ML2_COMPLETE_QA.md`: comprehensive ML2 audit against ML1 QA categories.
- `WINDOWS_QA_NOTES.md`: historical ML1 QA results.
- `tools/qa_windows.py`: opt-in launch, keyboard and layout checks.
- `tools/qa_ml2_complete.py`: complete interaction and scaling audit.
- `qa_artifacts/`: local-only evidence and source delivery ZIP; excluded from Git.

Keep reports explicit about native Windows display checks versus programmatic
scaling/geometry checks. Native 1920x1080 at 125% and 150% still requires a
suitable desktop. Do not infer a full native-DPI pass from unit tests.

Run `python -m pytest -q` with the project interpreter for the lightweight
automated suite. Live tools need a Windows desktop-enabled process and write
their evidence to the output directory supplied on the command line.
