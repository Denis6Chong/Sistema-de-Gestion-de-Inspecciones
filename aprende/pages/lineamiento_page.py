import reflex as rx
from ..templates import template
from ..model.all_model import Lineamiento
from ..service.lineamiento_service import (
    select_all_lineamientos_service,
    create_lineamiento_service,
    delete_lineamiento_service,
    select_lineamiento_by_numero_service,
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
        async with self:
            self.lineamientos = select_all_lineamientos_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""

    @rx.background
    async def get_lineamiento_by_numero(self):
        async with self:
            self.lineamientos = select_lineamiento_by_numero_service(self.lineamiento_buscar)




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
                rx.table.column_header_cell("Numero"),
                rx.table.column_header_cell("Titulo"),
                rx.table.column_header_cell("Accion")
            )
        ),
        rx.table.body(
            rx.foreach(list_lineamientos, row_table_lineamiento)
        )
    )


def row_table_lineamiento(lineamiento: Lineamiento) -> rx.Component:
    return rx.table.row(
        rx.table.cell(lineamiento.numero),
        rx.table.cell(lineamiento.titulo),
        rx.table.cell(rx.hstack(
            delete_lineamiento_dialog_component(lineamiento.numero)
        ))
    )


def buscar_lineamiento_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ingrese numero", on_change=LineamientoState.buscar_on_change, type="number"),
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
