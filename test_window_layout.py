from main import get_initial_window_geometry, get_minimum_window_size
from views.settings_view import SettingsView


def test_get_initial_window_geometry_scales_reasonably() -> None:
    geometry = get_initial_window_geometry(1920, 1080)
    assert geometry == "1500x885"

    geometry = get_initial_window_geometry(1280, 720)
    assert geometry == "1049x590"


def test_window_size_adapts_to_dpi_reduced_screen_coordinates() -> None:
    # A 1366x768 display is reported as about 1093x614 logical pixels at 125%.
    assert get_minimum_window_size(1093, 614) == (819, 460)
    assert get_initial_window_geometry(1093, 614) == "896x503"

    # At 150%, the same display reports approximately 911x512 logical pixels.
    assert get_minimum_window_size(911, 512) == (760, 400)
    assert get_initial_window_geometry(911, 512) == "760x419"


def test_layout_decisions_are_consistent_across_dpi_scaling() -> None:
    logical_width = 970
    expected = SettingsView.get_layout_mode(logical_width, 1.0)

    assert SettingsView.get_layout_mode(logical_width * 1.25, 1.25) == expected
    assert SettingsView.get_layout_mode(logical_width * 1.5, 1.5) == expected
    assert expected == (True, False, False, 2)


def test_narrow_layout_uses_one_form_column() -> None:
    assert SettingsView.get_layout_mode(570, 1.0) == (True, True, True, 1)


def test_wide_layout_keeps_right_panel_beside_form() -> None:
    panel_below, menu_above, header_stacked, columns = (
        SettingsView.get_layout_mode(1600, 1.0)
    )

    assert panel_below is False
    assert menu_above is False
    assert header_stacked is False
    assert columns == 3
