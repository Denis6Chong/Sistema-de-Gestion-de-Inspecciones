import reflex as rx
import random
import datetime
from datetime import timedelta, date
import calendar
from reflex.components.radix.themes.base import (
    LiteralAccentColor,
)
from ..service.oblig_hacer_service import obtener_obligaciones_por_categoria_y_fecha_service
from ..utils.base import State

class StatsState(rx.State):
    area_toggle: bool = True
    selected_tab: str = "users"
    timeframe: str = "15 dias"
    users_data = []
    revenue_data = []
    orders_data = []
    device_data = []
    obligaciones_15_dias_data = []
    obligaciones_mes_data = []
    obligaciones_trimestre_data = []
    
    

    def toggle_areachart(self):
        self.area_toggle = not self.area_toggle

    # Define variables para cada conjunto de datos
    def set_timeframe(self, timeframe: str):
        print(f"Cambiando timeframe a: {timeframe}")
        self.timeframe = timeframe



    @rx.background
    async def load_obligaciones_15_dias_data(self):
        hoy = date.today()
        fecha_limite = hoy + timedelta(days=15)
        print(fecha_limite)
        obligaciones_data = obtener_obligaciones_por_categoria_y_fecha_service(fecha_limite)
        print(obligaciones_data)
        # Crear la lista de datos para las obligaciones
        obligaciones_data_list = []

        # Recorrer cada categoría en el diccionario de obligaciones
        for categoria, obligaciones in obligaciones_data.items():
            # Asignar color basado en la categoría
            if categoria == "Producto o Servicio":
                fill_color = "var(--blue-10)"
            elif categoria == "Higiene":
                fill_color = "var(--red-10)"
            elif categoria == "Metrologia":
                fill_color = "var(--yellow-10)"
            else:
                fill_color = "var(--default-color)"  # Color por defecto si no coincide con ninguna categoría

            # Agregar un diccionario con el nombre de la categoría, el conteo de obligaciones y el color
            obligaciones_data_list.append({
                "name": categoria,
                "value": len(obligaciones),
                "fill": fill_color   
            })
        

        async with self:
            self.obligaciones_15_dias_data = obligaciones_data_list

    # Método para cargar datos de obligaciones del mes
    @rx.background
    async def load_obligaciones_mes_data(self):
        
        hoy = date.today()

        # Obtener el último día del mes actual
        ultimo_dia_mes = calendar.monthrange(hoy.year, hoy.month)[1]

            # Crear la fecha límite como el último día del mes actual
        fecha_limite = date(hoy.year, hoy.month, ultimo_dia_mes)

        obligaciones_data = obtener_obligaciones_por_categoria_y_fecha_service(fecha_limite)

        # Crear la lista de datos para las obligaciones
        obligaciones_data_list = []

        # Recorrer cada categoría en el diccionario de obligaciones
        for categoria, obligaciones in obligaciones_data.items():
            # Asignar color basado en la categoría
            if categoria == "Producto o Servicio":
                fill_color = "var(--blue-10)"
            elif categoria == "Higiene":
                fill_color = "var(--red-10)"
            elif categoria == "Metrologia":
                fill_color = "var(--yellow-10)"
            else:
                fill_color = "var(--default-color)"  # Color por defecto si no coincide con ninguna categoría

            # Agregar un diccionario con el nombre de la categoría, el conteo de obligaciones y el color
            obligaciones_data_list.append({
                "name": categoria,
                "value": len(obligaciones),
                "fill": fill_color   
            })

        async with self:
            self.obligaciones_mes_data = obligaciones_data_list

    # Método para cargar datos de obligaciones del trimestre (90 días)
    @rx.background
    async def load_obligaciones_trimestre_data(self):
        hoy = date.today()

        # Determinar el último día del trimestre según el mes actual
        if 1 <= hoy.month <= 3:
            fecha_limite = date(hoy.year, 3, 31)  # Primer trimestre, hasta el 31 de marzo
        elif 4 <= hoy.month <= 6:
            fecha_limite = date(hoy.year, 6, 30)  # Segundo trimestre, hasta el 30 de junio
        elif 7 <= hoy.month <= 9:
            fecha_limite = date(hoy.year, 9, 30)  # Tercer trimestre, hasta el 30 de septiembre
        else:
            fecha_limite = date(hoy.year, 12, 31)  # Cuarto trimestre, hasta el 31 de diciembre


        obligaciones_data = obtener_obligaciones_por_categoria_y_fecha_service(fecha_limite)

        # Crear la lista de datos para las obligaciones
        obligaciones_data_list = []

        # Recorrer cada categoría en el diccionario de obligaciones
        for categoria, obligaciones in obligaciones_data.items():
            # Asignar color basado en la categoría
            if categoria == "Producto o Servicio":
                fill_color = "var(--blue-10)"
            elif categoria == "Higiene":
                fill_color = "var(--red-10)"
            elif categoria == "Metrologia":
                fill_color = "var(--yellow-10)"
            else:
                fill_color = "var(--default-color)"  # Color por defecto si no coincide con ninguna categoría

            # Agregar un diccionario con el nombre de la categoría, el conteo de obligaciones y el color
            obligaciones_data_list.append({
                "name": categoria,
                "value": len(obligaciones),
                "fill": fill_color   
            })

        async with self:
            self.obligaciones_trimestre_data = obligaciones_data_list

    # Método para cargar los datos de los tres periodos al mismo tiempo
    @rx.background
    async def load_all_obligaciones_data(self):
        yield StatsState.load_obligaciones_15_dias_data()
        yield StatsState.load_obligaciones_mes_data()
        yield StatsState.load_obligaciones_trimestre_data()
        yield State.check_login()
    
    

        


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


