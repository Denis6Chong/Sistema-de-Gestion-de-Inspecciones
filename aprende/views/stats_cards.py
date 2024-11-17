import reflex as rx
from .. import styles
from reflex.components.radix.themes.base import LiteralAccentColor
from datetime import datetime
from ..service.oblig_hacer_service import cant_obligaciones_no_cumplidas,cant_obligaciones_en_espera, cant_obligaciones_falta_datos

# Función para la tarjeta de estadísticas de obligaciones
def obligaciones_stats_card(
    stat_name: str,
    value: int,
    prev_value: int,
    icon: str,
    icon_color: LiteralAccentColor,
    extra_char: str = "",
    respecto: str = "",
) -> rx.Component:
    percentage_change = (
        round(((value - prev_value) / prev_value) * 100, 2)
        if prev_value != 0
        else 0 if value == 0 else float("inf")
    )
    change = "aumentó" if value > prev_value else "disminuyó"
    arrow_icon = "trending-up" if value > prev_value else "trending-down"
    arrow_color = "grass" if value > prev_value else "tomato"
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(tag=icon, size=34),
                    color_scheme=icon_color,
                    radius="full",
                    padding="0.7rem",
                ),
                rx.vstack(
                    rx.heading(
                        f"{extra_char}{value:,}",
                        size="6",
                        weight="bold",
                    ),
                    rx.text(stat_name, size="4", weight="medium"),
                    spacing="1",
                    height="100%",
                    align_items="start",
                    width="100%",
                ),
                height="100%",
                spacing="4",
                align="center",
                width="100%",
            ),
            rx.hstack(
                rx.hstack(
                    rx.icon(
                        tag=arrow_icon,
                        size=24,
                        color=rx.color(arrow_color, 9),
                    ),
                    rx.text(
                        f"{percentage_change}%",
                        size="3",
                        color=rx.color(arrow_color, 9),
                        weight="medium",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.text(
                    f"{change} {respecto}",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                align="center",
                width="100%",
            ),
            spacing="3",
        ),
        size="3",
        width="100%",
        box_shadow=styles.box_shadow_style,
    )

# Función para generar las tarjetas de estadísticas de obligaciones
def obligaciones_stats_cards() -> rx.Component:
    return rx.grid(
        obligaciones_stats_card(
            stat_name="En Espera",
            value=cant_obligaciones_en_espera(),  # Mes actual
            prev_value=cant_obligaciones_en_espera(anterior=True),
            icon="loader",
            icon_color="yellow",
            respecto="respecto al mes anterior",
        ),
        obligaciones_stats_cards_sin_por_ciento(
            stat_name="Datos Incompletos",
            value=cant_obligaciones_falta_datos(),  # Último trimestre
            icon="triangle_alert",
            icon_color="orange"
        ),
        obligaciones_stats_card(
            stat_name="No Cumplidas",
            value=cant_obligaciones_no_cumplidas(), 
            prev_value=cant_obligaciones_no_cumplidas(anterior=True),
            icon="ban",
            icon_color="tomato",
            respecto="respecto al trimestre anterior"
        ),
        gap="1rem",
        grid_template_columns=[
            "1fr",
            "repeat(1, 1fr)",
            "repeat(2, 1fr)",
            "repeat(3, 1fr)", 
            "repeat(3, 1fr)",
        ],
        width="100%",
    )

def obligaciones_stats_cards_sin_por_ciento(
    stat_name: str,
    value: int,
    icon: str,
    icon_color: LiteralAccentColor,
    extra_char: str = "",
) -> rx.Component:
    
    
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(
                    rx.icon(tag=icon, size=34),
                    color_scheme=icon_color,
                    radius="full",
                    padding="0.7rem",
                ),
                rx.vstack(
                    rx.heading(
                        f"{extra_char}{value:,}",
                        size="6",
                        weight="bold",
                    ),
                    rx.text(stat_name, size="4", weight="medium"),
                    spacing="1",
                    height="100%",
                    align_items="start",
                    width="100%",
                ),
                height="100%",
                spacing="4",
                align="center",
                width="100%",
            ),
            spacing="3",
        ),
        size="3",
        width="100%",
        box_shadow=styles.box_shadow_style,
    )