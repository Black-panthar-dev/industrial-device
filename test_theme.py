import customtkinter as ctk

from utils import theme
from widgets.icons import create_icon


def test_visual_colors_define_light_and_dark_values() -> None:
    color_names = (
        name
        for name in dir(theme)
        if name.startswith("COLOR_")
    )

    for name in color_names:
        value = getattr(theme, name)
        assert isinstance(value, tuple), name
        assert len(value) == 2, name
        assert all(isinstance(color, str) and color.startswith("#") for color in value)


def test_icons_support_appearance_specific_colors() -> None:
    icon = create_icon("settings", 18, theme.COLOR_TEXT_MUTED)
    cached_icon = create_icon("settings", 18, theme.COLOR_TEXT_MUTED)

    assert isinstance(icon, ctk.CTkImage)
    assert icon.cget("light_image") is not icon.cget("dark_image")
    assert cached_icon is icon
