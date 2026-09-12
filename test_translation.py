from services.translation_service import t, translate_page_title


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
