import reflex as rx
from ..templates import template
from ..utils.for_table import header_cell
from ..utils.base import State
from ..model.all_model import Lineamiento
from ..service.lineamiento_service import (
    select_all_lineamientos_service,
    create_lineamiento_service,
    delete_lineamiento_service,
    select_lineamiento_by_numero_service,
    update_lineamiento_service,
    select_lineamiento_by_titulo_service
)
from ..notify import notify_component
import asyncio

class LineamientoState(rx.State):
    # states
    lineamientos: list[Lineamiento] = []
    error: str = ""
    lineamiento_buscar: str

    @rx.background
    async def get_all_lineamientos(self):
        yield State.check_login()
        async with self:
            self.lineamientos = select_all_lineamientos_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""

    @rx.background
    async def get_lineamiento_by_numero(self):
        async with self:
            self.lineamientos = select_lineamiento_by_titulo_service(self.lineamiento_buscar)




    @rx.background
    async def create_lineamiento(self, data: dict):
        async with self:
            try:
                self.lineamientos = create_lineamiento_service(
                    numero=data["numero"],
                    titulo=data["titulo"],
                )
            except BaseException as be:
                print(be.args)
                self.error = be.args
        await self.handleNotify()

    def buscar_on_change(self, value: str):
        self.lineamiento_buscar = value

    @rx.background
    async def delete_lineamiento(self, numero):
        async with self:
            self.lineamientos = delete_lineamiento_service(numero)

    @rx.background
    async def update_lineamiento(self, data: dict):
        print("Datos enviados para actualizar: ", data)
        async with self:
            try:
                
                
                self.lineamientos = update_lineamiento_service(
                    numero=data["numero"],
                    titulo=data["titulo"],

                    )
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()


@template(route="/lineamientos", title="Lineamientos", on_load=LineamientoState.get_all_lineamientos)
def lineamiento_page() -> rx.Component:
    return rx.flex(
        rx.hstack(
                        rx.icon("hash", size=25),
                        rx.heading(f"Lineamientos", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
        rx.hstack(
            buscar_lineamiento_component(),
            create_lineamiento_dialogo_component(),
            justify="center",
            style={"margin-top": '30px'}
        ),
        table_lineamiento(LineamientoState.lineamientos),
        rx.cond(
            LineamientoState.error != "",
            notify_component(LineamientoState.error, "shield-alert", "yellow")
        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )


def table_lineamiento(list_lineamientos: list[Lineamiento]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                header_cell("Numero", "hash"),
                header_cell("Titulo", "case-upper"),
                header_cell("Accion", "cog")
            )
        ),
        rx.table.body(
            rx.foreach(list_lineamientos, lambda lineamiento, index=None: row_table(lineamiento, index))
        )
    )


def row_table(lineamiento: Lineamiento, index) -> rx.Component:
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
        rx.table.cell(lineamiento.numero),
        rx.table.cell(lineamiento.titulo),
        rx.table.cell(
            rx.hstack(
                update_lineamiento_dialog_component(lineamiento),
                delete_lineamiento_dialog_component(lineamiento.numero),
                
            ), align="center"
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center")



def buscar_lineamiento_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Buscar...", on_change=LineamientoState.buscar_on_change, type="number"),
        rx.button("Buscar lineamiento", on_click=LineamientoState.get_lineamiento_by_numero)
    )


def create_lineamiento_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="Numero",
                name="numero",
                is_required=True,
                type="number"
            ),
            rx.input(
                placeholder="Titulo",
                name="titulo",
                is_required=True,
            ),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=LineamientoState.create_lineamiento,
    )


def create_lineamiento_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Lineamiento")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Lineamiento"),
                create_lineamiento_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )


def delete_lineamiento_dialog_component(numero: int) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash_2"))),
        rx.dialog.content(
            rx.dialog.title("Eliminar Lineamiento"),
            rx.dialog.description(f"¿Está seguro de querer eliminar el lineamiento número {numero}?"),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        'Cancelar',
                        color_scheme="crimson",
                        variant="soft"
                    ),
                ),
                rx.dialog.close(
                    rx.button("Confirmar", on_click=LineamientoState.delete_lineamiento(numero)),
                ),
                spacing="3",
                marging_top="16px",
                justify="end"
            )
        )
    )


def update_lineamiento_dialog_component(lineamiento: Lineamiento) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.flex(
    rx.icon("square-mouse-pointer"),
    
    gap="2",
))),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title(f"Editar Lineamiento {lineamiento.numero}"),
                update_lineamiento_form(lineamiento),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"} 
        ),
    )
def buscar_lineamiento_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ingrese Titulo", on_change=LineamientoState.buscar_on_change),
        rx.button("Buscar Lineamiento", on_click=LineamientoState.get_lineamiento_by_numero)
    )

def update_lineamiento_form(lineamiento: Lineamiento) -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="Numero",
                name="numero",
                value=lineamiento.numero,
            
                
            ),
            rx.input(
                placeholder="Título", 
                name="titulo",
                default_value=lineamiento.titulo,
                is_required=True,
            ),
        
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=LineamientoState.update_lineamiento,
    )