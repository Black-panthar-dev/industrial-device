# QA Fix Plan – Power Monitor GUI

Status: Review and planning only. No implementation changes were made.

## Scope
This review covers the current Milestone 1 GUI framework and Settings screen for the Power Monitor desktop app. The plan stays within the current project structure and avoids hardware communication, Modbus, databases, and installer work.

---

## 1. File-by-file QA report

### [main.py](main.py)
Issues:
- The main window uses a fixed initial size and does not adapt dynamically enough to common Windows desktop resolutions and DPI scaling.
- The app currently has no app-level coordination for theme, translation, and persistence services.
- The window should be initialized with a sensible size based on screen resolution and scaling, while still allowing the Settings page to reorganize gracefully.

Assessment:
- Medium priority.
- This is a good place to centralize future app-level settings and theme behavior.

### [utils/theme.py](utils/theme.py)
Issues:
- Theme handling is currently light-only and does not provide a complete dark palette for all UI surfaces.
- Colors are hard-coded in several places rather than being driven by a theme layer.
- There is no separation between visual style constants and future localization/persistence logic.

Assessment:
- High priority for dark mode and future UI consistency.

### [views/settings_view.py](views/settings_view.py)
Issues:
- Responsive layout is the biggest concern. The current layout uses several fixed or semi-fixed column assumptions and can clip or squeeze content at smaller widths.
- The Current Configuration panel is currently treated as a static side panel and should be allowed to move below the main settings content at narrow widths.
- The Settings view uses many hard-coded strings, which makes translation and future localization difficult.
- The Company Logo upload option should be removed from the UI and architecture because the logo will be an application asset later.
- Keyboard navigation is not fully defined; tab order and Enter/Space activation need to be made consistent for ComboBoxes, entries, checkboxes, and buttons.
- The view creates a large number of widgets and performs redraw work during resize; this likely contributes to sluggish resizing behavior.
- The current layout logic uses resize events but does not fully optimize for performance or for very narrow window widths.

Assessment:
- Highest priority.
- This file is the main source of responsive behavior issues and UX pain points.

### [widgets/form_controls.py](widgets/form_controls.py)
Issues:
- ComboBoxes are visually under-styled and do not have a polished closed/opened state that matches the rest of the interface.
- Focus order and keyboard activation behavior are not explicitly managed.
- Enter/Space activation is not coordinated for controls such as buttons and checkboxes.
- The custom controls should expose a predictable keyboard interaction pattern and be wired into the parent form’s tab traversal.

Assessment:
- High priority.
- This is the best place to standardize focus, keyboard behavior, and ComboBox appearance.

### [widgets/cards.py](widgets/cards.py)
Issues:
- Cards and summary rows need darker-theme support and better scaling behavior for narrow widths.
- Some labels may wrap too aggressively or feel cramped on smaller resolutions.
- The component spacing should support responsive reflow without visual overlap.

Assessment:
- Medium priority.

### [widgets/sidebar.py](widgets/sidebar.py)
Issues:
- Sidebar layout should stay usable at smaller widths and different scaling factors.
- The current fixed sidebar width may be too rigid at very small windows.
- Dark theme support and keyboard navigation should be considered for all interactive sidebar controls.

Assessment:
- Medium priority.

### [widgets/icons.py](widgets/icons.py)
Issues:
- Icons are generated on demand and are not cached, which can add overhead when the UI is created or refreshed repeatedly.
- The current implementation is functional, but performance can be improved by caching generated images by name/size/color.

Assessment:
- Medium priority for performance improvement.

### [START_WINDOWS.bat](START_WINDOWS.bat)
Issues:
- The Python version gate contains a syntax error and does not match the client’s requested command.
- The launcher should be corrected to use the exact tested version check.

Assessment:
- High priority for Windows launcher reliability.

### [requirements.txt](requirements.txt)
Issues:
- Dependencies are not pinned to tested versions.
- This makes reproducibility and QA harder across Windows environments.

Assessment:
- Medium priority.

### [README.md](README.md)
Issues:
- Documentation still mentions the Company Logo upload feature and should be updated once the UI changes are finalized.
- The setup instructions should remain aligned with the pinned dependency versions and launcher behavior.

Assessment:
- Low priority.

---

## 2. Prioritized fix plan

### P0 – Stabilize Windows usability and layout
1. Refactor the Settings view layout into explicit responsive modes:
   - Wide mode: current side panel and main content layout remain as-is.
   - Medium mode: move the Current Configuration panel below the main settings content.
   - Narrow mode: stack the section menu and content vertically with a reduced-width panel.
2. Remove the Company Logo upload control from the Settings screen and related logic.
3. Improve resize handling so the layout is recalculated less aggressively and does not cause visible redraw lag.
4. Add explicit minimum supported window size behavior and ensure all major controls remain visible at the minimum size.

### P1 – Complete dark theme support
1. Introduce a dark palette in [utils/theme.py](utils/theme.py) and make all shared widgets use theme-aware colors rather than hard-coded light values.
2. Update cards, form controls, sidebar, labels, separators, and buttons to honor both light and dark modes consistently.
3. Review all remaining hard-coded colors in the UI and replace them with theme-driven values.

