import reflex as rx
from ..utils.for_table import header_cell
from ..templates import template
from ..service.entidad_service import select_all_entidad_service
from ..service.provincia_service import select_all_provincia_service
from ..service.organismo_service import select_all_organismo_service
from ..service.municipio_service import select_all_municipio_service
from ..model.all_model import Establecimiento, Municipio, Entidad
from ..service.establecimiento_service import (
    select_all_establecimientos_service,
    select_establecimiento_by_nombre_service,
    create_establecimiento_service,
    update_establecimiento_service,
    delete_establecimiento_service,
    select_establecimiento_by_nombre_provincia_service,
    select_establecimientos_by_nombre_entidad_service,
    select_establecimientos_by_municipio_service,
    select_establecimiento_by_nombre_organismo_service
)
from ..notify import notify_component
import asyncio

class EstablecimientoState(rx.State):
    # States
    establecimientos: list[Establecimiento]
    establecimiento_buscar: str = ""
    error: str = ""
    entidad_lista: list[tuple[str, str]] = []
    municipio_lista: list[str] = []
    organismo_lista: list[str] = []
    provincia_lista: list[str] = []
    selected_filter: str = ""
    nombre_municipio: str = ""
    nombre_provincia: str = ""
    nombre_entidad: str = ""
    nombre_organismo: str = ""
    entidad_lista_nombre: list[str] = []

    

    
    def has_establecimientos(self) -> bool:
        """Devuelve True si hay establecimientos en la lista, False en caso contrario."""
        return bool(self.establecimientos)  # Verifica si la lista tiene elementos
    

    @rx.background
    async def get_all_establecimientos(self):
        async with self:
            self.establecimientos = select_all_establecimientos_service()

    @rx.background
    async def load_entidad_lista(self):
        entidades = select_all_entidad_service()
        lista = []
        lista_nombre = []
        for entidad in entidades:
            nombre = entidad.nombre  # Toma el nombre del establecimiento
            id_entidad = entidad.id_entidad
            lista.append((nombre, str(id_entidad)))
            lista_nombre.append(nombre)
        
        # Modificar el estado dentro de un bloque 'async with self'
        async with self:
            self.entidad_lista = lista 
            self.entidad_lista_nombre = lista_nombre

    @rx.background
    async def load_municipio_lista(self):
        municipios = select_all_municipio_service()
        lista = []
        for municipio in municipios:
            nombre = municipio.nombre  
            lista.append(nombre)
        # Modificar el estado dentro de un bloque 'async with self'
        async with self:
            self.municipio_lista = lista   



            
    @rx.background
    async def load_all_data(self):
        
        yield EstablecimientoState.load_entidad_lista()
        yield EstablecimientoState.load_municipio_lista()
        yield EstablecimientoState.get_all_establecimientos()
        yield EstablecimientoState.load_organismo_lista()
        yield EstablecimientoState.load_provincia_lista()                    

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""

    @rx.background
    async def get_establecimiento_by_nombre(self):
        async with self:
            self.establecimientos = select_establecimiento_by_nombre_service(self.establecimiento_buscar)
            
    @rx.background
    async def load_organismo_lista(self):
        organismos = select_all_organismo_service()
        lista = [organismo.nombre for organismo in organismos]
        async with self:
            self.organismo_lista = lista

    @rx.background
    async def load_provincia_lista(self):
        # Aquí se asume que hay un servicio similar para provincias
        provincias = select_all_provincia_service()  # Deberás tener este servicio disponible
        lista = [provincia.nombre for provincia in provincias]
        async with self:
            self.provincia_lista = lista






    @rx.background
    async def create_establecimiento(self, data: dict):
        async with self:
            try:
                self.establecimientos = create_establecimiento_service(
                    id_est=None,
                    nombre=data["nombre"],
                    direccion=data["direccion"],
                    telefono=data["telefono"],
                    municipio_nombre=data["municipio_nombre"],
                    id_entidad=data["id_entidad"]
                )
            except Exception as e:
                print(e.args)
                self.error = e.args
        await self.handleNotify()

    def buscar_on_change(self, value: str):
        self.establecimiento_buscar = value

    @rx.background
    async def update_establecimiento(self, data: dict):
        print("Datos enviados para actualizar: ", data)
        async with self:
            try:
                
                
                self.establecimientos = update_establecimiento_service(
                    id_est=data["id_est"],
                    nombre=data["nombre"], 
                    direccion=data["direccion"],
                    telefono=data["telefono"],
                    municipio_nombre=data["municipio_nombre"],
                    id_entidad=data["id_entidad"],
                )
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    @rx.background
    async def delete_establecimiento_by_id(self, id_est):
        async with self:
            self.establecimientos = delete_establecimiento_service(id_est)

    def on_filter_change(self, value: str):
        self.selected_filter = value

    def buscar_municipio_on_change(self, value: str):
        self.nombre_municipio = str(value)

    def buscar_provincia_on_change(self, value: str):
        self.nombre_provincia = str(value)

    def buscar_entidad_on_change(self, value: str):
        self.nombre_entidad = str(value)

    def buscar_organismo_on_change(self, value: str):
        self.nombre_organismo = str(value)

    async def get_establecimiento_by_municipio(self):
        try:
            self.establecimientos = select_establecimientos_by_municipio_service(self.nombre_municipio)
        except BaseException as be:
            print(be.args)
            self.error = be.args
    
    async def get_establecimiento_by_provincia(self):
        try:
            self.establecimientos = select_establecimiento_by_nombre_provincia_service(self.nombre_provincia)
        except BaseException as be:
            print(be.args)
            self.error = be.args

    async def get_establecimiento_by_entidad(self):
        try:
            self.establecimientos = select_establecimientos_by_nombre_entidad_service(self.nombre_entidad)
        except BaseException as be:
            print(be.args)
            self.error = be.args

    async def get_establecimiento_by_organismo(self):
        try:
            self.establecimientos = select_establecimiento_by_nombre_organismo_service(self.nombre_organismo)
        except BaseException as be:
            print(be.args)
            self.error = be.args


