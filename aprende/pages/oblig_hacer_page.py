import reflex as rx
from ..templates import template
from ..utils.for_table import header_cell
from ..utils.datos import ResultadoEnum, TipoObligacionEnum
from ..components.status_badge import status_badge
from ..utils.base import State

from ..model.all_model import Oblig_Hacer
from ..service.norma_service import select_all_normas_service
from ..service.oblig_hacer_service import *
from ..notify import notify_component
import asyncio
from datetime import date

class Oblig_HacerState(rx.State):
    # States
    tiempo: int
    oblig_hacer: list[Oblig_Hacer]
    oblig_hacer_buscar: str
    error: str = ""
    tipo: str = ""
    selected_filter: str = ""
    id_inspeccion: int = 0
    selected_month: int
    selected_year: int
    selected_tipo_fecha: str
    codigo_norma_list: list [str]
    
    def on_filter_change(self, value: str):
        self.selected_filter = value

    def on_month_change(self, value: str):
        self.selected_month = int(value)

    
    def on_year_change(self, value: str):
    
        self.selected_year = int(value)

    def on_tipo_fecha_change(self, value: str):
        self.selected_tipo_fecha = value

    @rx.background
    async def get_all_oblig_hacer(self):
        async with self:
            obligaciones = select_all_oblig_hacer_service()
        
        
            if obligaciones:
                self.oblig_hacer = [
                    {
                    "codigo_obligacion": obligacion.codigo_obligacion,
                    "id_inspeccion": obligacion.id_inspeccion,
                    "tipo_obligacion": obligacion.tipo_obligacion,
                    "fecha_inicio": obligacion.fecha_inicio,
                    "fecha_venc": obligacion.fecha_venc,
                    "fecha_comp": obligacion.fecha_comp,
                    "tiempo": (obligacion.fecha_venc - date.today()).days if obligacion.fecha_venc else None,
                    "resultado": obligacion.resultado,
                    "multa": obligacion.multa,
                    "codigo_norma": obligacion.codigo_norma,
                    }
                    for obligacion in obligaciones
                ]
            else:
            # Opcional: inicializar con una lista vacía si no hay resultados
                self.oblig_hacer = []
    @rx.background
    async def load_codigo_norma_lista(self):
        normas = select_all_normas_service()
        lista = []
        for norma in normas:
            codigo = norma.codigo_norma
            lista.append(str(codigo))

        # Modificar el estado dentro de un bloque 'async with self'
        async with self:
            self.codigo_norma_list = lista
    @rx.background
    async def load_all_data(self):
        # Cargar inspectores, establecimientos e inspecciones al iniciar la página
        yield State.check_login()
        yield Oblig_HacerState.load_codigo_norma_lista()
        yield Oblig_HacerState.get_all_oblig_hacer()
        

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""

    async def get_obligaciones_by_month(self):
        try:
            self.oblig_hacer = select_obligaciones_by_month_service(self.selected_tipo_fecha, self.selected_month, self.selected_year)
        except BaseException as be:
            print(be.args)
            self.error = be.args

    @rx.background
    async def get_oblig_hacer_by_resultado(self):
        async with self:
            self.oblig_hacer = get_obligaciones_by_resultado_service(self.oblig_hacer_buscar)
    
    
    @rx.background
    async def get_oblig_hacer_by_tipo(self):
        async with self:
            self.oblig_hacer = get_obligaciones_by_tipo(self.tipo)
    
    @rx.background
    async def get_oblig_hacer_by_datos_incompletos(self):
        async with self:
            self.oblig_hacer = obligaciones_falta_datos()
    
    @rx.background
    async def get_oblig_hacer_by_id(self):
        async with self:
            self.oblig_hacer = get_obligaciones_by_inspeccion_service(self.id_inspeccion)
    @rx.background
    async def update_oblig_hacer(self, data: dict):
        async with self:
            try:
                
                self.oblig_hacer = update_obligacion_service(
                    codigo_obligacion=data["codigo_obligacion"],
                    fecha_venc=data["fecha_venc"],
                    fecha_comp=data["fecha_comp"],
                    resultado=data["resultado"],
                    multa=data["multa"],
                    codigo_norma=data["codigo_norma"],
                )
            except BaseException as be:
                print(be.args)
                self.error = be.args
        await self.handleNotify()

    def buscar_on_change(self, value: str):
        self.oblig_hacer_buscar = value

    def buscar_id_on_change(self, value: int):
        try:
            self.id_inspeccion = int(value)
        except ValueError:
            self.error = "Por favor ingrese un ID válido."
    
    def buscar_tipo_on_change(self, value: str):
        self.tipo = value
            


    
