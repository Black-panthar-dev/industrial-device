# Power Monitor — ML2 QA Report

## QA status

**Result: Passed with one known pre-existing sidebar presentation issue.**

This report covers ML2 work completed through Chunk 7: the reusable ML2
component library and the detailed General, Measurements, and Communications
screens.

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
- [x] Full automated suite: **23 tests passed**.

## Translation checks

- [x] General, Measurements, and Communications use the existing `t()` helper.
- [x] ML2 section keys use organized `*.sections.*` namespaces.
- [x] Visible dropdown options and dummy display values are centralized.
- [x] Sidebar labels remain centralized under `sidebar.*`.
- [x] Automated AST inspection finds no missing literal ML2 translation keys.
- [x] Live rendering finds no dotted translation-key fallbacks in any ML2 view.

## ML2 keyboard navigation checks

- [x] General exposes 18 controls in explicit visual focus order.
- [x] Measurements exposes 22 controls in explicit visual focus order.
- [x] Communications exposes 24 controls in explicit visual focus order.
- [x] Tab advances, Shift+Tab reverses, and traversal wraps on all three views.
- [x] Entries accept keyboard focus.
- [x] ComboBoxes open by keyboard and support arrow navigation and selection.
- [x] Space toggles focused checkboxes and radio choices.
- [x] Enter activates focused action buttons.
- [x] Communications segmented tabs activate through the keyboard.
- [x] Normal mouse/command invocation remains functional.

## Measurements screen checks

- [x] All five required configuration sections render.
- [x] All three required right-side panels render.
- [x] Voltage and current dummy metrics render with highlighted values.
- [x] Internal, external, and automatic measurement modes are available.
- [x] Internal and external shunt settings render.
- [x] Right panel moves below the main content at constrained widths.
- [x] Header controls reflow at constrained widths.
- [x] Light and Dark themes apply without runtime errors.
- [x] Export, Import, and Reset Energy Counters remain placeholder actions.
- [x] The explicit focus chain contains 22 targets.
- [x] Tab, Shift+Tab, wrapping traversal, and radio Space activation pass.
- [x] Navigation to other ML2 screens and Settings remains functional.

## Communications screen checks

- [x] All four required communication sections render.
- [x] RS485 and RS232 settings and dummy packet counters render.
- [x] USB information and its maintenance banner render.
- [x] Expansion-module and 4G settings render.
- [x] Password and PIN fields visually mask their values.
- [x] 4G Settings and Module Information segmented choices work.
- [x] All 12 dropdowns open and close successfully.
- [x] All three right-side status panels and the information banner render.
- [x] Right panel and header controls reflow at constrained widths.
- [x] The explicit focus chain contains 24 targets.
- [x] Tab, Shift+Tab, and wrapping keyboard traversal pass.
- [x] Light and Dark themes apply without runtime errors.
- [x] Export and Import actions remain placeholders.
- [x] Navigation to other ML2 screens and Settings remains functional.

## PDF mockup rendering

The ML2 mockup can be rendered for local visual QA with the development-only
PDFium utility. Install development requirements, then render a page:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe tools\render_pdf.py C:\path\to\ML2.pdf mockup-page-1.png --page 1
```

This renderer was verified against all three pages of the supplied `ML2.pdf`.
Pages render at 1263 × 893 using the default 1.5 scale. PDFium is kept out of
`requirements.txt`, so it does not affect the production application.

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

## Resolved issue

### Configuration sidebar label truncation

The existing **Configuration** group label previously appeared truncated on the
tested Windows layout (approximately `nfiguration`). The issue originated in a
manual spacing/caret suffix in the ML1 sidebar presentation logic.

Resolved on 12 September 2026 by removing the spacing suffix and rendering the
centralized translated label directly. Live Windows rendering confirms that the
complete **Configuration** label is now visible.

### Expansion/4G narrow-layout clipping

The Communications Expansion/4G cards previously collapsed into a narrow
column at the 900 × 700 constrained layout because their old two-column Tk
`uniform` group remained active after the controls moved to one column.

Resolved on 12 September 2026 by clearing the uniform group in one-column mode
and restoring it only in two-column mode. Live Windows QA confirms that module
values, segmented tabs, labels, and masked Password/PIN fields now use the full
available width.

## Remaining QA

For later device-integration milestones, repeat the same checks for:

- Required fields and dummy values.
- Wide, medium, and narrow reflow.
- Light and Dark modes.
- Keyboard traversal and activation.
- Scroll reachability.
- Navigation and ML1 regression behavior.
