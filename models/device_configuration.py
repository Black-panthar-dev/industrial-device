"""Model boundary for independently saved Power Monitor device files."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DeviceConfiguration:
    """Configuration data for one device configuration document.

    Each instance will eventually be serialized to its own user-selected JSON
    file. It must not contain application preferences such as theme, language,
    start page, or other settings local to the desktop application.

    File selection, JSON serialization, validation, and device communication
    are intentionally deferred to later milestones.
    """

    name: str = ""
    device_type: str = "Power Monitor"
    values: dict[str, Any] = field(default_factory=dict)
