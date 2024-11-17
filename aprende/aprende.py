"""Welcome to Reflex!."""

# Import all the pages.
from .pages import *
from . import styles

import reflex as rx
from .pages.index import index
from .pages.login import login
from .pages.signup import signup
from .utils.base import State



# Create the app.
app = rx.App(
    style=styles.base_style,
    stylesheets=styles.base_stylesheets,
    title="Sistema de Inspecciones",
    description="Gestiona Inspecciones",
)
app.add_page(login)
app.add_page(signup)
app.add_page(index, route="/", on_load=State.check_login())