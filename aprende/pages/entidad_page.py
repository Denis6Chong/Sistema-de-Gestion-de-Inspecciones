import reflex as rx
from ..utils.for_table import header_cell
from ..templates import template
from ..model.all_model import Entidad, Organismo
from ..service.organismo_service import select_all_organismo_service
from ..service.entidad_service import delete_entidad_service, select_entidad_by_nombre_organismo_service,update_entidad_service,select_all_entidad_service, select_entidad_by_nombre_service, create_entidad_service
from ..notify import notify_component
import asyncio

class EntidadState(rx.State):
    #states
    entidad:list[Entidad]
    entidad_buscar: str
    error: str = ""
    organismo_lista: list[str] = []
    nombre_organismo: str = ""



    @rx.background
    async def load_all_data(self):
        
        yield EntidadState.get_all_entidad()
        yield EntidadState.load_organismo_lista()

    def buscar_organismo_on_change(self, value: str):
        self.nombre_organismo = str(value)

    @rx.background
    async def load_organismo_lista(self):
        organismos = select_all_organismo_service()
        lista = [organismo.nombre for organismo in organismos]
        async with self:
            self.organismo_lista = lista    

    @rx.background
    async def get_all_entidad(self):
        async with self:
            self.entidad = select_all_entidad_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""

    def buscar_on_change(self, value: str):
        self.entidad_buscar = value
    @rx.background
    async def get_entidad_by_nombre(self):
        async with self:
            self.entidad = select_entidad_by_nombre_service(self.entidad_buscar)

    @rx.background
    async def create_entidad(self, data: dict):
        async with self:
            try:
                self.entidad = create_entidad_service(
                    id_entidad=data["id_entidad"],
                    nombre=data["nombre"],
                    siglas=data["siglas"],
                    id_organismo=data["id_organismo"]
                    )
                                                        
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    
    
    @rx.background
    async def update_entidad(self, data: dict):
        print("Datos enviados para actualizar: ", data)
        async with self:
            try:
                
                
                self.entidad = update_entidad_service(
                    id_entidad=data["id_entidad"],
                    nombre=data["nombre"], 
                    siglas=data["siglas"],
                    id_organismo=data["id_organismo"],
                )
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    async def get_entidad_by_organismo(self):
        try:
            self.entidad = select_entidad_by_nombre_organismo_service(self.nombre_organismo)
        except BaseException as be:
            print(be.args)
            self.error = be.args

    @rx.background
    async def delete_entidad_by_id(self, id_entidad):
        async with self:
            self.entidads = delete_entidad_service(id_entidad)



@template(route="/entidades", title="Entidades", on_load=EntidadState.load_all_data)
def entidad_page() -> rx.Component:
    return rx.flex(
        rx.hstack(
                        rx.icon("circle-dot", size=25),
                        rx.heading(f"Entidades", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
            rx.hstack(
                buscar_entidad_component(),
                create_entidad_dialogo_component(),
                filtro_organismo_component(),
                justify="center",
                style={"margin-top": '30px'}
            ),
        table_entidad(EntidadState.entidad),
        rx.cond(
            EntidadState.error != "",
            notify_component(EntidadState.error, "shield-alert", "yellow")

        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )

def table_entidad(list_entidad: list[Entidad]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                header_cell("ID", "hash"),
                header_cell("Nombre", "case-sensitive"),
                header_cell("Siglas", "case-upper"),
                header_cell("Organismo", "globe"),    
                header_cell("Acción", "cog")
            )
        ),
    rx.table.body(
        rx.foreach(list_entidad, lambda entidad, index=None: row_table(entidad, index))
        )
    )

def row_table(entidad: Entidad, index: int) -> rx.Component:
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
        rx.table.cell(entidad.id_entidad),
        rx.table.cell(entidad.nombre ),
        rx.table.cell(entidad.siglas),
        rx.cond(
            entidad.organismo_relation,
            rx.table.cell(entidad.organismo_relation.nombre),  # Si existe, mostrar el nombre
            rx.table.cell("N/A")  # Si no existe, mostrar "N/A"
        ),
        rx.table.cell(
            rx.hstack(
                update_entidad_dialog_component(entidad),
                delete_entidad_dialog_component(entidad.id_entidad),
                
            ), align="center"
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center")





def create_entidad_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="ID",
                name="id_entidad"
                
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
            rx.select.root(
                rx.select.trigger(placeholder="Organismo"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            EntidadState.organismo_lista,  # Lista de inspectores con nombre y código
                            lambda organismo: rx.select.item(
                                organismo[0], value=organismo[1]  # Nombre y código del inspector
                            )
                        )
                    )
                ),name="id_organismo",  # Nombre de la clave para el formulario
                required=True,
                ),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=EntidadState.create_entidad,
    )

def create_entidad_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Entidad")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Entidad"),
                create_entidad_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )

def delete_entidad_dialog_component(id: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash_2"))),
        rx.dialog.content(
            rx.dialog.title("Eliminar Entidad"),
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
                    rx.button("Confirmar", on_click=EntidadState.delete_entidad_by_id(id)),
                ),
                spacing="3",
                marging_top="16px",
                justify="end"
            )
        )
    )

def update_entidad_dialog_component(entidad: Entidad) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.flex(
    rx.icon("square-mouse-pointer"),
    
    gap="2",
))),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title(f"Editar Entidad {entidad.nombre}"),
                update_entidad_form(entidad),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"} 
        ),
    )
def buscar_entidad_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ingrese nombre", on_change=EntidadState.buscar_on_change),
        rx.button("Buscar Entidad", on_click=EntidadState.get_entidad_by_nombre)
    )

def update_entidad_form(entidad: Entidad) -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="ID",
                name="id_entidad",
                value=entidad.id_entidad
                
            ),
            rx.input(
                placeholder="Nombre",
                name="nombre",
                default_value=entidad.nombre,
                is_required=True,
            ),
            rx.input(
                placeholder="Siglas",
                name="siglas",
                default_value=entidad.siglas,
            ),
            rx.select.root(
                rx.select.trigger(placeholder="Organismo"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            EntidadState.organismo_lista,  # Lista de inspectores con nombre y código
                            lambda organismo: rx.select.item(
                                organismo[0], value=organismo[1]  # Nombre y código del inspector
                            )
                        )
                    )
                ),
                default_value=f"{entidad.id_entidad}",
                name="id_organismo",  # Nombre de la clave para el formulario
                required=True,
                ),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=EntidadState.create_entidad,
    )

def filtro_organismo_component() -> rx.Component:
    return rx.hstack(
        rx.select(EntidadState.organismo_lista,
                placeholder="Seleccione el Organismo", on_change=EntidadState.buscar_organismo_on_change),
        rx.button("Aplicar Filtro", on_click=EntidadState.get_entidad_by_organismo) 
    )