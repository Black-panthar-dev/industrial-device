import ast
from pathlib import Path

from utils import theme


ML2_VIEW_PATHS = (
    Path("views/general_view.py"),
    Path("views/measurements_view.py"),
    Path("views/communications_view.py"),
)


def _luminance(hex_color: str) -> float:
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        value / 12.92
        if value <= 0.04045
        else ((value + 0.055) / 1.055) ** 2.4
        for value in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(first: str, second: str) -> float:
    lighter, darker = sorted((_luminance(first), _luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def test_ml2_views_do_not_define_literal_hex_colors() -> None:
    violations: list[str] = []
    for path in ML2_VIEW_PATHS:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and node.value.startswith("#")
            ):
                violations.append(f"{path}:{node.lineno}")

    assert violations == []


def test_status_and_danger_colors_remain_readable_in_both_modes() -> None:
    foreground_tokens = (theme.COLOR_SUCCESS, theme.COLOR_DANGER)
    surfaces = (theme.COLOR_SURFACE[0], theme.COLOR_SURFACE[1])

    for token in foreground_tokens:
        assert _contrast(token[0], surfaces[0]) >= 4.5
        assert _contrast(token[1], surfaces[1]) >= 4.5


def test_normal_and_muted_text_remain_readable_in_both_modes() -> None:
    for token in (theme.COLOR_TEXT, theme.COLOR_TEXT_MUTED):
        assert _contrast(token[0], theme.COLOR_SURFACE[0]) >= 4.5
        assert _contrast(token[1], theme.COLOR_SURFACE[1]) >= 4.5
