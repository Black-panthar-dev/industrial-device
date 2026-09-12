from views.communications_view import CommunicationsView


def test_communications_layout_breakpoints_are_dpi_independent() -> None:
    expected = CommunicationsView.get_layout_mode(1000, 1.0)
    assert CommunicationsView.get_layout_mode(1250, 1.25) == expected
    assert CommunicationsView.get_layout_mode(1500, 1.5) == expected


def test_communications_responsive_modes() -> None:
    assert CommunicationsView.get_layout_mode(1200) == (False, False, False)
    assert CommunicationsView.get_layout_mode(1000) == (True, False, False)
    assert CommunicationsView.get_layout_mode(680) == (True, True, True)
