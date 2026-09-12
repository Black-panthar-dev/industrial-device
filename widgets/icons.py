"""Small Pillow-rendered line icons used by the CustomTkinter interface."""

from collections.abc import Callable
from functools import lru_cache

import customtkinter as ctk
from PIL import Image, ImageDraw

from utils.theme import COLOR_TEXT_MUTED, ThemeColor


Point = tuple[int, int]


@lru_cache(maxsize=128)
def create_icon(
    name: str, size: int = 18, color: ThemeColor = COLOR_TEXT_MUTED
) -> ctk.CTkImage:
    """Return a crisp, scalable line icon without external asset files."""
    light_color, dark_color = color if isinstance(color, tuple) else (color, color)

    return ctk.CTkImage(
        light_image=_render_icon(name, size, light_color),
        dark_image=_render_icon(name, size, dark_color),
        size=(size, size),
    )


@lru_cache(maxsize=256)
def _render_icon(name: str, size: int, color: str) -> Image.Image:
    """Render one appearance-specific Pillow icon image."""
    scale = 4
    canvas_size = size * scale
    image = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    width = max(4, scale * 2)

    def point(x: float, y: float) -> Point:
        return int(x * canvas_size), int(y * canvas_size)

    def line(points: list[tuple[float, float]], fill: str = color) -> None:
        draw.line([point(x, y) for x, y in points], fill=fill, width=width, joint="curve")

    def rect(box: tuple[float, float, float, float], radius: float = 0.0) -> None:
        xy = (*point(box[0], box[1]), *point(box[2], box[3]))
        if radius:
            draw.rounded_rectangle(xy, radius=int(radius * canvas_size), outline=color, width=width)
        else:
            draw.rectangle(xy, outline=color, width=width)

    def ellipse(box: tuple[float, float, float, float], fill: str | None = None) -> None:
        draw.ellipse(
            (*point(box[0], box[1]), *point(box[2], box[3])),
            outline=color,
            fill=fill,
            width=width,
        )

    def dot(x: float, y: float, radius: float = 0.06) -> None:
        draw.ellipse(
            (*point(x - radius, y - radius), *point(x + radius, y + radius)),
            fill=color,
        )

    drawers: dict[str, Callable[[], None]] = {
        "dashboard": lambda: (rect((0.2, 0.36, 0.8, 0.82), 0.06), line([(0.14, 0.43), (0.5, 0.14), (0.86, 0.43)])),
        "activity": lambda: line([(0.08, 0.55), (0.27, 0.55), (0.38, 0.2), (0.55, 0.82), (0.67, 0.43), (0.92, 0.43)]),
        "settings": lambda: (ellipse((0.29, 0.29, 0.71, 0.71)), ellipse((0.43, 0.43, 0.57, 0.57), fill=color), line([(0.5, 0.08), (0.5, 0.25)]), line([(0.5, 0.75), (0.5, 0.92)]), line([(0.08, 0.5), (0.25, 0.5)]), line([(0.75, 0.5), (0.92, 0.5)])),
        "general": lambda: (ellipse((0.3, 0.3, 0.7, 0.7)), dot(0.5, 0.5, 0.08), line([(0.5, 0.08), (0.5, 0.25)]), line([(0.5, 0.75), (0.5, 0.92)])),
        "measurements": lambda: (line([(0.15, 0.75), (0.15, 0.48), (0.38, 0.48), (0.38, 0.28), (0.62, 0.28), (0.62, 0.58), (0.85, 0.58), (0.85, 0.18)]), line([(0.13, 0.83), (0.87, 0.83)])),
        "communications": lambda: (line([(0.12, 0.4), (0.5, 0.72), (0.88, 0.4)]), line([(0.25, 0.25), (0.5, 0.45), (0.75, 0.25)]), dot(0.5, 0.78, 0.05)),
        "relays": lambda: (ellipse((0.16, 0.16, 0.84, 0.84)), line([(0.28, 0.72), (0.72, 0.28)]), dot(0.3, 0.3, 0.04), dot(0.7, 0.7, 0.04)),
        "alarms": lambda: (line([(0.22, 0.72), (0.3, 0.62), (0.3, 0.4), (0.38, 0.23), (0.62, 0.23), (0.7, 0.4), (0.7, 0.62), (0.78, 0.72), (0.22, 0.72)]), line([(0.43, 0.82), (0.57, 0.82)])),
        "io": lambda: (ellipse((0.15, 0.15, 0.85, 0.85)), line([(0.5, 0.3), (0.5, 0.7)]), line([(0.3, 0.5), (0.7, 0.5)])),
        "logging": lambda: (rect((0.18, 0.14, 0.82, 0.86), 0.05), line([(0.3, 0.65), (0.43, 0.5), (0.56, 0.58), (0.7, 0.34)])),
        "commissioning": lambda: (line([(0.2, 0.22), (0.78, 0.8)]), line([(0.7, 0.15), (0.85, 0.3), (0.34, 0.81), (0.18, 0.82), (0.19, 0.66), (0.7, 0.15)])),
        "diagnostics": lambda: (rect((0.14, 0.28, 0.86, 0.82), 0.06), rect((0.36, 0.14, 0.64, 0.3), 0.04), line([(0.14, 0.47), (0.86, 0.47)]), line([(0.44, 0.47), (0.44, 0.57), (0.56, 0.57), (0.56, 0.47)])),
        "logs": lambda: (rect((0.2, 0.12, 0.8, 0.88), 0.03), line([(0.33, 0.32), (0.68, 0.32)]), line([(0.33, 0.5), (0.68, 0.5)]), line([(0.33, 0.68), (0.68, 0.68)])),
        "maintenance": lambda: (line([(0.18, 0.82), (0.75, 0.25)]), ellipse((0.1, 0.7, 0.3, 0.9)), line([(0.63, 0.14), (0.85, 0.14), (0.85, 0.36)])),
        "connection": lambda: (line([(0.25, 0.12), (0.25, 0.42)]), line([(0.75, 0.12), (0.75, 0.42)]), line([(0.14, 0.42), (0.86, 0.42)]), line([(0.5, 0.42), (0.5, 0.88)])),
        "application": lambda: (rect((0.12, 0.12, 0.42, 0.42)), rect((0.58, 0.12, 0.88, 0.42)), rect((0.12, 0.58, 0.42, 0.88)), rect((0.58, 0.58, 0.88, 0.88))),
        "security": lambda: (rect((0.2, 0.42, 0.8, 0.88), 0.06), line([(0.32, 0.42), (0.32, 0.28), (0.4, 0.14), (0.6, 0.14), (0.68, 0.28), (0.68, 0.42)]), dot(0.5, 0.62, 0.05)),
        "reports": lambda: (rect((0.2, 0.1, 0.8, 0.9), 0.04), line([(0.58, 0.1), (0.58, 0.32), (0.8, 0.32)]), line([(0.33, 0.52), (0.67, 0.52)]), line([(0.33, 0.68), (0.67, 0.68)])),
        "help": lambda: (ellipse((0.12, 0.12, 0.88, 0.88)), line([(0.36, 0.38), (0.42, 0.28), (0.58, 0.28), (0.66, 0.38), (0.52, 0.52), (0.5, 0.62)]), dot(0.5, 0.76, 0.035)),
        "info": lambda: (ellipse((0.12, 0.12, 0.88, 0.88)), dot(0.5, 0.31, 0.04), line([(0.5, 0.45), (0.5, 0.72)])),
        "download": lambda: (line([(0.5, 0.12), (0.5, 0.62)]), line([(0.3, 0.45), (0.5, 0.65), (0.7, 0.45)]), line([(0.18, 0.78), (0.82, 0.78)])),
        "upload": lambda: (line([(0.5, 0.68), (0.5, 0.18)]), line([(0.3, 0.35), (0.5, 0.15), (0.7, 0.35)]), line([(0.18, 0.82), (0.82, 0.82)])),
        "sun": lambda: (ellipse((0.3, 0.3, 0.7, 0.7)), line([(0.5, 0.05), (0.5, 0.2)]), line([(0.5, 0.8), (0.5, 0.95)]), line([(0.05, 0.5), (0.2, 0.5)]), line([(0.8, 0.5), (0.95, 0.5)])),
        "refresh": lambda: (line([(0.75, 0.28), (0.85, 0.42), (0.68, 0.43)]), line([(0.8, 0.42), (0.68, 0.22), (0.42, 0.17), (0.2, 0.32), (0.16, 0.58), (0.32, 0.8), (0.58, 0.83), (0.78, 0.68)])),
    }
    drawers.get(name, drawers["info"])()
    image = image.resize((size, size), Image.Resampling.LANCZOS)
    return image
