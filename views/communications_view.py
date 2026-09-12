import customtkinter as ctk

from services.translation_service import t
from views.placeholder_view import PlaceholderView


class CommunicationsView(PlaceholderView):
    """ML2 shell for communication interface and network settings."""

    def __init__(self, master: ctk.CTk, **kwargs) -> None:
        super().__init__(
            master,
            title=t("communications.title"),
            subtitle=t("communications.subtitle"),
            **kwargs,
        )
