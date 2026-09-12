from services.translation_service import t, translate_page_title
import ast
import json
from pathlib import Path


def test_english_translation_lookup_and_formatting() -> None:
    assert t("settings.title") == "Settings"
    assert t("placeholder.page", title="Dashboard") == "Dashboard page"


def test_missing_translation_falls_back_to_key() -> None:
    assert t("missing.translation.key") == "missing.translation.key"


def test_internal_page_names_are_translated_for_display() -> None:
    assert translate_page_title("Diagnostics") == "Diagnostics"
    assert translate_page_title("Live Measurements") == "Live Measurements"
    assert translate_page_title("Future Page") == "Future Page"


def test_ml2_page_shell_strings_are_translated() -> None:
    assert t("general.title") == "General"
    assert t("general.subtitle").startswith("Configure basic device information")
    assert t("measurements.title") == "Measurements"
    assert t("communications.title") == "Communications"


def test_all_literal_ml2_translation_keys_exist() -> None:
    locale = json.loads(Path("locales/en.json").read_text(encoding="utf-8"))
    missing: list[str] = []

    for filename in (
        "views/general_view.py",
        "views/measurements_view.py",
        "views/communications_view.py",
    ):
        tree = ast.parse(Path(filename).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
                continue
            if node.func.id != "t" or not node.args:
                continue
            key = node.args[0]
            if isinstance(key, ast.Constant) and isinstance(key.value, str):
                if key.value not in locale:
                    missing.append(f"{filename}: {key.value}")

    assert missing == []