@template(route="/obligaciones", title="Obligaciones", on_load=Oblig_HacerState.load_all_data)
def oblig_hacer_page() -> rx.Component:
    
    return rx.flex(
        rx.hstack(
                        rx.icon("shield", size=25),
                        rx.heading(f"Obligaciones de Hacer", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
        rx.hstack(
            filtro_general_component(),
            justify="center",
            style={"margin-top": '30px'}
        ),
        table_oblig_hacer(Oblig_HacerState.oblig_hacer),
        rx.cond(
            Oblig_HacerState.error != "",
            notify_component(Oblig_HacerState.error, "shield-alert", "yellow")
        ),
        direction="column",
        style={"width": "auto", "margin": "auto"}
    )

def table_oblig_hacer(list_oblig_hacer: list[Oblig_Hacer]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                header_cell("ID_Inspeccion","hash"),
                header_cell("Código","code"),
                header_cell("Tipo", "boxes"),
                header_cell("Inicio", "calendar"),
                header_cell("Vencimiento","calendar-clock"),
                header_cell("Comprobacion", "calendar-check-2"),
                header_cell("Tiempo","clock"),
                header_cell("Resultado", "orbit"),
                header_cell("Multa", "dollar-sign"),
                header_cell("Norma_Incumplida", "book-open" ),
                header_cell("Acción", "cog")
            )
        ),
        rx.table.body(
            rx.foreach(list_oblig_hacer, lambda obligacion, index=None: row_table(obligacion, index))
        )
        )

    

def row_table(oblig_hacer: Oblig_Hacer, index: int) -> rx.Component:
    bg_color = rx.cond(
    index % 2 == 0,
    rx.color("gray", 1),
    rx.color("accent", 2),)
    
    hover_color = rx.cond(
    index % 2 == 0,
    rx.color("gray", 3),
    rx.color("accent", 3),
    )
    
    return rx.table.row(
        rx.table.cell(
            oblig_hacer.id_inspeccion, align="center"),
        rx.table.cell(oblig_hacer.codigo_obligacion, align="center"),
        rx.table.cell(oblig_hacer.tipo_obligacion, align="center"),
        rx.table.cell(oblig_hacer.fecha_inicio, align="center"),
        rx.cond(
                oblig_hacer.fecha_venc,
                rx.table.cell(oblig_hacer.fecha_venc, align="center",),
                rx.table.cell("-", align="center"),
                ),
        rx.cond(
                oblig_hacer.fecha_comp,
                rx.table.cell(oblig_hacer.fecha_comp, align="center",),
                rx.table.cell("-", align="center"),
                ),
        rx.cond(
                oblig_hacer.fecha_venc,
                rx.table.cell(oblig_hacer.tiempo, align="center",),
                rx.table.cell("-", align="center"),
                ),
        rx.table.cell(status_badge(oblig_hacer.resultado)),
        rx.table.cell(rx.cond(
            oblig_hacer.multa is not None,
            
            rx.badge(
                f"$ {oblig_hacer.multa}",
                color_scheme="red",
                align="center"
            )
            ),align="center"),
            rx.cond(
                oblig_hacer.codigo_norma,
                rx.table.cell(oblig_hacer.codigo_norma, align="center",),
                rx.table.cell("N/A", align="center"),
                ),
        rx.table.cell(
            rx.hstack(
                update_oblig_hacer_dialog_component(oblig_hacer),
            ),align="center",
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center" 

    )



def update_oblig_hacer_form(oblig_hacer: Oblig_Hacer) -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Codigo", name="codigo_obligacion", value=oblig_hacer.codigo_obligacion, read_only=True),
            rx.input(placeholder="Fecha Vencimiento", name="fecha_venc", type="date", default_value=f"{oblig_hacer.fecha_venc}"),
            rx.input(placeholder="Fecha Comprobacion", name="fecha_comp", type="date", default_value=f"{oblig_hacer.fecha_comp}"),
            rx.select(
                    [ResultadoEnum.CUMPLIDA, ResultadoEnum.EN_ESPERA, ResultadoEnum.NO_CUMPLIDA], name="resultado",
                            default_value=f"{oblig_hacer.resultado}"
                ),
            rx.input(placeholder="Multa", name="multa", type="float", default_value=f"{oblig_hacer.multa}"),    
            rx.select(Oblig_HacerState.codigo_norma_list, name="codigo_norma", default_value=f"{oblig_hacer.codigo_norma}"),
            rx.dialog.close(rx.button("Guardar", type="submit"))
        ),
        on_submit=Oblig_HacerState.update_oblig_hacer,
    )

