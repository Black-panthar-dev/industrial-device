"""Central light/dark visual palette for the application."""

from typing import TypeAlias


ThemeColor: TypeAlias = str | tuple[str, str]

APP_APPEARANCE_MODE = "light"
APP_COLOR_THEME = "blue"
SIDEBAR_WIDTH = 230

# Each pair is (light, dark), as supported natively by CustomTkinter.
COLOR_BACKGROUND: ThemeColor = ("#FAFCFE", "#0B1220")
COLOR_SIDEBAR: ThemeColor = ("#FFFFFF", "#111827")
COLOR_SURFACE: ThemeColor = ("#FFFFFF", "#151F2E")
COLOR_SURFACE_ALT: ThemeColor = ("#EAF1F7", "#26364A")
COLOR_BORDER: ThemeColor = ("#DCE5EF", "#334155")
COLOR_PRIMARY: ThemeColor = ("#0875F5", "#3B82F6")
COLOR_PRIMARY_HOVER: ThemeColor = ("#0066DD", "#2563EB")
COLOR_TEXT: ThemeColor = ("#0C1833", "#E5EDF7")
COLOR_TEXT_MUTED: ThemeColor = ("#4D6080", "#94A3B8")
COLOR_ON_PRIMARY: ThemeColor = ("#FFFFFF", "#FFFFFF")

COLOR_HOVER: ThemeColor = ("#EAF3FE", "#1E3046")
COLOR_ACTIVE: ThemeColor = ("#E7F2FF", "#173B63")
COLOR_ACTIVE_HOVER: ThemeColor = ("#DCEEFF", "#214E7D")
COLOR_SECTION_ACTIVE: ThemeColor = ("#E4EFF8", "#1D3A57")
COLOR_DROPDOWN_HOVER: ThemeColor = ("#DCEBFA", "#2B4A69")
COLOR_SCROLLBAR: ThemeColor = ("#BCC9D6", "#475569")
COLOR_SCROLLBAR_HOVER: ThemeColor = ("#A9B8C7", "#64748B")
COLOR_STATUS_NEUTRAL: ThemeColor = ("#94A3B8", "#64748B")
COLOR_INFO: ThemeColor = ("#0875F5", "#60A5FA")
COLOR_INFO_SURFACE: ThemeColor = ("#EAF3FE", "#172F4D")
COLOR_SUCCESS: ThemeColor = ("#17834A", "#4ADE80")
COLOR_SUCCESS_SURFACE: ThemeColor = ("#EAF8F0", "#173629")
COLOR_READONLY: ThemeColor = ("#F1F5F9", "#202C3C")

COLOR_DANGER: ThemeColor = ("#C43D3D", "#F87171")
COLOR_DANGER_HOVER: ThemeColor = ("#FCEAEA", "#3A1D24")

# Windows color-key used only to make custom popup corners transparent.
TRANSPARENT_COLOR_KEY = "#010203"
