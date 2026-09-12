# Industrial Device Configurator — ML1 Work Completed

## Delivery summary

ML1 establishes the desktop GUI foundation for the Industrial Device
Configurator. It provides a consistent application shell and a functional local
Settings experience ready for later device-integration milestones.

## Completed work

- Created the CustomTkinter application window and responsive main workspace.
- Added sidebar navigation, grouped application areas, icons, active-page state,
  status display, and Settings access.
- Added reusable section cards, information rows, labeled entries, dropdowns,
  checkboxes, primary buttons, and outline buttons.
- Implemented the Settings screen sections: General, Connection, Application,
  Security, and Reports.
- Added local settings import and export using JSON files.
- Added reset-to-default behavior, theme selection, company-logo selection,
  export-folder selection, and section navigation.
- Added placeholder screens for functionality planned in later milestones.
- Centralized application colors and theme constants.

## Windows rendering refinement

The reusable action-button styling was refined to reduce soft or uneven corner
rasterization on Windows:

- Button height standardized to an integer `36` pixels.
- Small-button corner radius reduced to `6` pixels.
- Outline border width increased to `2` pixels.
- Outline buttons use a consistent solid surface fill and border color.
- The Company logo **Upload Logo** button and other outline actions inherit the
  same sharper reusable style.
- The existing layout and overall mockup appearance were preserved.

## QA completed

- Reviewed reusable controls in `widgets/form_controls.py` and reusable cards in
  `widgets/cards.py`.
- Confirmed the scoped component dimensions use integer values.
- Checked action-button height, radius, border, fill, text, and icon consistency.
- Visually inspected the Settings and Reports sections for clipping, alignment,
  spacing, and corner symmetry.
- Confirmed Python source compilation succeeds.
- Confirmed the application starts successfully with the project interpreter.

Final visual acceptance should be performed on the client's Windows 10 or
Windows 11 computer at its normal display scale. Recommended QA scales are 100%,
125%, and 150% because rasterization can vary by monitor and Windows DPI setup.

## ML1 scope boundary

ML1 is a GUI and local-settings milestone. It does not include hardware/device
communication, production protocols, databases, a signed Windows installer, or
live measurement/configuration logic. Those areas remain future work.

## Delivered source files

- `main.py` — application entry point and page switching
- `requirements.txt` — required Python packages
- `START_WINDOWS.bat` — guided Windows setup and launcher
- `CLIENT_WINDOWS_GUIDE.md` — client setup, usage, and troubleshooting
- `README.md` — project overview and developer instructions
- `utils/`, `views/`, and `widgets/` — application source modules
