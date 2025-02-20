import reflex as rx
from ..styles import *


def container(*children, **props):
    """A fixed container based on a 960px grid."""
    # Enable override of default props.
    props = (
        dict(
            width="100%",
            max_width="960px",
            background="white",
            height="100%",
            px="9",
            margin="0 auto",
            position="relative",
            border_radius=border_radius,
            box_shadow=box_shadow_style,
        )
        | props
    )
    return rx.stack(*children, **props)