@template(route="/establecimientos", title="Establecimientos", on_load=EstablecimientoState.load_all_data)
def establecimiento_page() -> rx.Component:
    return rx.flex(
        rx.hstack(
                        rx.icon("building-2", size=25),
                        rx.heading(f"Establecimientos", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
        rx.hstack(
            buscar_establecimiento_component(),
            create_establecimiento_dialogo_component(),
            filtro_general_component(),
            justify="center",
            style={"margin-top": '30px'}
        ),
        table_establecimientos(EstablecimientoState.establecimientos),
        rx.cond(
            EstablecimientoState.error != "",
            notify_component(EstablecimientoState.error, "shield-alert", "yellow")
        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )

def table_establecimientos(list_establecimientos: list[Establecimiento]) -> rx.Component:
    
    return rx.cond(
        EstablecimientoState.has_establecimientos(),  # Usamos la propiedad del estado para la condición
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    header_cell("ID", "hash"),
                    header_cell("Nombre", "case-sensitive"),
                    header_cell("Direccion", "map-pin"),
                    header_cell("Telefono","smartphone"),
                    header_cell("Municipio", "map-pinned"),
                    header_cell("Entidad","circle-dot" ),
                    header_cell("Acción", "cog")
                )
            ),
            rx.table.body(
                rx.foreach(list_establecimientos, lambda establecimiento, index=None: row_table_establecimiento(establecimiento, index))
            )
        ),
        rx.text("No hay establecimientos disponibles")  # Lo que se muestra si no hay datos
    )

def row_table_establecimiento(establecimiento: Establecimiento, index: int) -> rx.Component:
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
        rx.table.cell(establecimiento.id_est ),
        rx.table.cell(establecimiento.nombre),
        rx.table.cell(establecimiento.direccion),
        rx.table.cell(establecimiento.telefono),
            rx.cond(
                establecimiento.est_municipio_relation,
                rx.table.cell(establecimiento.est_municipio_relation.nombre, ),
                rx.table.cell("N/A"),  # Mensaje en caso de que no haya relación
            ),
            rx.cond(
                establecimiento.entidad_relation,
                rx.table.cell(establecimiento.entidad_relation.nombre),
                rx.table.cell("N/A"),  # Mensaje en caso de que no haya relación
            ),
            rx.table.cell(
            rx.hstack(
                update_establecimiento_dialog_component(establecimiento),
                delete_establecimiento_dialog_component(establecimiento.id_est),
                
            ), align="center"
        ),
            style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center")
def buscar_establecimiento_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ingrese nombre", on_change=EstablecimientoState.buscar_on_change),
        rx.button("Buscar establecimiento", on_click=EstablecimientoState.get_establecimiento_by_nombre)
    )

def create_establecimiento_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="Nombre",
                name="nombre",
                is_required=True,
            ),
            rx.input(
                placeholder="Direccion",
                name="direccion"
            ),
            rx.input(
                placeholder="Telefono",
                name="telefono"
            ),
            rx.select(
                EstablecimientoState.municipio_lista,
                placeholder="Municipio",
                name="municipio_nombre",
                required=True
            ),
            rx.select.root(
                rx.select.trigger(placeholder="Entidad"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            EstablecimientoState.entidad_lista,  # Lista de inspectores con nombre y código
                            lambda entidad: rx.select.item(
                                entidad[0], value=entidad[1]  # Nombre y código del inspector
                            )
                        )
                    )
                ),name="id_entidad",  # Nombre de la clave para el formulario
                required=True,
                ),
            
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ),
        ),
        on_submit=EstablecimientoState.create_establecimiento,
    )

