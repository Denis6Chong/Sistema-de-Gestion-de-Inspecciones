import reflex as rx
from ..templates import template
from ..model.all_model import Municipio
from ..service.municipio_service import select_all_municipio_service, select_municipio_by_nombre_service, create_municipio_service
from ..notify import notify_component
import asyncio

class MunicipioState(rx.State):
    #states
    municipio:list[Municipio]
    municipio_buscar: str
    error: str = ""

    @rx.background
    async def get_all_municipio(self):
        async with self:
            self.municipio = select_all_municipio_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""


    @rx.background
    async def get_municipio_by_nombre(self):
        async with self:
            self.municipio = select_municipio_by_nombre_service(self.municipio_buscar)

    @rx.background
    async def create_municipio(self, data: dict):
        async with self:
            try:
                self.municipio = create_municipio_service(nombre=data["nombre"],
                                                        nombre_provincia=data["nombre_provincia"])
                                                        
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    def buscar_on_change(self, value: str):
        self.municipio_buscar = value
    


@template(route="/municipios", title="Municipios", on_load=MunicipioState.get_all_municipio)
def municipio_page() -> rx.Component:
    return rx.flex(
        rx.heading("Municipios", align="center"),
            rx.hstack(
                
                create_municipio_dialogo_component(),
                justify="center",
                style={"margin-top": '30px'}
            ),
        table_municipio(MunicipioState.municipio),
        rx.cond(
            MunicipioState.error != "",
            notify_component(MunicipioState.error, "shield-alert", "yellow")

        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )

def table_municipio(list_municipio: list[Municipio]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Nombre"),  
                rx.table.column_header_cell("Provincia"),
            )
        ),
    rx.table.body(
        rx.foreach(list_municipio, row_table)
        )
    )

def row_table(municipio: Municipio) -> rx.Component:
    return rx.table.row(
        rx.table.cell(municipio.nombre),
        rx.table.cell(municipio.nombre_provincia),
        

    )



def create_municipio_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="Nombre",
                name="nombre",
                is_required=True,
            ),
            rx.input(
                placeholder="Provincia",
                name="nombre_provincia",
                is_required=True,
            ),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=MunicipioState.create_municipio,
    )

def create_municipio_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Municipio")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Municipio"),
                create_municipio_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )

