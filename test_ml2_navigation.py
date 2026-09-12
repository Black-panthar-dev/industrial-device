from main import IndustrialDeviceConfiguratorApp
from views.communications_view import CommunicationsView
from views.general_view import GeneralView
from views.measurements_view import MeasurementsView


def test_ml2_views_are_registered_in_page_navigation() -> None:
    source_names = IndustrialDeviceConfiguratorApp.show_page.__code__.co_names

    assert GeneralView.__name__ in source_names
    assert MeasurementsView.__name__ in source_names
    assert CommunicationsView.__name__ in source_names
