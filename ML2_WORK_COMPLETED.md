# Power Monitor — ML2 Work Completed

## Document status

This document records the Milestone 2 work completed through **Chunk 11**. The
General, Measurements, and Communications screens are implemented in detail
within the approved GUI-only scope.

## ML2 scope

Milestone 2 covers these configuration screens:

- General
- Measurements
- Communications

The milestone remains GUI-only. Values and actions are local placeholders. It
does not include hardware communication, Modbus logic, real serial or USB
communication, a database, or an installer.

## Chunk 1 — Screen structure and navigation

- Added dedicated General, Measurements, and Communications view modules.
- Connected all three views to the existing Configuration sidebar navigation.
- Added translated page titles and subtitles.
- Preserved the ML1 Settings screen and all existing navigation destinations.
- Reused the existing theme and translation services.

## Chunk 2 — Reusable UI components

Added reusable CustomTkinter components in `widgets/ml2_components.py`:

- `PageHeader` for titles, subtitles, and optional header controls.
- `StatusPanel` for side-panel status cards.
- `StatusRow` for label/value status information.
- `MetricValue` for highlighted measurement values and units.
- `SectionHeader` for numbered section headings.
- `ReadonlyField` for disabled-looking display values.
- `ActionButtonRow` for reusable, reflowable action buttons.
- `InlineInfoBanner` for information and success messages.
- `RadioGroup` for horizontal or vertical measurement-mode choices.

The central theme palette was extended with light/dark information, success,
and read-only field colors. Buttons and radio choices include keyboard support
where practical.

## Chunk 3 — General screen

The production General screen now includes:

### Header controls

- Light/Dark theme selection.
- Export Configuration placeholder action.
- Import Configuration placeholder action.

### Main sections

1. Device Identification
2. Date & Time
3. General Operation
4. Device Information Summary
5. Configuration Actions

The required dummy device, site, version, date/time, interval, status, and
configuration values are present. Read-only device information uses dedicated
read-only controls.

### Right-side status area

- Device Connection
- Device Summary
- Configuration Status
- Device connection information banner

### Responsive behavior

- The right-side status area moves below the main form when width is limited.
- Form controls reflow from two columns to one column at narrow widths.
- Header controls move below the title at narrow widths.
- Configuration action buttons reflow from four columns to two columns.
- The complete page remains vertically scrollable.

## Placeholder behavior

The following actions only print a descriptive placeholder message:

- Export Configuration
- Import Configuration
- Synchronize with PC
- Read from Device
- Write to Device
- Load from File
- Save to File

No action communicates with a device or performs Modbus, serial, or USB work.

## Chunk 4 — Measurements screen

The production Measurements screen now provides Voltage Measurement, Current
Measurement, Measurement Processing, Calculated Measurements, and Measurement
Status sections. It includes both internal and external shunt settings, live
dummy voltage/current values, calculated-value controls, and the required Live
Measurements, Measurement Status, and Information side panels.

The screen uses 22 explicit keyboard focus targets covering header controls,
checkboxes, radio choices, dropdowns, entries, and buttons. Its right panel,
form fields, and header controls reflow at the same responsive modes used by
General. All displayed measurement values remain placeholders.

## Chunk 5 — Communications screen

The production Communications screen now provides RS485 / Modbus RTU, RS232,
USB Interface, and Expansion / Communication Module sections. It contains the
required dummy serial parameters and packet counters, USB information, 4G
module values, masked Password/PIN entries, and 4G/Module Information segmented
navigation.

Communication Status, Network Status, and Configuration Status panels appear
beside the form at wide widths and move below it at constrained widths. The
screen contains 24 explicit keyboard focus targets and 12 theme-aware dropdowns.
All actions are placeholders; no protocol or device communication is present.

## Chunk 6 — Translation architecture

All visible ML2 labels, section headings, helper text, dropdown options, dummy
display values, and placeholder messages are centralized in `locales/en.json`.
Section keys use organized namespaces such as `general.sections.*`,
`measurements.sections.*`, and `communications.sections.*`. The three production
views use the existing `t()` translation helper, and sidebar labels remain
centralized under `sidebar.*`.

An automated AST-based check verifies that every literal ML2 translation key
used by the views exists in the English locale. Live GUI inspection also
confirms that no dotted fallback keys appear on any ML2 screen.

## Chunk 7 — Keyboard navigation

All three ML2 screens use the shared explicit focus-chain utility. General has
18 focus targets, Measurements has 22, and Communications has 24. Tab and
Shift+Tab traverse in visual order and wrap at the ends of each screen.

Shared ComboBoxes open with Enter, keypad Enter, Space, or Down. Their popup
choices support Up/Down navigation, Enter selection, and Escape closing.
Buttons support Enter and Space, checkboxes and radio choices support Space,
and Communications segmented tabs are included in the normal focus order.
Mouse command behavior remains unchanged.

## Chunk 8 — Responsive layout QA

General, Measurements, and Communications were audited at 1366 × 768, at
1920 × 1080 DPI-equivalent logical sizes for 125% and 150% scaling, and at the
760 × 540 minimum test window. All three views use the same DPI-normalized
breakpoints and a 180 ms resize debounce. Resizing only changes grid placement;
it does not destroy or rebuild screen content.

The right status panel remains beside the main form when the content viewport
is at least 1120 logical pixels wide and moves below it at narrower widths.
Form groups switch to one column below 720 logical pixels, while page-header
controls move below the title below 900 logical pixels. At the minimum layout,
the three header controls now reflow to two columns so no button is squeezed or
cut off. All page content remains vertically scrollable.

## Chunk 9 — Light/Dark theme QA

General, Measurements, Communications, and Settings were rendered and switched
live between Light and Dark modes. All paired theme values resolved correctly,
and the dark render contained no unintended white card or panel surfaces.
Entries, ComboBoxes, checkboxes, radio buttons, buttons, banners, section cards,
read-only fields, scrollbars, and right-side status panels use centralized theme
tokens.

Operational states such as Connected, Ready, OK, Available, and Synchronized
use the shared success color where they appear as status values. Success,
danger, normal text, and muted text tokens meet a 4.5:1 contrast threshold
against their corresponding card surfaces in both appearance modes. Automated
checks also reject literal hex colors added directly to ML2 production views.

## Chunk 10 — Performance cleanup

The three ML2 screens now share `DebouncedResponsiveMixin` instead of carrying
three copies of the resize scheduling code. Resize events within the current
breakpoint perform no scheduled work, repeated events headed toward the same
breakpoint reuse one pending timer, and minimized one-pixel geometry events are
ignored. If a drag returns to the active breakpoint before the debounce expires,
the pending reflow is cancelled.

Breakpoint changes only update the grid positions and weights of existing
widgets. Pages, cards, fields, and scrollable frames are never destroyed or
recreated by resize callbacks. Each ML2 page retains one scrollable workspace.
The existing icon factory already caches both `CTkImage` instances and rendered
Pillow images with bounded LRU caches, so no additional image churn occurs.

## Chunk 11 — Delivery tests and README

The delivery includes the complete lightweight automated suite. Explicit checks
now cover application and view imports, required translation strings, paired
theme colors, ML2 page registration, exact runtime dependency pins, and the
Windows launcher's ML2 entry point. Tests remain hardware-independent and do
not initialize Modbus, serial/USB communication, networking, or a database.

The README now identifies the product as Power Monitor, documents the full ML2
GUI scope and exclusions, describes `START_WINDOWS.bat`, manual Python startup,
and test commands, and records the dependency versions used for QA. The stale
Milestone 1 launcher heading was updated to Milestone 2. Runtime and development
dependencies are pinned for reproducible delivery.

## Files created during ML2

- `views/general_view.py`
- `views/measurements_view.py`
- `views/communications_view.py`
- `widgets/ml2_components.py`
- `test_ml2_navigation.py`
- `test_ml2_components.py`
- `test_general_view.py`
- `test_measurements_view.py`
- `test_communications_view.py`
- `test_ml2_responsive.py`
- `test_ml2_theme_qa.py`
- `test_responsive_scheduler.py`
- `test_ml2_delivery.py`
- `ML2_WORK_COMPLETED.md`
- `ML2_QA_REPORT.md`

## Existing files updated during ML2

- `main.py` — dedicated ML2 page routing.
- `views/placeholder_view.py` — optional subtitle support.
- `widgets/ml2_components.py` — responsive action-row support.
- `utils/theme.py` — semantic light/dark colors for ML2 components.
- `locales/en.json` — centralized ML2 interface text.
- `test_translation.py` — ML2 translation coverage.

## Current milestone boundary

All three ML2 screens are implemented within the GUI-only milestone boundary.
Hardware communication, Modbus behavior, serial/USB access, 4G networking,
database storage, and installer work remain explicitly excluded.

## Run the application

From the project directory:

```powershell
python main.py
```

Alternatively, use the project interpreter directly:

```powershell
.\.venv\Scripts\python.exe main.py
```

Use the Configuration group to inspect the General, Measurements, and
Communications screens.
