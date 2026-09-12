# Power Monitor — ML2 QA Report

## QA status

**Result: Passed with one known pre-existing sidebar presentation issue.**

This report covers ML2 work completed through Chunk 3: navigation and screen
shells, the reusable ML2 component library, and the detailed General screen.
Measurements and Communications detailed forms are not included because their
requirements have not yet been implemented.

## Test environment

- Platform: Windows
- Python environment: project `.venv`
- GUI framework: CustomTkinter 5.2.2
- Image support: Pillow 10.4.0
- Test framework: pytest
- Test date: 12 September 2026

The live GUI checks were executed with Windows desktop access. Tkinter GUI
initialization is not supported inside the restricted command sandbox, so live
tests must run in a desktop-enabled process.

## Automated verification

- [x] Python source compilation succeeds.
- [x] English locale JSON parses successfully.
- [x] All ML1 regression tests continue to pass.
- [x] ML2 page registration tests pass.
- [x] Reusable component availability test passes.
- [x] General responsive breakpoint tests pass.
- [x] Full automated suite: **17 tests passed**.

## Navigation checks

- [x] Configuration > General opens `GeneralView`.
- [x] Configuration > Measurements opens `MeasurementsView`.
- [x] Configuration > Communications opens `CommunicationsView`.
- [x] Settings continues to open correctly.
- [x] The active sidebar item updates for each destination.
- [x] Navigating away from and back to General preserves the created page.

## General screen content checks

- [x] Page title and subtitle render.
- [x] Theme, Export Configuration, and Import Configuration controls render.
- [x] Device Identification section renders.
- [x] Date & Time section renders.
- [x] General Operation section renders.
- [x] Device Information Summary section renders.
- [x] Configuration Actions section renders.
- [x] Device Connection panel renders.
- [x] Device Summary panel renders.
- [x] Configuration Status panel renders.
- [x] Device connection information banner renders.
- [x] Required dummy values are present.
- [x] Read-only values use disabled-looking fields.

## Responsive and visual checks

Live rendering was checked at the largest available desktop size and at a
constrained 900 × 700 test window. Deterministic logical-width checks also
covered 1200, 1000, and 680 pixels.

- [x] Wide layout keeps the status area beside the form.
- [x] Medium layout moves the status area below the form.
- [x] Narrow layout changes form sections to one column.
- [x] Narrow layout moves header controls below the page heading.
- [x] Configuration actions reflow from four columns to two.
- [x] Main and right-panel content remains vertically scrollable.
- [x] Device Summary, Configuration Status, and the information banner are
  reachable at the bottom of the constrained layout.
- [x] No overlap was observed in the General page content.
- [x] No clipped General fields or action buttons were observed.

Windows may constrain a requested window size to the available work area. For
example, a requested height can be reduced to avoid the taskbar. This behavior
is controlled by Windows and is not an application layout failure.

## Theme checks

- [x] Light mode renders all General sections and shared ML2 components.
- [x] Dark mode renders all General sections and shared ML2 components.
- [x] The General header theme control switches both modes successfully.
- [x] New information, success, and read-only colors provide light/dark values.
- [x] No screen-specific hard-coded theme colors were introduced.

## Reusable component checks

- [x] All nine ML2 components instantiate in a live Tk window.
- [x] Components report valid, non-zero geometry.
- [x] `StatusRow`, `MetricValue`, and `ReadonlyField` update correctly.
- [x] `RadioGroup` selection and value retrieval work.
- [x] `ActionButtonRow` callbacks execute and buttons reflow.
- [x] `InlineInfoBanner` renders information and success variants.
- [x] `PageHeader` accepts top-right controls.

## Keyboard checks

- [x] Header action buttons respond to Enter and Space.
- [x] Configuration action buttons respond to Enter and Space.
- [x] Reusable radio choices support keyboard activation.
- [x] Existing ML1 keyboard behavior remains covered by regression tests.

## Placeholder-action checks

- [x] Export Configuration executes a placeholder action.
- [x] Import Configuration executes a placeholder action.
- [x] Synchronize with PC is a placeholder action.
- [x] Read from Device executes a placeholder action.
- [x] Write to Device executes a placeholder action.
- [x] Load from File executes a placeholder action.
- [x] Save to File executes a placeholder action.
- [x] No hardware, Modbus, serial, USB, or database logic is present.

## Known issue

### Configuration sidebar label truncation

The existing **Configuration** group label appears truncated on the tested
Windows layout (approximately `nfiguration`). The issue originates in the ML1
sidebar presentation logic and is not caused by the new General screen.

Priority: Low to medium. Navigation remains functional, but the label should be
corrected during a sidebar polish pass.

## Remaining QA

After detailed Measurements and Communications screens are implemented, repeat
the same checks for:

- Required fields and dummy values.
- Wide, medium, and narrow reflow.
- Light and Dark modes.
- Keyboard traversal and activation.
- Scroll reachability.
- Navigation and ML1 regression behavior.