def create_establecimiento_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Establecimiento")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Crear Establecimiento"),
                create_establecimiento_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
        
    )



def delete_establecimiento_dialog_component(id_est: int) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash_2"))),
        rx.dialog.content(
            rx.dialog.title("Eliminar Establecimiento"),
            rx.dialog.description("Esta seguro de querer eliminar el establecimineto " + str(id_est)),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        'Cancelar',
                        color_scheme="crimson",
                        variant="soft"
                    ),
                ),
                rx.dialog.close(
                    rx.button("Confirmar", on_click=EstablecimientoState.delete_establecimiento_by_id(id_est)),
                ),
                spacing="3",
                marging_top="16px",
                justify="end"
            )
        )
    )


def update_establecimiento_dialog_component(establecimiento: Establecimiento) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.flex(
    rx.icon("square-mouse-pointer"),
    
    gap="2",
))),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title(f"Editar Establecimiento {establecimiento.nombre}"),
                update_establecimiento_form(establecimiento),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"} 
        ),
    )


def update_establecimiento_form(establecimiento: Establecimiento) -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="id_est", value=establecimiento.id_est),
            rx.input(
                
                placeholder="Nombre",
                name="nombre",
                default_value=establecimiento.nombre
            ),
            rx.input(
                placeholder="Dirección",
                name="direccion",
                default_value=establecimiento.direccion
                
            ),
            rx.select(
                EstablecimientoState.municipio_lista,
                placeholder="Municipio",
                name="municipio_nombre",
                default_value=establecimiento.municipio_nombre
            ),
            rx.input(
                placeholder="Telefono",
                name="telefono",
                default_value=establecimiento.telefono
            ),
            rx.select.root(
                rx.select.trigger(placeholder="Entidad"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            EstablecimientoState.entidad_lista,  # Lista de inspectores con nombre y código
                            lambda entidad: rx.select.item(
                                entidad[0], value=entidad[1]  # Nombre y código del inspector
                            )
                        )
                    )
                ),
                default_value=f"{establecimiento.id_entidad}",
                name="id_entidad",  # Nombre de la clave para el formulario
                required=True,
                
            ),
            
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ), align="stretch"
        ),
        on_submit=EstablecimientoState.update_establecimiento,
    )

def filtro_general_component() -> rx.Component:
    return rx.hstack(
        rx.select(
                [("Seleccionar Filtro"),
                ("Municipio"),
                ("Provincia"),
                ("Entidad"),
                ("Organismo"),
            
            ],
            placeholder="Seleccionar Filtro",
            on_change=EstablecimientoState.on_filter_change
        ),
        rx.cond(
            EstablecimientoState.selected_filter == "Municipio",
            filtro_municipio_component()
        ),
        rx.cond(
            EstablecimientoState.selected_filter == "Provincia",
            filtro_provincia_component()
        ),
        rx.cond(
            EstablecimientoState.selected_filter == "Entidad",
            filtro_entidad_component()
        ),
        rx.cond(
            EstablecimientoState.selected_filter == "Organismo",
            filtro_organismo_component()
        ),
        
        rx.icon("filter", size=20),
    )


def filtro_municipio_component() -> rx.Component:
    return rx.hstack(
        rx.select(EstablecimientoState.municipio_lista,
                placeholder="Seleccione el Municipio", on_change=EstablecimientoState.buscar_municipio_on_change),
        rx.button("Aplicar Filtro", on_click=EstablecimientoState.get_establecimiento_by_municipio) 
    )

def filtro_provincia_component() -> rx.Component:
    return rx.hstack(
        rx.select(EstablecimientoState.provincia_lista,
                placeholder="Seleccione la Provinica", on_change=EstablecimientoState.buscar_provincia_on_change),
        rx.button("Aplicar Filtro", on_click=EstablecimientoState.get_establecimiento_by_provincia) 
    )


def filtro_organismo_component() -> rx.Component:
    return rx.hstack(
        rx.select(EstablecimientoState.organismo_lista,
                placeholder="Seleccione el Organismo", on_change=EstablecimientoState.buscar_organismo_on_change),
        rx.button("Aplicar Filtro", on_click=EstablecimientoState.get_establecimiento_by_organismo) 
    )

def filtro_entidad_component() -> rx.Component:
    
    return rx.hstack(
        rx.select(EstablecimientoState.entidad_lista_nombre,
                placeholder="Seleccione la Entidad", on_change=EstablecimientoState.buscar_entidad_on_change),
        rx.button("Aplicar Filtro", on_click=EstablecimientoState.get_establecimiento_by_entidad) 
    )