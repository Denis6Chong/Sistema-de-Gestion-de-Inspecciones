import reflex as rx
from ..templates import template
from ..model.all_model import Organismo
from ..service.organismo_service import select_all_organismo_service, select_organismo_by_nombre_service, create_organismo_service
from ..notify import notify_component
import asyncio

class OrganismoState(rx.State):
    #states
    organismo:list[Organismo]
    organismo_buscar: str
    error: str = ""

    @rx.background
    async def get_all_organismo(self):
        async with self:
            self.organismo = select_all_organismo_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""


    @rx.background
    async def get_organismo_by_nombre(self):
        async with self:
            self.organismo = select_organismo_by_nombre_service(self.organismo_buscar)

    @rx.background
    async def create_organismo(self, data: dict):
        async with self:
            try:
                self.organismo = create_organismo_service(
                    id_organismo=data["id_organismo"],
                    nombre=data["nombre"],
                    siglas=data["siglas"],
                    direccion=data["direccion"],
                    telefono=data["telefono"]
                    )
                                                        
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    def buscar_on_change(self, value: str):
        self.organismo_buscar = value
    


@template(route="/organismos", title="Organismos", on_load=OrganismoState.get_all_organismo)
def organismo_page() -> rx.Component:
    return rx.flex(
        rx.hstack(
                        rx.icon("globe", size=25),
                        rx.heading(f"Organismos", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
            rx.hstack(
                
                create_organismo_dialogo_component(),
                justify="center",
                style={"margin-top": '30px'}
            ),
        table_organismo(OrganismoState.organismo),
        rx.cond(
            OrganismoState.error != "",
            notify_component(OrganismoState.error, "shield-alert", "yellow")

        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )

def table_organismo(list_organismo: list[Organismo]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("ID"),
                rx.table.column_header_cell("Nombre"),
                rx.table.column_header_cell("Siglas"),
                rx.table.column_header_cell("Direccion"),
                rx.table.column_header_cell("Telefono")   
            )
        ),
    rx.table.body(
        rx.foreach(list_organismo, row_table)
        )
    )

def row_table(organismo: Organismo) -> rx.Component:
    return rx.table.row(
        rx.table.cell(organismo.id_organismo),
        rx.table.cell(organismo.nombre),
        rx.table.cell(organismo.siglas),
        rx.table.cell(organismo.direccion),
        rx.table.cell(organismo.telefono),

    )



def create_organismo_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="ID",
                name="id_organismo"
                
            ),
            rx.input(
                placeholder="Nombre",
                name="nombre",
                is_required=True,
            ),
            rx.input(
                placeholder="Siglas",
                name="siglas"
            ),
            rx.input(
                placeholder="Direccion",
                name="direccion"
            ),
            rx.input(
                placeholder="Telefono",
                name="telefono"
            ),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=OrganismoState.create_organismo,
    )

def create_organismo_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Organismo")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Organismo"),
                create_organismo_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )

