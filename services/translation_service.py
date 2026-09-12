"""Small cached JSON translation service with dotted string keys."""

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


LOCALES_DIR = Path(__file__).resolve().parent.parent / "locales"

PAGE_TITLE_KEYS = {
    "Dashboard": "sidebar.dashboard",
    "Live Measurements": "sidebar.live_measurements",
    "Configuration": "sidebar.configuration",
    "General": "sidebar.general",
    "Measurements": "sidebar.measurements",
    "Communications": "sidebar.communications",
    "Relays": "sidebar.relays",
    "Alarms": "sidebar.alarms",
    "I/O": "sidebar.io",
    "Data Logging": "sidebar.data_logging",
    "Commissioning": "sidebar.commissioning",
    "Diagnostics": "sidebar.diagnostics",
    "Logs": "sidebar.logs",
    "Maintenance": "sidebar.maintenance",
    "Settings": "settings.title",
}


@lru_cache(maxsize=4)
def _load_locale(language: str) -> dict[str, str]:
    path = LOCALES_DIR / f"{language}.json"
    values = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(values, dict):
        raise ValueError(f"Locale must contain a JSON object: {path}")
    return {str(key): str(value) for key, value in values.items()}


def t(key: str, *, language: str = "en", **values: Any) -> str:
    """Return a translated string, falling back to the key when missing."""
    text = _load_locale(language).get(key, key)
    return text.format(**values) if values else text


def translate_page_title(page_name: str, *, language: str = "en") -> str:
    """Translate a stable internal navigation identifier for display."""
    key = PAGE_TITLE_KEYS.get(page_name)
    return t(key, language=language) if key is not None else page_name
