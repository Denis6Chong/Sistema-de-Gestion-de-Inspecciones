"""The settings page."""
from ..styles import *
from ..templates import template
from ..utils.base import State
import reflex as rx
from ..views.color_picker import primary_color_picker, secondary_color_picker
from ..views.radius_picker import radius_picker
from ..views.scaling_picker import scaling_picker


@template(route="/configuracion", title="Configuración", on_load=State.check_login())
def settings() -> rx.Component:
    """The settings page.

    Returns:
        The UI for the settings page.
    """
    return rx.vstack(
        rx.hstack(
                        rx.icon("settings", size=25),
                        rx.heading(f"Configuración", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
        # Primary color picker
        rx.vstack(
            rx.hstack(
                rx.icon("palette", color=rx.color("accent", 10)),
                rx.heading("Color Primario", size="6"),
                align="center",
            ),
            primary_color_picker(),
            spacing="4",
            width="100%",
        ),
        # Secondary color picker
        rx.vstack(
            rx.hstack(
                rx.icon("blend", color=rx.color("gray", 11)),
                rx.heading("Color Secundario", size="6"),
                align="center",
            ),
            secondary_color_picker(),
            spacing="4",
            width="100%",
        ),
        # Radius picker
        radius_picker(),
        # Scaling picker
        scaling_picker(),
        rx.vstack(
            rx.hstack(
                rx.icon("user", color=rx.color("gray", 11)),
                rx.heading("Registrar Usuario", size="6"),
                align="center",
            ),
            rx.button(
            "Ir a Registro",
            on_click=rx.redirect("/signup"),  # Redirect to the signup page
            size="3",
            width="10em",
            background_color=accent_color,
            color=accent_text_color,
            border_radius=border_radius,
            **hover_accent_bg,
        )
    ),  
        spacing="7",
        width="100%",
    )
