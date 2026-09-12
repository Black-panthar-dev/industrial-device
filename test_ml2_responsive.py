from views.communications_view import CommunicationsView
from views.general_view import GeneralView
from views.measurements_view import MeasurementsView


ML2_VIEWS = (GeneralView, MeasurementsView, CommunicationsView)


def test_ml2_views_share_responsive_breakpoints() -> None:
    for view_type in ML2_VIEWS:
        assert view_type.PANEL_REFLOW_WIDTH == 1120
        assert view_type.FORM_REFLOW_WIDTH == 720
        assert view_type.HEADER_REFLOW_WIDTH == 900
        assert view_type.RESIZE_DEBOUNCE_MS >= 100


def test_required_viewport_layouts() -> None:
    expected_modes = {
        1136: (False, False, False),  # 1366-wide window minus the sidebar
        1306: (False, False, False),  # 1920-wide window minus the sidebar
        1050: (True, False, False),   # 1280 logical px (1920 at 150%)
        530: (True, True, True),      # 760 px minimum window
    }

    for view_type in ML2_VIEWS:
        for viewport_width, expected in expected_modes.items():
            assert view_type.get_layout_mode(viewport_width) == expected


def test_required_viewports_are_dpi_independent() -> None:
    for view_type in ML2_VIEWS:
        for logical_width in (530, 1050, 1136, 1306):
            expected = view_type.get_layout_mode(logical_width, 1.0)
            assert view_type.get_layout_mode(logical_width * 1.25, 1.25) == expected
            assert view_type.get_layout_mode(logical_width * 1.5, 1.5) == expected
