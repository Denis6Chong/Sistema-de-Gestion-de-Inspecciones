import random
from ..templates import template
import reflex as rx
from rxconfig import config
from ..components.card import card
from ..views.stats_cards import obligaciones_stats_cards
from ..views.adquisition_view import adquisition
from ..components.notification import notification
from ..views.charts import (
    users_chart,
    revenue_chart,
    orders_chart,
    area_toggle,
    pie_chart,
    timeframe_select,
    StatsState,
)
from ..model.all_model import *
from ..service.inspeccion_service import *
from datetime import datetime, timedelta
from ..service.oblig_hacer_service import *

class State(rx.State):
    """The app state."""
    pending_obligations_count: int = 0

    def update_pending_obligations(self):
        self.pending_obligations_count = len(get_obligaciones_by_resultado_service("En Espera"))

    def on_mount(self):
        self.update_pending_obligations()

en_espera = len(get_obligaciones_by_resultado_service("En Espera"))

class MouseEnter(rx.State):
    text = "Obligaciones"

    def change_text(self):
        if self.text == "Obligaciones":
            self.text = f"{en_espera} Pendientes"
        else:
            self.text = "Obligaciones"


@template(route="/", title="Indice", on_load=StatsState.load_all_obligaciones_data) 
def index() -> rx.Component:

    # Actualiza el conteo de obligaciones pendientes
    en_espera = len(get_obligaciones_by_resultado_service("En Espera"))
    graph = StatsState
    graph.users_data = []
    graph.revenue_data = []
    graph.orders_data = []
    current_date = datetime.now()

    for i in range(12, 0, -1):  # 12 meses
        target_date = current_date - timedelta(days=(i - 1) * 30)  # Aproximadamente 30 días por mes
        year = target_date.year
        month = target_date.month
        inspecciones_count = count_inspecciones_by_month_year_service(month, year)
        graph.users_data.append(
            {
                "Date": target_date.strftime("%b %Y"),
                "Todas": inspecciones_count,
            }
        )
        
    for i in range(12, 0, -1):
        target_date = current_date - timedelta(days=(i - 1) * 30)
        year = target_date.year
        month = target_date.month
        revenue_count = count_inspecciones_with_infraccion_by_month_year_service(month, year)
        graph.revenue_data.append(
            {
                "Date": target_date.strftime("%b %Y"),
                "No Conforme": revenue_count,
            }
        )

    for i in range(12, 0, -1):
        target_date = current_date - timedelta(days=(i - 1) * 30)
        year = target_date.year
        month = target_date.month
        orders_count = count_inspecciones_without_infraccion_by_month_year_service(month, year)
        graph.orders_data.append(
            {
                "Date": target_date.strftime("%b %Y"),
                "Conforme": orders_count,
            }
        )
    
    return rx.vstack(
            rx.hstack(
                        rx.icon("info", size=25),
                        rx.heading(f"Información General", size="7"),
                        align="center",
                        spacing="2",
                    ),
            
            obligaciones_stats_cards(),

            
            card(
                rx.hstack(
                    tab_content_header(),
                    rx.segmented_control.root(
                        rx.segmented_control.item("Todas", value="users"),
                        rx.segmented_control.item("No Conforme", value="revenue"),
                        rx.segmented_control.item("Conforme", value="orders"),
                        margin_bottom="1.5em",
                        default_value="users",
                        on_change=StatsState.set_selected_tab,
                    ),
                    width="100%",
                    justify="between",
                ),
                rx.match(
                    StatsState.selected_tab,
                    ("users", users_chart()),
                    ("revenue", revenue_chart()),
                    ("orders", orders_chart()),
                ),
            ),
            rx.grid(
            card(
                rx.hstack(
                    rx.hstack(
                        rx.icon("layout-dashboard", size=20),
                        rx.text("Obligaciones Pendientes", size="4", weight="medium"),
                        align="center",
                        spacing="2",
                    ),
                    timeframe_select(),
                    align="center",
                    width="100%",
                    justify="between",
                ),
                pie_chart(),
            ),
            card(
                rx.hstack(
                    rx.icon("user-round-search", size=20),
                    rx.text("Inspectores Destacados en el Trimestre", size="4", weight="medium"),
                    align="center",
                    spacing="2",
                    margin_bottom="2.5em",
                ),
                rx.vstack(
                    adquisition(),
                ),
            ),
            gap="1rem",
            grid_template_columns=[
                "1fr",
                "repeat(1, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
                "repeat(2, 1fr)",
            ],
            width="100%",
        ),
            
        spacing="9",
        width="100%",
    )

def area_toggle() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.icon_button(
            rx.icon("area-chart"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=StatsState.toggle_areachart,
        ),
        rx.icon_button(
            rx.icon("bar-chart-3"),
            size="2",
            cursor="pointer",
            variant="surface",
            on_click=StatsState.toggle_areachart,
        ),
    )

def _time_data() -> rx.Component:
    return rx.hstack(
        rx.tooltip(
            rx.icon("activity", size=20),
            content=f"{(datetime.now() - timedelta(days=365)).strftime('%b %d, %Y')} - {datetime.now().strftime('%b %d, %Y')}",
        ),
        rx.text("Inspecciones", size="4", weight="medium"),
        align="center",
        spacing="2",
        display=["none", "none", "flex"],
    )

def tab_content_header() -> rx.Component:
    return rx.hstack(
        _time_data(),
        area_toggle(),
        align="center",
        width="100%",
        spacing="4",
    )