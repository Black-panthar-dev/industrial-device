from views.measurements_view import MeasurementsView


def test_measurements_layout_breakpoints_are_dpi_independent() -> None:
    expected = MeasurementsView.get_layout_mode(1000, 1.0)
    assert MeasurementsView.get_layout_mode(1250, 1.25) == expected
    assert MeasurementsView.get_layout_mode(1500, 1.5) == expected


def test_measurements_responsive_modes() -> None:
    assert MeasurementsView.get_layout_mode(1200) == (False, False, False)
    assert MeasurementsView.get_layout_mode(1000) == (True, False, False)
    assert MeasurementsView.get_layout_mode(680) == (True, True, True)
