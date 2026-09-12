from models import AppPreferences, DeviceConfiguration


def test_preferences_and_device_configuration_are_separate_models() -> None:
    preferences = AppPreferences(values={"theme": "Dark"})
    device = DeviceConfiguration(name="Meter 1", values={"baudrate": 115200})

    assert preferences.values == {"theme": "Dark"}
    assert device.values == {"baudrate": 115200}
    assert "theme" not in device.values


def test_model_value_mappings_are_not_shared() -> None:
    first_preferences = AppPreferences()
    second_preferences = AppPreferences()
    first_device = DeviceConfiguration()
    second_device = DeviceConfiguration()

    assert first_preferences.values is not second_preferences.values
    assert first_device.values is not second_device.values
