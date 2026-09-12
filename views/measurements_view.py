import customtkinter as ctk

from services.translation_service import t
from views.placeholder_view import PlaceholderView


class MeasurementsView(PlaceholderView):
    """ML2 shell for measurement and calculated-value settings."""

    def __init__(self, master: ctk.CTk, **kwargs) -> None:
        super().__init__(
            master,
            title=t("measurements.title"),
            subtitle=t("measurements.subtitle"),
            **kwargs,
        )
