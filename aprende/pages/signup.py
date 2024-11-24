import reflex as rx
from aprende.utils.auth_layout import auth_layout
from aprende.utils.auth import AuthState
from ..styles import *


def signup():
    """The sign-up page."""
    return auth_layout(
        rx.box(
            rx.vstack(
                rx.input(
                    placeholder="usuario",
                    on_blur=AuthState.set_username,
                    size="3",
                    background=gray_bg_color,
                    color=accent_text_color,
                ),
                rx.input(
                    type="password",
                    placeholder="contraseña",
                    on_blur=AuthState.set_password,
                    size="3",
                    background=gray_bg_color,
                    color=accent_text_color,
                ),
                rx.input(
                    type="password",
                    placeholder="confirmar contraseña",
                    on_blur=AuthState.set_confirm_password,
                    size="3",
                    background=gray_bg_color,
                    color=accent_text_color,
                ),
                rx.button(
                    "Registrar",
                    on_click=AuthState.signup,
                    size="3",
                    width="6em",
                    background_color=accent_color,
                    color=accent_text_color,
                    border_radius=border_radius,
                    **hover_accent_bg,
                ),
                spacing="4",
                align_items="center",
            ),
            align_items="center",
            background=gray_bg_color,
            border=accent_text_color,
            padding="16px",
            width="400px",
            border_radius=border_radius,
            box_shadow=box_shadow_style,
        ),
        rx.text(
            "¿Ya tienes una cuenta? ",
            rx.link(
                "Inicia sesión aquí.",
                href="/",
                color=accent_text_color,
                **hover_accent_color,
            ),
        ),
    )