import os
import sys
from pathlib import Path

try:
    import customtkinter as ctk
except ModuleNotFoundError:
    project_root = Path(__file__).resolve().parent
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = project_root / ".venv" / "bin" / "python"
    if venv_python.exists():
        print("Re-launching with the project virtual environment...")
        os.execv(str(venv_python), [str(venv_python), str(Path(__file__))])
    raise

from utils.theme import APP_APPEARANCE_MODE, APP_COLOR_THEME, COLOR_BACKGROUND
from services.translation_service import t, translate_page_title
from views.communications_view import CommunicationsView
from views.general_view import GeneralView
from views.measurements_view import MeasurementsView
from views.placeholder_view import PlaceholderView
from views.settings_view import SettingsView
from widgets.sidebar import Sidebar


def get_minimum_window_size(
    screen_width: int | None = None, screen_height: int | None = None
) -> tuple[int, int]:
    """Return a DPI-safe minimum size in CustomTkinter logical pixels."""
    width = max(1, screen_width or 1536)
    height = max(1, screen_height or 864)
    minimum_width = max(760, min(1200, int(width * 0.75)))
    minimum_height = max(400, min(720, int(height * 0.75)))
    return minimum_width, minimum_height


def get_initial_window_geometry(
    screen_width: int | None = None, screen_height: int | None = None
) -> str:
    """Return a window size that scales comfortably across common desktop resolutions."""
    width = max(1, screen_width or 1536)
    height = max(1, screen_height or 864)
    minimum_width, minimum_height = get_minimum_window_size(width, height)
    target_width = max(minimum_width, min(1500, int(width * 0.82)))
    target_height = max(minimum_height, min(980, int(height * 0.82)))
    return f"{target_width}x{target_height}"


class IndustrialDeviceConfiguratorApp(ctk.CTk):
    """Main application window for the device configurator."""

    def __init__(self) -> None:
        super().__init__()

        self.title(t("app.title"))
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(get_initial_window_geometry(screen_width, screen_height))
        self.minsize(*get_minimum_window_size(screen_width, screen_height))
        self.configure(fg_color=COLOR_BACKGROUND)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar = Sidebar(self, on_page_selected=self.show_page)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.content_area = ctk.CTkFrame(
            self,
            fg_color=COLOR_BACKGROUND,
            corner_radius=0,
        )
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        self.pages: dict[str, ctk.CTkFrame] = {}
        self.current_page: ctk.CTkFrame | None = None
        self.show_page("Settings")

    def show_page(self, page_name: str) -> None:
        """Show a page by name, creating it the first time it is requested."""
        if self.current_page is not None:
            self.current_page.grid_remove()

        if page_name not in self.pages:
            page_types = {
                "General": GeneralView,
                "Measurements": MeasurementsView,
                "Communications": CommunicationsView,
                "Settings": SettingsView,
            }
            page_type = page_types.get(page_name)
            if page_type is not None:
                page = page_type(self.content_area)
            else:
                page = PlaceholderView(
                    self.content_area,
                    title=translate_page_title(page_name),
                )

            page.grid(row=0, column=0, sticky="nsew")
            self.pages[page_name] = page

        self.current_page = self.pages[page_name]
        self._sync_theme_controls()
        self.current_page.grid()
        self.sidebar.set_active(page_name)

    def _set_appearance_mode(self, mode_string: str) -> None:
        super()._set_appearance_mode(mode_string)
        self._sync_theme_controls()

    def _sync_theme_controls(self) -> None:
        """Keep cached and newly opened pages consistent with the app theme."""
        mode = ctk.get_appearance_mode()
        for name, page in getattr(self, "pages", {}).items():
            if isinstance(page, SettingsView):
                page.controls["header_theme"].set(mode)
                page.controls["theme"].set(mode)
                page._sync_summary()
            elif name in {"General", "Measurements", "Communications"}:
                page.theme_menu.set(t(f"{name.lower()}.theme.{mode.lower()}"))


def main() -> None:
    ctk.set_appearance_mode(APP_APPEARANCE_MODE)
    ctk.set_default_color_theme(APP_COLOR_THEME)

    app = IndustrialDeviceConfiguratorApp()
    print("Power Monitor started successfully")
    app.mainloop()


if __name__ == "__main__":
    main()