def update_oblig_hacer_dialog_component(oblig_hacer: Oblig_Hacer) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.flex(
    rx.icon("square-mouse-pointer"),
    
    gap="2",
))),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title(f"Editar Obligación {oblig_hacer.codigo_obligacion}"),
                update_oblig_hacer_form(oblig_hacer),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )






def filtro_general_component() -> rx.Component:
    return rx.hstack(
        rx.select(
                [("Seleccionar Filtro"),
                ("Resultado"),
                ("Tipo"),
                ("Mes y Año"),
                ("ID Inspeccion"),
                ("Datos Incompletos")
                
                
            ],
            placeholder="Seleccionar Filtro",
            on_change=Oblig_HacerState.on_filter_change
        ),
        rx.cond(
            Oblig_HacerState.selected_filter == "Resultado",
            buscar_oblig_hacer_component()
        ),
        rx.cond(
            Oblig_HacerState.selected_filter == "Tipo",
            filtro_tipo_obligacion_hacer()
        ),
        rx.cond(
            Oblig_HacerState.selected_filter == "Mes y Año",
            filtro_mes_ano_component()
        ),
        rx.cond(
            Oblig_HacerState.selected_filter == "ID Inspeccion",
            filtro_id_inspeccion_component()
        ),
        rx.cond(
            Oblig_HacerState.selected_filter == "Datos Incompletos",
            filtro_datos_incompletos_component()
        ),
        rx.icon("filter", size=20),
    )


def filtro_id_inspeccion_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ingrese ID", type="int", on_change=Oblig_HacerState.buscar_id_on_change),
        rx.button("Buscar Obligación", on_click=Oblig_HacerState.get_oblig_hacer_by_id)
    )



def filtro_datos_incompletos_component() -> rx.Component:
    return rx.button("Aplicar Filtro", on_click=Oblig_HacerState.get_oblig_hacer_by_datos_incompletos) 
    

current_year = datetime.now().year

# Generar las opciones de años en formato de tupla (texto, valor)
years = [(f"{current_year - i}") for i in range(20)]


def filtro_mes_ano_component() -> rx.Component:
    return rx.hstack(
        rx.select(["Fecha Inicio", "Fecha Vencimiento", "Fecha Comprobación"],
                placeholder="Seleccione Tipo de Fecha",
                on_change=Oblig_HacerState.on_tipo_fecha_change,

        ),
        rx.select(
                    [("1"), ("2"), ("3"), ("4"), ("5"), 
                    ("6"), ("7"), ("8"), ("9"), 
                    ("10"), ("11"), ("12")],
            placeholder="Seleccione Mes",
            on_change=Oblig_HacerState.on_month_change,
                ),
        rx.select(years,
            placeholder="Seleccione Año",
            on_change=Oblig_HacerState.on_year_change,
        ),
        rx.button("Filtrar", on_click=Oblig_HacerState.get_obligaciones_by_month)
    )

def buscar_oblig_hacer_component() -> rx.Component:
    return rx.hstack(
        rx.select(["Cumplida", "En Espera", "No Cumplida"],placeholder="Filtrar por Resultado", on_change=Oblig_HacerState.buscar_on_change),
        rx.button("Filtrar", on_click=Oblig_HacerState.get_oblig_hacer_by_resultado)
    )

def filtro_tipo_obligacion_hacer() -> rx.Component:
    return rx.hstack(
        rx.select(["Producto o Servicio", "Higiene", "Metrologia"],placeholder="Filtrar por Tipo", on_change=Oblig_HacerState.buscar_tipo_on_change),
        rx.button("Filtrar", on_click=Oblig_HacerState.get_oblig_hacer_by_tipo)
    )