import reflex as rx
from ..utils.for_table import header_cell
from ..templates import template
from ..model.all_model import Inspector, Municipio
from ..service.provincia_service import select_all_provincia_service
from ..service.municipio_service import select_all_municipio_service
from ..service.inspector_service import tiene_inspecciones_service, select_inspector_by_municipio_service, select_inspector_by_provincia_service, update_inspector_service,select_all_inspector_service, select_inspector_by_email_service, create_inspector_service, delete_inspector_service, select_all_inspectors_oh
from ..notify import notify_component
import asyncio

class InspectorState(rx.State):
    #states
    inspector:list[Inspector]
    inspector_buscar: str
    error: str = ""
    selected_filter: str = ""
    nombre_municipio: str = ""
    nombre_provincia: str = ""
    


    def buscar_municipio_on_change(self, value: str):
        self.nombre_municipio = str(value)

    def buscar_provincia_on_change(self, value: str):
        self.nombre_provincia = str(value)

    def on_filter_change(self, value: str):
        self.selected_filter = value

    @rx.background
    async def get_all_inspector(self):
        async with self:
            self.inspector = select_all_inspector_service()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""

    async def get_inspector_by_municipio(self):
        try:
            self.inspector = select_inspector_by_municipio_service(self.nombre_municipio)
        except BaseException as be:
            print(be.args)
            self.error = be.args

    async def get_inspector_by_provincia(self):
        try:
            self.inspector = select_inspector_by_provincia_service(self.nombre_provincia)
        except BaseException as be:
            print(be.args)
            self.error = be.args

    @rx.background
    async def get_inspector_by_email(self):
        async with self:
            self.inspector = select_inspector_by_email_service(self.inspector_buscar)

    @rx.background
    async def create_inspector(self, data: dict):
        async with self:
            try:
                self.inspector = create_inspector_service(
                                                        codigo_inspector="",
                                                        nombre=data["nombre"], 
                                                        apellidos=data["apellidos"], 
                                                        direccion=data["direccion"], 
                                                        municipio=data["municipio"],
                                                        telefono=data["telefono"],
                                                        sexo=data["sexo"],
                                                        ci=data["ci"],
                                                        baja=0)
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    @rx.background
    async def update_inspector(self, data: dict):
        print("Datos enviados para actualizar: ", data)
        async with self:
            try:
                baja = 1 if data.get("baja") else 0
                
                self.inspector = update_inspector_service(
                    codigo_inspector=data["codigo_inspector"],
                    nombre=data["nombre"], 
                    apellidos=data["apellidos"], 
                    direccion=data["direccion"],
                    telefono=data["telefono"],
                    sexo=data["sexo"],
                    ci=data["ci"],
                    baja=baja,
                    municipio=data["municipio"],
                )
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()


    def buscar_on_change(self, value: str):
        self.inspector_buscar = value

    @rx.background
    async def delete_inspector_by_email(self, ci):
        async with self:
            self.inspector = delete_inspector_service(ci)    


@template(route="/inspectores", title="Inspectores", on_load=InspectorState.get_all_inspector)
def inspector_page() -> rx.Component:
    return rx.flex(
        rx.hstack(
                        rx.icon("user-round-search", size=25),
                        rx.heading(f"Inspectores", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
            rx.hstack(
                buscar_inspector_component(),
                filtro_general_component(),
                create_inspector_dialogo_component(),
                justify="center",
                style={"margin-top": '30px'}
            ),
        table_inspector(InspectorState.inspector),
        rx.cond(
            InspectorState.error != "",
            notify_component(InspectorState.error, "shield-alert", "yellow")

        ),
        direction="column",
        style={"width": "60vw", "margin": "auto"}
    )

    
def table_inspector(list_inspector: list[Inspector]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                header_cell("Código","code"),
                header_cell("Nombre","case-sensitive"),
                header_cell("Apellidos","case-sensitive"),
                header_cell("Dirección","map-pin"),
                header_cell("Municipio", "map-pinned"),
                header_cell("Teléfono", "smartphone"), 
                header_cell("Sexo", "heart"),
                header_cell("CI", "hash"),
                header_cell("Baja", "log-out"),
                header_cell("Accion", "cog")
            )
        ),
    rx.foreach(list_inspector, lambda inspector, index=None: row_table(inspector, index))
    )

def row_table(inspector: Inspector,index: int,) -> rx.Component:
    bg_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 1),
        rx.color("accent", 2),)
    
    hover_color = rx.cond(
        index % 2 == 0,
        rx.color("gray", 3),
        rx.color("accent", 3),)
    return rx.table.row(
        rx.table.cell(inspector.codigo_inspector, align="center",width="100px"),
        rx.table.cell(inspector.nombre, align="center", width="100px"),
        rx.table.cell(inspector.apellidos, align="center", width="100px"),
        rx.table.cell(inspector.direccion, align="center", width="100px"),
        rx.table.cell(inspector.municipio, align="center", width="100px"),
        rx.table.cell(inspector.telefono, align="center", width="100px"),
        rx.table.cell(inspector.sexo, align="center", width="100px"),
        rx.table.cell(inspector.ci, align="center", width="100px"),
        rx.table.cell(inspector.baja, align="center", width="100px"),
        rx.table.cell(update_inspector_dialog_component(inspector),
                    align="center",width="100px"),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )

def buscar_inspector_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Buscar...", on_change=InspectorState.buscar_on_change),
        rx.button("Buscar Inspector", on_click=InspectorState.get_inspector_by_email) 
    )
municipios = select_all_municipio_service()
municipios_nombres=[]

for municipio in municipios:
    municipios_nombres.append(municipio.nombre) 

def create_inspector_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(
                
                placeholder="Nombre",
                name="nombre",
                is_required=True,
            ),
            rx.input(
                placeholder="Apellidos",
                name="apellidos",
                is_required=True,
            ),
            rx.input(
                placeholder="Dirección",
                name="direccion"
            ),
            rx.select(
                municipios_nombres,
                placeholder="Municipio",
                name="municipio",
            ),
            rx.input(
                placeholder="Teléfono",
                name="telefono"
            ),
            rx.select(["M", "F"],
                placeholder="SEXO",
                name="sexo"
            ),
            rx.input(
                placeholder="CI",
                name="ci"
            ),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ), align="stretch"
        ),
        on_submit=InspectorState.create_inspector,
    )

def create_inspector_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Inspector")),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Añadir Inspector"),
                create_inspector_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )

def delete_inspector_dialog_component(ci: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash_2"))),
        rx.dialog.content(
            rx.dialog.title("Eliminar Inspector"),
            rx.dialog.description("Esta seguro de querer eliminar el usuaro " + str(ci)),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        'Cancelar',
                        color_scheme="crimson",
                        variant="soft"
                    ),
                ),
                rx.dialog.close(
                    rx.button("Confirmar", on_click=InspectorState.delete_inspector_by_email(ci)),
                ),
                spacing="3",
                marging_top="16px",
                justify="end"
            )
        )
    )


def update_inspector_form(inspector: Inspector) -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="ID", name="codigo_inspector", value=inspector.codigo_inspector),
            rx.input(
                
                placeholder="Nombre",
                name="nombre",
                default_value=inspector.nombre
            ),
            rx.input(
                placeholder="Apellidos",
                name="apellidos",
                default_value=inspector.apellidos
            ),
            rx.input(
                placeholder="Direccion",
                name="direccion",
                default_value=inspector.direccion
                
            ),
            rx.select(
                municipios_nombres,
                placeholder="Municipio",
                name="municipio",
                default_value=inspector.municipio
            ),
            rx.input(
                placeholder="Telefono",
                name="telefono",
                default_value=inspector.telefono
            ),
            rx.select(["M", "F"],
                placeholder="Sexo",
                name="sexo",
                default_value=inspector.sexo
            ),
            rx.input(
                placeholder="Email",
                name="ci",
                default_value=inspector.ci
            ),
            rx.checkbox(
                "Baja",
                name="baja",
                default_checked=(inspector.baja == 1)
            ),
            rx.dialog.close(
                rx.button("Guardar", type="submit")
            ), align="stretch"
        ),
        on_submit=InspectorState.update_inspector,
    )

def update_inspector_dialog_component(inspector: Inspector) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.flex(
    rx.icon("square-mouse-pointer"),
    
    gap="2",
))),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title(f"Editar Inspector {inspector.nombre}"),
                update_inspector_form(inspector),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"} 
        ),
    )


def filtro_general_component() -> rx.Component:
    return rx.hstack(
        rx.select(
                [("Seleccionar Filtro"),
                ("Municipio"),
                ("Provincia"),
            ],
            placeholder="Seleccionar Filtro",
            on_change=InspectorState.on_filter_change
        ),
        rx.cond(
            InspectorState.selected_filter == "Municipio",
            filtro_municipio_component()
        ),
        rx.cond(
            InspectorState.selected_filter == "Provincia",
            filtro_provincia_component()
        ),
        
        rx.icon("filter", size=20),
    )

municipios = select_all_municipio_service()
municipios_list=[]

for municipio in municipios:
    municipios_list.append(municipio.nombre)

provincias = select_all_provincia_service()
provincias_list=[]

for provincia in provincias:
    provincias_list.append(provincia.nombre)    


def filtro_municipio_component() -> rx.Component:
    return rx.hstack(
        rx.select(municipios_list,
                placeholder="Seleccione el Municipio", on_change=InspectorState.buscar_municipio_on_change),
        rx.button("Aplicar Filtro", on_click=InspectorState.get_inspector_by_municipio) 
    )

def filtro_provincia_component() -> rx.Component:
    return rx.hstack(
        rx.select(provincias_list,
                placeholder="Seleccione la Provinica", on_change=InspectorState.buscar_provincia_on_change),
        rx.button("Aplicar Filtro", on_click=InspectorState.get_inspector_by_provincia) 
    )

