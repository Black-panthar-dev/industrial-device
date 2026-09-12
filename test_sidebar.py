from services.translation_service import t
from widgets.sidebar import TOP_ITEMS


def test_configuration_navigation_uses_the_translated_label_without_padding() -> None:
    page_name, label_key, _icon = next(
        item for item in TOP_ITEMS if item[0] == "Configuration"
    )

    assert page_name == "Configuration"
    assert t(label_key) == "Configuration"
