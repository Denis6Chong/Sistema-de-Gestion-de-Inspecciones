import reflex as rx
from reflex.components.radix.themes.base import LiteralAccentColor
from ..service.inspector_service import select_top_inspectores_service_handler, cant_inspecciones_inspector_service

# Obtener los 5 mejores inspectores
mejores_inspectores = select_top_inspectores_service_handler(5)

# Definir el máximo de la barra en 50 inspecciones
MAX_INSPECCIONES = 50

def item(
    nombre_inspector: str, codigo_inspector: str, cantidad_inspecciones: int, color: LiteralAccentColor
) -> rx.Component:
    # Calcular el progreso basado en un máximo de 50 inspecciones
    progress = min(cantidad_inspecciones, MAX_INSPECCIONES)
    
    return (
        rx.hstack(
            rx.hstack(
                # Mostrar el nombre del inspector
                rx.text(
                    nombre_inspector,
                    size="3",
                    weight="medium",
                    display=["none", "none", "none", "none", "flex"],
                ),
                width=["10%", "10%", "10%", "10%", "25%"],
                align="center",
                spacing="3",
            ),
            rx.flex(
                rx.text(
                    f"{cantidad_inspecciones}",  # Mostrar cantidad exacta de inspecciones
                    position="absolute",
                    top="50%",
                    left=["90%", "90%", "90%", "90%", "95%"],
                    transform="translate(-50%, -50%)",
                    size="1",
                ),
                rx.progress(
                    value=progress,  # El valor es la cantidad de inspecciones, ajustado a un máximo de 50
                    max=MAX_INSPECCIONES,  # El máximo de la barra es 50
                    height="19px",
                    color_scheme=color,
                    width="100%",
                ),
                position="relative",
                width="100%",
            ),
            width="100%",
            border_radius="10px",
            align="center",
            justify="between",
        ),
    )


def adquisition() -> rx.Component:
    # Lista de colores para los inspectores
    colores = ["blue", "crimson", "plum", "green", "amber"]

    # Crear una lista de componentes basados en los mejores inspectores
    items = [
        item(
            inspector.nombre,  # Acceder al nombre del inspector
            inspector.codigo_inspector,  # Acceder al código del inspector
            int(total_inspecciones),  # Acceder al total de inspecciones
            color  # Asignar un color distinto a cada inspector
        )
        for (inspector, total_inspecciones), color in zip(select_top_inspectores_service_handler(5), colores)
    ]

    return rx.vstack(
        *items,  # Mostrar todos los inspectores
        width="100%",
        spacing="6",
    )