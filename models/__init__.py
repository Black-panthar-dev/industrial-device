"""Domain models kept independent from UI and future storage services."""

from models.app_preferences import AppPreferences
from models.device_configuration import DeviceConfiguration

__all__ = ["AppPreferences", "DeviceConfiguration"]
