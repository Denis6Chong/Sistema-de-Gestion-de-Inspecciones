import reflex as rx
from ..utils.for_table import header_cell
from ..templates import template
from ..model.all_model import Requisito, Organismo
from ..service.norma_service import select_all_normas_service
from ..service.requisito_service import *
from ..notify import notify_component
import asyncio
from ..utils.base import State
class RequisitoState(rx.State):
    #states
    requisito:list[Requisito]
    requisito_buscar: str
    error: str = ""
    norma_lista: list[str] = []
    nombre_norma: str = ""
    codigo_norma_lista: list[str] = []


    @rx.background
    async def load_all_data(self):
        
        yield RequisitoState.get_all_requisito()
        yield RequisitoState.load_norma_lista()
        yield State.check_login()

    def buscar_norma_on_change(self, value: str):
        self.nombre_norma = str(value)

    @rx.background
    async def load_norma_lista(self):
        normas = select_all_normas_service()
        lista = [norma.titulo for norma in normas]
        lista_codigo = [norma.codigo_norma for norma in normas]
        async with self:
            self.norma_lista = lista
            self.codigo_norma_lista = lista_codigo


    @rx.background
    async def get_all_requisito(self):
        async with self:
            self.requisito = select_all_requisitos_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""

    def buscar_on_change(self, value: str):
        self.requisito_buscar = value
    @rx.background
    async def get_requisito_by_nombre(self):
        async with self:
            self.requisito = select_requisito_by_titulo_requisito_service(self.requisito_buscar)

    @rx.background
    async def create_requisito(self, data: dict):
        async with self:
            try:
                self.requisito = create_requisito_service(
                    id="",
                    titulo=data["titulo"],
                    codigo_norma=data["codigo_norma"],
                    )
                                                        
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    
    
    @rx.background
    async def update_requisito(self, data: dict):
        print("Datos enviados para actualizar: ", data)
        async with self:
            try:
                
                
                self.requisito = update_requisito_service(
                    id=data["id"],
                    titulo=data["titulo"], 
                    codigo_norma=data["codigo_norma"],
                )
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    async def get_requisito_by_norma(self):
        try:
            self.requisito = select_requisito_by_nombre_norma_service(self.nombre_norma)
        except BaseException as be:
            print(be.args)
            self.error = be.args

    @rx.background
    async def delete_requisito_by_id(self, id_requisito):
        async with self:
            self.requisitos = delete_requisito_service(id_requisito)



@template(route="/requisitos", title="Requisitos", on_load=RequisitoState.load_all_data)
def requisito_page() -> rx.Component:
    return rx.flex(
        rx.hstack(
                        rx.icon("book_open", size=25),
                        rx.heading(f"Requisitos", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
            rx.hstack(
                buscar_requisito_component(),
                create_requisito_dialogo_component(),
                filtro_norma_component(),
                justify="center",
                style={"margin-top": '30px'}
            ),
        table_requisito(RequisitoState.requisito),
        rx.cond(
            RequisitoState.error != "",
            notify_component(RequisitoState.error, "shield-alert", "yellow")

        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )

def table_requisito(list_requisito: list[Requisito]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                header_cell("ID", "hash"),
                header_cell("Acápites", "case-sensitive"),
                header_cell("Código_Norma", "book"),    
                header_cell("Acción", "cog")
            )
        ),
    rx.table.body(
        rx.foreach(list_requisito, lambda requisito, index=None: row_table(requisito, index))
        )
    )

def row_table(requisito: Requisito, index: int) -> rx.Component:
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
        rx.table.cell(requisito.id),
        rx.table.cell(requisito.titulo ),
        rx.table.cell(requisito.codigo_norma),
        rx.table.cell(
            rx.hstack(
                update_requisito_dialog_component(requisito),
                delete_requisito_dialog_component(requisito.id),
                
            ), align="center"
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center")





def create_requisito_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="Título",
                name="titulo",
                is_required=True,
            ),
            rx.select(RequisitoState.codigo_norma_lista,
                
                placeholder="Código_Norma",  
                name="codigo_norma",  # Nombre de la clave para el formulario
                required=True,
                ),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=RequisitoState.create_requisito,
    )

def create_requisito_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Requisito")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Requisito"),
                create_requisito_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )

def delete_requisito_dialog_component(id: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash_2"))),
        rx.dialog.content(
            rx.dialog.title("Eliminar Requisito"),
            rx.dialog.description("Esta seguro de querer eliminar el usuaro " + str(id)),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        'Cancelar',
                        color_scheme="crimson",
                        variant="soft"
                    ),
                ),
                rx.dialog.close(
                    rx.button("Confirmar", on_click=RequisitoState.delete_requisito_by_id(id)),
                ),
                spacing="3",
                marging_top="16px",
                justify="end"
            )
        )
    )

def update_requisito_dialog_component(requisito: Requisito) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.flex(
    rx.icon("square-mouse-pointer"),
    
    gap="2",
))),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title(f"Editar Requisito {requisito.titulo}"),
                update_requisito_form(requisito),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"} 
        ),
    )
def buscar_requisito_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ingrese nombre", on_change=RequisitoState.buscar_on_change),
        rx.button("Buscar Requisito", on_click=RequisitoState.get_requisito_by_nombre)
    )

def update_requisito_form(requisito: Requisito) -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="ID",
                name="id",
                value=requisito.id,
                
                
            ),
            rx.input(
                placeholder="Título",
                name="titulo",
                default_value=requisito.titulo,
                is_required=True,
            ),
            rx.select(RequisitoState.codigo_norma_lista,
                
                placeholder="Código_Norma",  
                name="codigo_norma",  # Nombre de la clave para el formulario
                required=True,
                default_value=f"{requisito.codigo_norma}"
                ),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=RequisitoState.update_requisito,
    )

def filtro_norma_component() -> rx.Component:
    return rx.hstack(
        rx.select(RequisitoState.norma_lista,
                placeholder="Seleccione la Norma", on_change=RequisitoState.buscar_norma_on_change),
        rx.button("Aplicar Filtro", on_click=RequisitoState.get_requisito_by_norma) 
    )