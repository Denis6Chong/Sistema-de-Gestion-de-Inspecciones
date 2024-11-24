from ..styles import *
import reflex as rx
from ..components.container import container


def auth_layout(*args):
    """The shared layout for the login and sign-up pages."""
    return rx.box(
        container(
            rx.vstack(
                rx.image(
            src="/logo_color.svg", 
            width="10em",  # Ajusta el tamaño del logo
            height="auto",
            margin_top="10px"
        ),
        rx.spacer(),
        rx.spacer(),
        rx.spacer(),
        rx.spacer(),
                rx.heading("¡Bienvenido!", size="8", color=accent_text_color),
                rx.heading("Inicia sesión para comenzar.", size="8", color=accent_text_color),
                align="center",
                spacing="3",
            ),
            *args,
            border_top_radius=border_radius,
            box_shadow=box_shadow_style,
            display="flex",
            flex_direction="column",
            align_items="center",
            padding_top="36px",
            padding_bottom="24px",
            spacing="4",
            background=gray_bg_color,
        ),
        height="100vh",
        padding_top="40px",
        background=gray_bg_color,
        background_repeat="no-repeat",
        background_size="cover",
    )
