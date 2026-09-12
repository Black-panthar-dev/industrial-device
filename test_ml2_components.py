from widgets.ml2_components import (
    ActionButtonRow,
    InlineInfoBanner,
    MetricValue,
    PageHeader,
    RadioGroup,
    ReadonlyField,
    SectionHeader,
    StatusPanel,
    StatusRow,
)


def test_required_ml2_components_are_available() -> None:
    components = (
        PageHeader,
        StatusPanel,
        StatusRow,
        MetricValue,
        SectionHeader,
        ReadonlyField,
        ActionButtonRow,
        InlineInfoBanner,
        RadioGroup,
    )

    assert all(component.__module__ == "widgets.ml2_components" for component in components)
