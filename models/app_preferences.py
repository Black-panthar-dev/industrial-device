"""Model boundary for local Power Monitor application preferences."""

from dataclasses import dataclass, field


PreferenceValue = str | bool


@dataclass(slots=True)
class AppPreferences:
    """Preferences that belong to this application installation.

    A future preferences store may load and save this model automatically in a
    local application-data location. These values must remain separate from
    device configuration files, which users will manage individually.

    Persistence is intentionally not implemented in this milestone.
    """

    values: dict[str, PreferenceValue] = field(default_factory=dict)
