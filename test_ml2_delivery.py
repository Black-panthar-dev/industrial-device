"""Lightweight delivery checks that do not create a GUI window."""

import importlib
import json
from pathlib import Path

import main
from services.translation_service import t
from utils import theme
from views.communications_view import CommunicationsView
from views.general_view import GeneralView
from views.measurements_view import MeasurementsView


def test_application_and_ml2_modules_import() -> None:
    modules = (
        "main",
        "views.general_view",
        "views.measurements_view",
        "views.communications_view",
        "views.settings_view",
    )

    assert all(importlib.import_module(name) is not None for name in modules)
    assert main.IndustrialDeviceConfiguratorApp is not None


def test_required_ml2_translation_keys_load() -> None:
    locale = json.loads(Path("locales/en.json").read_text(encoding="utf-8"))
    required = (
        "general.title",
        "general.subtitle",
        "measurements.title",
        "measurements.subtitle",
        "communications.title",
        "communications.subtitle",
    )

    assert all(key in locale for key in required)
    assert all(t(key) != key for key in required)


def test_required_theme_colors_load_as_light_dark_pairs() -> None:
    required = (
        theme.COLOR_BACKGROUND,
        theme.COLOR_SURFACE,
        theme.COLOR_TEXT,
        theme.COLOR_PRIMARY,
        theme.COLOR_SUCCESS,
        theme.COLOR_DANGER,
    )

    assert all(isinstance(color, tuple) and len(color) == 2 for color in required)


def test_ml2_pages_are_registered_without_starting_hardware_services() -> None:
    registered_names = main.IndustrialDeviceConfiguratorApp.show_page.__code__.co_names

    assert GeneralView.__name__ in registered_names
    assert MeasurementsView.__name__ in registered_names
    assert CommunicationsView.__name__ in registered_names


def test_runtime_dependencies_are_exactly_pinned() -> None:
    requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()
    packages = [line.strip() for line in requirements if line.strip() and not line.startswith("#")]

    assert packages
    assert all("==" in package for package in packages)


def test_windows_launcher_targets_ml2_application() -> None:
    launcher = Path("START_WINDOWS.bat").read_text(encoding="utf-8")

    assert "Power Monitor - Milestone 2" in launcher
    assert "-r requirements.txt" in launcher
    assert "python main.py" in launcher
