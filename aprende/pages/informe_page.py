import reflex as rx
from ..utils.for_table import header_cell
from ..templates import template
from ..model.all_model import Informe, Organismo
from ..service.organismo_service import select_all_organismo_service
from ..service.informe_service import *
from ..notify import notify_component
from ..utils.base import State
import asyncio

class InformeState(rx.State):
    #states
    informe:list[Informe]
    informe_buscar: str
    error: str = ""
    selected_month: int
    selected_year: int



    @rx.background
    async def load_all_data(self):
        
        yield InformeState.get_all_informe()
        yield State.check_login()
    

    @rx.background
    async def get_all_informe(self):
        async with self:
            self.informe = select_all_informes_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""

    async def get_informe_by_month(self):
        try:
            self.informe = select_informe_by_month_service(self.selected_month, self.selected_year)
        except BaseException as be:
            print(be.args)
            self.error = be.args
    
    def on_month_change(self, value: str):
        self.selected_month = int(value)

    def on_year_change(self, value: int):
        self.selected_year = int(value)        

    def buscar_on_change(self, value: str):
        self.informe_buscar = value
    @rx.background
    async def get_informe_by_nombre(self):
        async with self:
            self.informe = select_informe_by_titulo_service(self.informe_buscar)

    @rx.background
    async def create_informe(self, data: dict):
        async with self:
            try:
            

                self.informe = create_informe_service(
                    id_informe="",
                    titulo=data["titulo"],
                    fecha=data["fecha"],
                    conclusiones=data["conclusiones"]

                    )
                                                        
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    
    
    @rx.background
    async def update_informe(self, data: dict):
        print("Datos enviados para actualizar: ", data)
        async with self:
            try:
                
                
                self.informe = update_informe_service(
                    id_informe=data["id_informe"],
                    titulo=data["titulo"],
                    fecha=data["fecha"],
                    conclusiones=data["conclusiones"],
                

                    )
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()


    @rx.background
    async def delete_informe_by_id(self, id_informe):
        async with self:
            self.informe = delete_informe_service(id_informe)



@template(route="/informes", title="Informes", on_load=InformeState.load_all_data)
def informe_page() -> rx.Component:
    return rx.flex(
        rx.hstack(
                        rx.icon("circle-dot", size=25),
                        rx.heading(f"Informes", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
            rx.hstack(
                buscar_informe_component(),
                create_informe_dialogo_component(),
                filtro_mes_ano_component(),
                justify="center",
                style={"margin-top": '30px'}
            ),
        table_informe(InformeState.informe),
        rx.cond(
            InformeState.error != "",
            notify_component(InformeState.error, "shield-alert", "yellow")

        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )

def table_informe(list_informe: list[Informe]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                header_cell("ID", "hash"),
                header_cell("Título","case-upper"),
                header_cell("Inicio", "calendar"),
                header_cell("Conclusiones", "calendar"), 
                
                header_cell("Acción", "cog")
            )
        ),
    rx.table.body(
        rx.foreach(list_informe, lambda informe, index=None: row_table(informe, index))
        )
    )

def row_table(informe: Informe, index: int) -> rx.Component:
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
        rx.table.cell(informe.id_informe),
        rx.table.cell(informe.titulo ),
        rx.table.cell(informe.fecha),
        rx.table.cell(informe.conclusiones),

        
        rx.table.cell(
            rx.hstack(
                update_informe_dialog_component(informe),
                delete_informe_dialog_component(informe.id_informe),
                
            ), align="center"
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center")





def create_informe_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="Título",
                name="titulo",
                is_required=True,
            ),
            rx.input(placeholder="Fecha Inicio", name="fecha", type="date"),
            rx.input(placeholder="Conclusiones", name="conclusiones", type="date"),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=InformeState.create_informe,
    )

def create_informe_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Informe")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Informe"),
                create_informe_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )

def delete_informe_dialog_component(id: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash_2"))),
        rx.dialog.content(
            rx.dialog.title("Eliminar Informe"),
            rx.dialog.description("Esta seguro de querer eliminar el informe " + str(id)),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        'Cancelar',
                        color_scheme="crimson",
                        variant="soft"
                    ),
                ),
                rx.dialog.close(
                    rx.button("Confirmar", on_click=InformeState.delete_informe_by_id(id)),
                ),
                spacing="3",
                marging_top="16px",
                justify="end"
            )
        )
    )

def update_informe_dialog_component(informe: Informe) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.flex(
    rx.icon("square-mouse-pointer"),
    
    gap="2",
))),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title(f"Editar Informe {informe.id_informe}"),
                update_informe_form(informe),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"} 
        ),
    )
def buscar_informe_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ingrese Titulo", on_change=InformeState.buscar_on_change),
        rx.button("Buscar Informe", on_click=InformeState.get_informe_by_nombre)
    )

def update_informe_form(informe: Informe) -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="ID",
                name="id_informe",
                value=informe.id_informe
                
            ),
            rx.input(
                placeholder="Establecimiento(s)", 
                name="titulo",
                default_value=informe.titulo,
                is_required=True,
            ),
            rx.input(placeholder="Fecha Inicio", name="fecha", type="date", default_value=f"{informe.fecha}"),
            rx.input(placeholder="Conclusiones", name="conclusiones", type="date", default_value=f"{informe.conclusiones}"),

            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=InformeState.update_informe,
    )

def filtro_mes_ano_component() -> rx.Component:
    return rx.hstack(
        rx.select(
                    [("1"), ("2"), ("3"), ("4"), ("5"), 
                    ("6"), ("7"), ("8"), ("9"), 
                    ("10"), ("11"), ("12")],
            placeholder="Seleccione Mes",
            on_change=InformeState.on_month_change,
                ),
        rx.input(
            placeholder="Ingrese Año",
            on_change=InformeState.on_year_change,
            type="number",
            min=2000,  # Ajustar según la necesidad
            max=2100,
        ),
        rx.button("Filtrar", on_click=InformeState.get_informe_by_month)
    )


    