def _create_gradient(color: LiteralAccentColor, id: str) -> rx.Component:
    return (
        rx.el.svg.defs(
            rx.el.svg.linear_gradient(
                rx.el.svg.stop(
                    stop_color=rx.color(color, 7), offset="5%", stop_opacity=0.8
                ),
                rx.el.svg.stop(stop_color=rx.color(color, 7), offset="95%", stop_opacity=0),
                x1=0,
                x2=0,
                y1=0,
                y2=1,
                id=id,
            ),
        ),
    )


def _custom_tooltip(color: LiteralAccentColor) -> rx.Component:
    return (
        rx.recharts.graphing_tooltip(
            separator=" : ",
            content_style={
                "backgroundColor": rx.color("gray", 1),
                "borderRadius": "var(--radius-2)",
                "borderWidth": "1px",
                "borderColor": rx.color(color, 7),
                "padding": "0.5rem",
                "boxShadow": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
            },
            is_animation_active=True,
        ),
    )


def users_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("blue", "colorBlue"),
            _custom_tooltip("blue"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Todas",
                stroke=rx.color("blue", 9),
                fill="url(#colorBlue)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.users_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            _custom_tooltip("blue"),
            rx.recharts.bar(
                data_key="Todas",
                stroke=rx.color("blue", 9),
                fill=rx.color("blue", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.users_data,
            height=425,
        ),
    )


def revenue_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("red", "colorRed"),  # Cambiado a rojo
            _custom_tooltip("red"),  # Cambiado a rojo
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="No Conforme",  # Este key puede mantenerse
                stroke=rx.color("red", 9),  # Cambiado a rojo
                fill="url(#colorRed)",  # Cambiado a rojo
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.revenue_data,
            height=425,
            title="No Conforme",  # Título del gráfico
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("red"),  # Cambiado a rojo
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="No Conforme",  # Este key puede mantenerse
                stroke=rx.color("red", 9),  # Cambiado a rojo
                fill=rx.color("red", 7),  # Cambiado a rojo
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.revenue_data,
            height=425,
            title="No Conforme",  # Título del gráfico
        ),
    )


def orders_chart() -> rx.Component:
    return rx.cond(
        StatsState.area_toggle,
        rx.recharts.area_chart(
            _create_gradient("purple", "colorPurple"),
            _custom_tooltip("purple"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.area(
                data_key="Conforme",
                stroke=rx.color("purple", 9),
                fill="url(#colorPurple)",
                type_="monotone",
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.orders_data,
            height=425,
        ),
        rx.recharts.bar_chart(
            _custom_tooltip("purple"),
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3",
            ),
            rx.recharts.bar(
                data_key="Conforme",
                stroke=rx.color("purple", 9),
                fill=rx.color("purple", 7),
            ),
            rx.recharts.x_axis(data_key="Date", scale="auto"),
            rx.recharts.y_axis(),
            rx.recharts.legend(),
            data=StatsState.orders_data,
            height=425,
        ),
    )




# Modifica la función para obtener los datos según el periodo seleccionado
def pie_chart() -> rx.Component:
    return rx.vstack(
        rx.cond(
        StatsState.timeframe == "Mes",
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.obligaciones_mes_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        )),
        rx.cond(
            StatsState.timeframe == "15 dias",
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.obligaciones_15_dias_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        )
    ),rx.cond(
        StatsState.timeframe == "Trimestre",
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=StatsState.obligaciones_trimestre_data,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                padding_angle=1,
                inner_radius="70",
                outer_radius="100",
                label=True,
            ),
            rx.recharts.legend(),
            height=300,
        ))
    )
        

def timeframe_select() -> rx.Component:
    return rx.select(
        ["15 dias", "Mes", "Trimestre"],
        default_value="15 dias",
        value=StatsState.timeframe,
        variant="surface",
        on_change=lambda selected: StatsState.set_timeframe(selected),  # Llama a set_timeframe al cambiar
    )