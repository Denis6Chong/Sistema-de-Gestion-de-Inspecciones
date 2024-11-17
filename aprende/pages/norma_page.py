import reflex as rx
from ..templates import template
from ..model.all_model import Norma
from ..service.norma_service import (
    select_all_normas_service,
    create_norma_service,
    delete_norma_service,
    select_norma_by_codigo_norma_service,
)
from ..notify import notify_component
import asyncio
import re

class NormaState(rx.State):
    # states
    normas: list[Norma] = []
    error: str = ""
    norma_buscar: str

    @rx.background
    async def get_all_normas(self):
        async with self:
            self.normas = select_all_normas_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""

    @rx.background
    async def get_norma_by_codigo_norma(self):
        async with self:
            self.normas = select_norma_by_codigo_norma_service(self.norma_buscar)


    @rx.background
    async def create_norma(self, data: dict):
            async with self:
                try:
                    self.normas = create_norma_service(
                        codigo_norma=data["codigo_norma"],
                        titulo=data["titulo"],
                    )
                except ValueError as ve:
                    print(ve.args)
                    self.error = ve.args[0]
                except BaseException as be:
                    print(be.args)
                    self.error = be.args[0]
            await self.handleNotify()

    def buscar_on_change(self, value: str):
        self.norma_buscar = value

    @rx.background
    async def delete_norma(self, codigo_norma):
        async with self:
            self.normas = delete_norma_service(codigo_norma)


@template(route="/normas", title="Normas", on_load=NormaState.get_all_normas)
def norma_page() -> rx.Component:
    return rx.flex(
        rx.hstack(
                        rx.icon("book", size=25),
                        rx.heading(f"Normas", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
        rx.hstack(
            buscar_norma_component(),
            create_norma_dialogo_component(),
            justify="center",
            style={"margin-top": '30px'}
        ),
        table_norma(NormaState.normas),
        rx.cond(
            NormaState.error != "",
            notify_component(NormaState.error, "shield-alert", "yellow")
        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )


def table_norma(list_normas: list[Norma]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Codigo"),
                rx.table.column_header_cell("Titulo"),
                rx.table.column_header_cell("Accion")
            )
        ),
        rx.table.body(
            rx.foreach(list_normas, row_table_norma)
        )
    )


def row_table_norma(norma: Norma) -> rx.Component:
    return rx.table.row(
        rx.table.cell(norma.codigo_norma),
        rx.table.cell(norma.titulo),
        rx.table.cell(rx.hstack(
            delete_norma_dialog_component(norma.codigo_norma)
        ))
    )


def buscar_norma_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ingrese codigo_norma", on_change=NormaState.buscar_on_change, type="^ISO\d{1,5}$"),
        rx.button("Buscar norma", on_click=NormaState.get_norma_by_codigo_norma)
    )


def create_norma_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="Codigo",
                name="codigo_norma",
                is_required=True,
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
        on_submit=NormaState.create_norma,
    )


def create_norma_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Norma")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Norma"),
                create_norma_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )


def delete_norma_dialog_component(codigo_norma: int) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash_2"))),
        rx.dialog.content(
            rx.dialog.title("Eliminar Norma"),
            rx.dialog.description(f"¿Está seguro de querer eliminar el norma número {codigo_norma}?"),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        'Cancelar',
                        color_scheme="crimson",
                        variant="soft"
                    ),
                ),
                rx.dialog.close(
                    rx.button("Confirmar", on_click=NormaState.delete_norma(codigo_norma)),
                ),
                spacing="3",
                marging_top="16px",
                justify="end"
            )
        )
    )
