import reflex as rx
from ..templates import template
from ..model.all_model import Provincia
from ..service.provincia_service import select_all_provincia_service, select_provincia_by_nombre_service, create_provincia_service
from ..notify import notify_component
import asyncio
from ..utils.base import State
class ProvinciaState(rx.State):
    #states
    provincia:list[Provincia]
    provincia_buscar: str
    error: str = ""

    @rx.background
    async def get_all_provincia(self):
        async with self:
            self.provincia = select_all_provincia_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""


    @rx.background
    async def get_provincia_by_nombre(self):
        async with self:
            self.provincia = select_provincia_by_nombre_service(self.provincia_buscar)

    @rx.background
    async def create_provincia(self, data: dict):
        async with self:
            try:
                self.provincia = create_provincia_service(nombre=data["nombre"])
                                                        
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    def buscar_on_change(self, value: str):
        self.provincia_buscar = value
    


@template(route="/provincias", title="Provincias", on_load=ProvinciaState.get_all_provincia)
def provincia_page() -> rx.Component:
    return rx.flex(
        rx.heading("Provincias", align="center"),
            rx.hstack(
                
                create_provincia_dialogo_component(),
                justify="center",
                style={"margin-top": '30px'}
            ),
        table_provincia(ProvinciaState.provincia),
        rx.cond(
            ProvinciaState.error != "",
            notify_component(ProvinciaState.error, "shield-alert", "yellow")

        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )

def table_provincia(list_provincia: list[Provincia]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Nombre"),   
            )
        ),
    rx.table.body(
        rx.foreach(list_provincia, row_table)
        )
    )

def row_table(provincia: Provincia) -> rx.Component:
    return rx.table.row(
        rx.table.cell(provincia.nombre),
        

    )



def create_provincia_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="Nombre",
                name="nombre",
                is_required=True,
            ),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=ProvinciaState.create_provincia,
    )

def create_provincia_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Provincia")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Provincia"),
                create_provincia_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )

