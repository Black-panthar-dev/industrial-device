from views.general_view import GeneralView


def test_general_layout_breakpoints_are_dpi_independent() -> None:
    expected = GeneralView.get_layout_mode(1000, 1.0)
    assert GeneralView.get_layout_mode(1250, 1.25) == expected
    assert GeneralView.get_layout_mode(1500, 1.5) == expected


def test_general_responsive_modes() -> None:
    assert GeneralView.get_layout_mode(1200) == (False, False, False)
    assert GeneralView.get_layout_mode(1000) == (True, False, False)
    assert GeneralView.get_layout_mode(680) == (True, True, True)