### P1 – Improve ComboBox UI and keyboard interaction
1. Improve the closed ComboBox styling by using stronger borders, better button color contrast, and more consistent padding.
2. Improve the opened dropdown appearance as much as CustomTkinter allows, while keeping the styling consistent with the rest of the app.
3. Add explicit focus order for ComboBoxes, entries, checkboxes, buttons, and any other interactive controls.
4. Add Enter and Space handling so focused controls activate properly.

### P1 – Prepare translation and settings architecture
1. Introduce a small translation service or translation loader, likely as a new module such as [utils/i18n.py](utils/i18n.py), with a JSON-based English dictionary.
2. Move all visible strings in [views/settings_view.py](views/settings_view.py) and other main views to the translation layer.
3. Add a small persistence abstraction for local application preferences and device configuration files, for example:
   - [utils/preferences_store.py](utils/preferences_store.py) for app preferences
   - [utils/device_config_store.py](utils/device_config_store.py) for device configurations
4. Keep the current JSON-based storage approach, but separate the responsibilities so future device config files are not mixed with application preferences.

### P1 – Performance and widget efficiency
1. Reduce unnecessary nested frame depth where possible for the Settings screen.
2. Avoid repeated full-layout rebuilds during resize; rely on debounced updates and only change layout mode when the breakpoint actually changes.
3. Cache generated icons in [widgets/icons.py](widgets/icons.py) to reduce repeated image creation overhead.
4. Review whether all sections need to be created up front for every launch; consider lazy construction if it improves startup and resize responsiveness.

### P2 – Launcher and dependency hygiene
1. Fix [START_WINDOWS.bat](START_WINDOWS.bat) to use the exact requested Python version check.
2. Pin tested dependency versions in [requirements.txt](requirements.txt) to match the verified Windows environment.
3. Update [README.md](README.md) to reflect the final launcher behavior and the removed logo feature.

---

## 3. Exact files that need changes

### Existing files
- [main.py](main.py)
- [utils/theme.py](utils/theme.py)
- [views/settings_view.py](views/settings_view.py)
- [widgets/form_controls.py](widgets/form_controls.py)
- [widgets/cards.py](widgets/cards.py)
- [widgets/sidebar.py](widgets/sidebar.py)
- [widgets/icons.py](widgets/icons.py)
- [START_WINDOWS.bat](START_WINDOWS.bat)
- [requirements.txt](requirements.txt)
- [README.md](README.md)

### New or additional files likely to be added
- [utils/i18n.py](utils/i18n.py) for translation loading and string access
- [utils/preferences_store.py](utils/preferences_store.py) for local application preference persistence
- [utils/device_config_store.py](utils/device_config_store.py) for future device configuration JSON files

---

## 4. Risks and limitations of CustomTkinter

### ComboBox dropdown styling
CustomTkinter can improve the closed ComboBox appearance reasonably well, but the opened dropdown menu is still partially constrained by the underlying Tkinter/ttk styling model on Windows. The following limitations should be expected:
- Full visual parity with a modern custom popup is not guaranteed.
- The dropdown border and text rendering may still look more native than fully custom.
- Some styling properties may be limited depending on the installed CustomTkinter version and Windows theme.

### Dark mode consistency
CustomTkinter supports theme switching, but achieving a fully consistent dark theme across all widgets still requires careful manual styling of separators, frames, labels, buttons, and scrollbars. It should not be assumed that changing appearance mode alone will make all controls match.

### Keyboard behavior
Keyboard focus and activation behavior can be improved, but some controls may still behave differently depending on platform and widget implementation. The plan should target the current Windows environment first and avoid over-engineering beyond the Milestone 1 scope.

### Performance
CustomTkinter is acceptable for this scope, but the current widget nesting and repeated resize work can create visible lag on Windows. The fix should focus on avoiding excessive redraws and reducing widget churn rather than moving to a completely different UI framework.

---

## 5. Short Windows test checklist

### Responsive layout
- Test at 1366×768 at 100% scaling.
- Test at 1920×1080 at 125% scaling.
- Test at 1920×1080 at 150% scaling.
- Test at the minimum supported window size.
- Verify that the Settings page remains usable and that the Current Configuration panel reflows below the main content when space is limited.
- Verify that no labels, buttons, or ComboBoxes are clipped or hidden.

### Dark mode
- Switch between Light and Dark modes.
- Confirm the sidebar, cards, buttons, labels, separators, and scrollbars all look coherent.
- Verify that the UI does not contain partially themed areas.

### ComboBox and keyboard interaction
- Open and close ComboBoxes.
- Verify the dropdown appearance is visually consistent with the rest of the app.
- Tab through all interactive controls in a logical order.
- Verify Shift+Tab moves in reverse order correctly.
- Verify Enter or Space activates focused buttons, checkboxes, and other appropriate controls.

### Performance
- Resize, maximize, and minimize the window repeatedly.
- Confirm redraw lag is reduced and the window remains responsive.

### Launcher and dependencies
- Run [START_WINDOWS.bat](START_WINDOWS.bat) on Windows.
- Verify the Python version check passes for Python 3.10+.
- Verify the pinned dependency versions install correctly.

---

## Implementation note
This plan is intentionally incremental and scoped to the current milestone. The goal is to improve the existing GUI without rewriting the app or introducing non-Milestone-1 features.
