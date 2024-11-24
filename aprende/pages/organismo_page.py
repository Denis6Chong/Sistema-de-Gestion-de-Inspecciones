import reflex as rx
from ..utils.for_table import header_cell
from ..templates import template
from ..model.all_model import Organismo
from ..service.organismo_service import delete_organismo_service, update_organismo_service, select_all_organismo_service, select_organismo_by_nombre_service, create_organismo_service
from ..notify import notify_component
import asyncio
from ..utils.base import State
class OrganismoState(rx.State):
    #states
    organismo:list[Organismo]
    organismo_buscar: str
    error: str = ""

    @rx.background
    async def get_all_organismo(self):
        yield State.check_login()
        async with self:
            self.organismo = select_all_organismo_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""

    @rx.background
    async def delete_organismo_by_id(self, id_organismo):
        async with self:
            self.organismo = delete_organismo_service(id_organismo)

    @rx.background
    async def get_organismo_by_nombre(self):
        async with self:
            self.organismo = select_organismo_by_nombre_service(self.organismo_buscar)

    @rx.background
    async def create_organismo(self, data: dict):
        async with self:
            try:
                self.organismo = create_organismo_service(
                    id_organismo="",
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
    
    @rx.background
    async def update_organismo(self, data: dict):
        print("Datos enviados para actualizar: ", data)
        async with self:
            try:
                
                self.organismo = update_organismo_service(
                    id_organismo=data["id_organismo"],
                    nombre=data["nombre"],
                    siglas=data["siglas"],
                    direccion=data["direccion"],
                    telefono=["telefono"],

                    )
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()


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
                buscar_organismo_component(),
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
                header_cell("ID","hash"),
                header_cell("Nombre","case-sensitive"),
                header_cell("Siglas","case-upper"),
                header_cell("Direccion","map-pin"),
                header_cell("Telefono","smartphone"),
                header_cell("Acción", "cog")   
            )
        ),
    rx.table.body(
        rx.foreach(list_organismo, lambda organismo, index=None: row_table(organismo, index))
        )
    )

def row_table(organismo: Organismo, index) -> rx.Component:
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
        rx.table.cell(organismo.id_organismo),
        rx.table.cell(organismo.nombre),
        rx.table.cell(organismo.siglas),
        rx.table.cell(organismo.direccion),
        rx.table.cell(organismo.telefono),
        rx.table.cell(
            rx.hstack(
                update_organismo_dialog_component(organismo),
                delete_organismo_dialog_component(organismo.id_organismo),
                
            ), align="center"
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center")

    



def create_organismo_form() -> rx.Component:
    return rx.form(
        rx.vstack(
        
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

def delete_organismo_dialog_component(id: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash_2"))),
        rx.dialog.content(
            rx.dialog.title("Eliminar Organismo"),
            rx.dialog.description("Esta seguro de querer eliminar el organismo " + str(id)),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        'Cancelar',
                        color_scheme="crimson",
                        variant="soft"
                    ),
                ),
                rx.dialog.close(
                    rx.button("Confirmar", on_click=OrganismoState.delete_organismo_by_id(id)),
                ),
                spacing="3",
                marging_top="16px",
                justify="end"
            )
        )
    )

def update_organismo_dialog_component(organismo: Organismo) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.flex(
    rx.icon("square-mouse-pointer"),
    
    gap="2",
))),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title(f"Editar Organismo {organismo.id_organismo}"),
                update_organismo_form(organismo),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"} 
        ),
    )
def buscar_organismo_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Buscar...", on_change=OrganismoState.buscar_on_change),
        rx.button("Buscar Organismo", on_click=OrganismoState.get_organismo_by_nombre)
    )

def update_organismo_form(organismo: Organismo) -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="ID",
                name="id_organismo",
                value=organismo.id_organismo
                
            ),
            rx.input(
                placeholder="Nombre", 
                name="nombre",
                default_value=organismo.nombre,
                is_required=True,
            ),
            rx.input(placeholder="Siglas", name="siglas", default_value=f"{organismo.siglas}"),
            rx.input(placeholder="Direccion", name="direccion", default_value=organismo.direccion),
            rx.input(placeholder="Telefono", name="telefono", default_value=organismo.telefono),

            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=OrganismoState.update_organismo,
    )