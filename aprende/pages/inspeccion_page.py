import reflex as rx
from ..utils.for_table import header_cell
from ..model.all_model import Inspeccion
from ..templates import template
from ..utils.base import State

from ..service.lineamiento_service import select_all_lineamientos_service
from ..service.establecimiento_service import select_all_establecimientos_service
from ..service.inspector_service import select_all_disponibles_service
from ..service.organismo_service import select_all_organismo_service
from ..service.informe_service import select_all_informes_service
from ..service.inspeccion_service import *

from ..notify import notify_component
import asyncio
from datetime import date




inspectores = select_all_disponibles_service()
inspectores_nombres=[]
inspectores_codigo=[]


for inspector in inspectores:
    primer_nombre = inspector.nombre.split()[0]  # Toma el primer nombre
    primer_apellido = inspector.apellidos.split()[0]  # Toma el primer apellido
    nombre_completo = f"{primer_nombre} {primer_apellido}"
    inspectores_nombres.append(nombre_completo)
    inspectores_codigo.append(inspector.codigo_inspector)

lineamientos = select_all_lineamientos_service()
lineamientos_list = []

for lineamiento in lineamientos:
    numero=lineamiento.numero
    lineamientos_list.append(str(numero))


informes = select_all_informes_service()
informe_titulo=[]

for informe in informes:
    titulo=informe.titulo
    informe_titulo.append(str(titulo))



class InspeccionState(rx.State):
    # States
    inspeccion: list[Inspeccion]
    producto_servicio_buscar: str
    error: str = ""
    selected_month: int
    selected_year: int
    infraccion_filter: bool = False
    selected_filter: str = ""
    nombre_inspector: str = ""
    titulo_informe: str = ""
    nombre_organismo: str = ""
    inspectores_por_nombre = []
    inspectores_por_codigo =  []  # Lista de inspectores obtenidos de la base de datos
    selected_codigo_inspector: str = ""  # Código seleccionado

    inspectores_lista: list[tuple[str, str]] = []
    establecimiento_lista: list[tuple[str, str]] = []
    informes_lista: list[tuple[str, str]] = []

    
    
    def change_codigo_inspector(self, value:str):
        """Change the select value var."""
        self.selected_codigo_inspector = value
        

    def buscar_producto_servicio_on_change(self, value: str):
        self.producto_servicio_buscar = value
    
    def buscar_organismo_on_change(self, value: str):
        self.nombre_organismo = str(value)  # Método para cambiar el ID del organismo
    
    def nombre_inspector_on_change(self, value: str):
        self.nombre_inspector = str(value) 

    def titulo_informe_on_change(self, value: str):
        self.titulo_informe = str(value) 

    def on_filter_change(self, value: str):
        self.selected_filter = value

    def on_infraccion_filter_change(self, value: bool):
        self.infraccion_filter = value    
    
    def on_month_change(self, value: str):
        self.selected_month = int(value)

    
    def on_year_change(self, value: int):
    
        self.selected_year = int(value)


    @rx.background
    async def get_all_inspeccion(self):
        async with self:
            self.inspeccion = select_all_inspeccion_service()

    @rx.background
    async def load_inspectores_lista(self):
        inspectores = select_all_disponibles_service()
        lista = []
        for inspector in inspectores:
            primer_nombre = inspector.nombre.split()[0]  # Toma el primer nombre
            primer_apellido = inspector.apellidos.split()[0]  # Toma el primer apellido
            nombre_completo = f"{primer_nombre} {primer_apellido}"
            codigo_inspector = inspector.codigo_inspector
            lista.append((nombre_completo, codigo_inspector))

        # Modificar el estado dentro de un bloque 'async with self'
        async with self:
            self.inspectores_lista = lista

    @rx.background
    async def load_informe_lista(self):
        informes = select_all_informes_service()
        lista = []
        for informe in informes:
            titulo = informe.titulo
            id = informe.id_informe
            lista.append((titulo, str(id)))

        # Modificar el estado dentro de un bloque 'async with self'
        async with self:
            self.informes_lista = lista

    @rx.background
    async def load_establecimiento_lista(self):
        establecimientos = select_all_establecimientos_service()
        lista = []
        for establecimiento in establecimientos:
            nombre = establecimiento.nombre  # Toma el nombre del establecimiento
            id_est = establecimiento.id_est
            lista.append((nombre, str(id_est)))

        # Modificar el estado dentro de un bloque 'async with self'
        async with self:
            self.establecimiento_lista = lista

    @rx.background
    async def load_all_data(self):
        # Cargar inspectores, establecimientos e inspecciones al iniciar la página
        yield State.check_login()
        yield InspeccionState.load_inspectores_lista()
        yield InspeccionState.load_establecimiento_lista()
        yield InspeccionState.get_all_inspeccion()
        yield InspeccionState.load_informe_lista()
    

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""
    async def get_inspecciones_by_organismo(self):
        try:
            self.inspeccion = select_inspecciones_by_organismo_service(self.nombre_organismo)
        except BaseException as be:
            print(be.args)
            self.error = be.args
    async def get_inspecciones_by_inspector(self):
        try:
            self.inspeccion = select_inspecciones_by_nombre_inspector_service(self.nombre_inspector)
        except BaseException as be:
            print(be.args)
            self.error = be.args

    async def get_inspecciones_by_titulo_informe(self):
        try:
            self.inspeccion = select_inspeccion_by_titulo_informe_service(self.titulo_informe)
        except BaseException as be:
            print(be.args)
            self.error = be.args

    async def get_inspecciones_by_month(self):
        try:
            self.inspeccion = select_inspecciones_by_month_service(self.selected_month, self.selected_year)
        except BaseException as be:
            print(be.args)
            self.error = be.args

    async def get_inspecciones_with_infraccion(self):
        if self.infraccion_filter:
            self.inspeccion = select_inspecciones_without_infraccion_service()
            
        else:
            self.inspeccion = select_inspecciones_with_infraccion_service()

    
    @rx.background
    async def get_inspeccion_by_producto_servicio(self):
        async with self:
            self.inspeccion = select_inspeccion_by_producto_servicio_service(self.producto_servicio_buscar)

    @rx.background
    async def create_inspeccion(self, data: dict):
        
        
        async with self:
            try:
                infraccion_p_o_s = 1 if data.get("infraccion_p_o_s") else 0
                infraccion_higiene = 1 if data.get("infraccion_higiene") else 0
                infraccion_metrologia = 1 if data.get("infraccion_metrologia") else 0

                self.inspeccion = create_inspeccion_service(
                    id_inspeccion="",
                    codigo_inspeccion="",
                    codigo_real="",
                    prod_o_serv_insp=data["prod_o_serv_insp"],
                    fecha_inicio=data["fecha_inicio"],
                    fecha_fin=data["fecha_fin"],
                    infraccion_p_o_s=infraccion_p_o_s,
                    infraccion_higiene=infraccion_higiene,
                    infraccion_metrologia=infraccion_metrologia,
                    codigo_inspector=data["codigo_inspector"],
                    id_est=data["id_est"],
                    id_informe=data["id_informe"],
                    numero_lineamiento=int(data["numero_lineamiento"]),
                )
                
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()
    @rx.background
    async def update_inspeccion(self, data: dict):
        print("Datos enviados para actualizar: ", data)
        async with self:
            try:
                infraccion_p_o_s = 1 if data.get("infraccion_p_o_s") else 0
                infraccion_higiene = 1 if data.get("infraccion_higiene") else 0
                infraccion_metrologia = 1 if data.get("infraccion_metrologia") else 0
                fecha_fin = data["fecha_fin"] if data["fecha_fin"] else None
                id_informe = data["id_informe"] if data["id_informe"] else None
                self.inspeccion = update_inspeccion_service(
                    id_inspeccion=data["id_inspeccion"],
                    codigo_inspeccion=data["codigo_inspeccion"],
                    prod_o_serv_insp=data["prod_o_serv_insp"],
                    fecha_inicio=data["fecha_inicio"],
                    fecha_fin=fecha_fin,
                    infraccion_p_o_s=infraccion_p_o_s,
                    infraccion_higiene=infraccion_higiene,
                    infraccion_metrologia=infraccion_metrologia,
                    codigo_inspector=data["codigo_inspector"],
                    id_est=data["id_est"],
                    id_informe=id_informe,
                    numero_lineamiento=data["numero_lineamiento"],
                )
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    def buscar_on_change(self, value: str):
        self.inspeccion_buscar = value

    @rx.background
    async def delete_inspeccion_by_codigo(self, codigo):
        async with self:
            self.inspeccion = delete_inspeccion_service(codigo)

@template(route="/inspecciones", title="Inspecciones", on_load=InspeccionState.load_all_data)
def inspeccion_page() -> rx.Component:
    return rx.flex(
        rx.hstack(
                        rx.icon("text-search", size=25),
                        rx.heading(f"Inspecciones", size="7"),
                        align="center",
                        spacing="2",
                        style={"margin-top":"20px"}
                    ),
        rx.hstack(
            buscar_inspeccion_component(),
            filtro_general_component(),
            create_inspeccion_dialogo_component(),
            justify="center",
            style={"margin-top": '30px'}
        ),
        table_inspeccion(InspeccionState.inspeccion),
        rx.cond(
            InspeccionState.error != "",
            notify_component(InspeccionState.error, "shield-alert", "yellow")
        ),
        direction="column",
        style={"width": "auto", "margin": "auto"}
    )

def table_inspeccion(list_inspeccion: list[Inspeccion]) -> rx.Component:
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                header_cell("ID","hash"),
                header_cell("Código","code"),
                header_cell("Producto/Servicio", "bolt"),
                header_cell("Inicio","calendar"),
                header_cell("Fin", "calendar-check"),
                header_cell("P/S", "shield-minus"),
                header_cell("Higiene","shield-minus" ),
                header_cell("Metrología", "shield-minus"),
                header_cell("Inspector", "user"),
                header_cell("Establecimiento", "map-pin"),
                header_cell("Informe", "book"),
                header_cell("Lineamiento","book-open" ),
                header_cell("Acción", "cog")
            )
        ),
        rx.table.body(
            rx.foreach(list_inspeccion, lambda inspeccion, index=None: row_table(inspeccion, index))
        )
    )

def row_table(inspeccion: Inspeccion, index: int) -> rx.Component:
    
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
        rx.table.cell(inspeccion.id_inspeccion, align="center"),
        rx.table.cell(inspeccion.codigo_real, align="center"),
        rx.table.cell(inspeccion.prod_o_serv_insp, align="center"),
        rx.table.cell(inspeccion.fecha_inicio, align="center"),
        rx.table.cell(inspeccion.fecha_fin, align="center"),
        rx.table.cell(inspeccion.infraccion_p_o_s, align="center"),
        rx.table.cell(inspeccion.infraccion_higiene, align="center"),
        rx.table.cell(inspeccion.infraccion_metrologia, align="center"),
        rx.cond(
                inspeccion.inspector,
                rx.table.cell(inspeccion.inspector.nombre, align="center"),
                rx.table.cell("N/A"),  # Mensaje en caso de que no haya relación
            ),
        rx.cond(
                inspeccion.establecimiento,
                rx.table.cell(inspeccion.establecimiento.nombre, align="center"),
                rx.table.cell("N/A", align="center"),  # Mensaje en caso de que no haya relación
            ),
        rx.cond(
                inspeccion.informe,
                rx.table.cell(inspeccion.informe.id_informe, align="center"),
                rx.table.cell("N/A"),  # Mensaje en caso de que no haya relación
            ),
        rx.cond(
                inspeccion.lineamiento,
                rx.table.cell(inspeccion.lineamiento.numero,align="center"),
                rx.table.cell("N/A", align="center"),  # Mensaje en caso de que no haya relación
            ),

        rx.table.cell(
            rx.hstack(
                update_inspeccion_dialog_component(inspeccion),
                delete_inspeccion_dialog_component(inspeccion.codigo_inspeccion),
                
            ), align="center"
        ),
        style={"_hover": {"bg": hover_color}, "bg": bg_color},
        align="center",
    )

def buscar_inspeccion_component() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="Ingrese Producto/Servicio", on_change=InspeccionState.buscar_producto_servicio_on_change),
        rx.button("Buscar inspección", on_click=InspeccionState.get_inspeccion_by_producto_servicio)
    )


def create_inspeccion_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.input(placeholder="Producto/Servicio", name="prod_o_serv_insp"),
            rx.input(placeholder="Fecha Inicio", name="fecha_inicio", type="date"),
            rx.input(placeholder="Fecha Fin", name="fecha_fin", type="date"),
            rx.text("Infracciones"),
            rx.checkbox("Producto o Servicio", name="infraccion_p_o_s"),
            rx.checkbox("Higiene", name="infraccion_higiene"),
            rx.checkbox("Metrología", name="infraccion_metrologia"),
            rx.text("Seleccionar Inspector"),
            rx.select.root(
                rx.select.trigger(placeholder="Inspector"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            InspeccionState.inspectores_lista,  # Lista de inspectores con nombre y código
                            lambda inspector:
                                rx.select.item(inspector[0], value=inspector[1])
                        )
                    )
                ),
                name="codigo_inspector",  # Nombre de la clave para el formulario
                required=True,
            ),
            rx.select.root(
                rx.select.trigger(placeholder="Establecimiento"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            InspeccionState.establecimiento_lista,  # Lista de inspectores con nombre y código
                            lambda establecimiento: rx.select.item(
                                establecimiento[0], value=establecimiento[1]  # Nombre y código del inspector
                            )
                        )
                    )
                ),
                name="id_est",  # Nombre de la clave para el formulario
                required=True,
                
            ),
            rx.select.root(
                rx.select.trigger(placeholder="Informe"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            InspeccionState.informes_lista,  # Lista de inspectores con nombre y código
                            lambda informe: rx.select.item(
                                informe[0], value=informe[1]  # Nombre y código del inspector
                            )
                        )
                    )
                ),
                name="id_informe", 
                
            ),
            rx.select(lineamientos_list, placeholder="Lineamiento", name="numero_lineamiento"),
            rx.dialog.close(rx.button("Guardar", type="submit")),
        ),
        on_submit=InspeccionState.create_inspeccion,
    )

def create_inspeccion_dialogo_component() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button("Crear Inspección", )),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title("Añadir Inspección"),
                create_inspeccion_form(),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"}
        ),
    )

def delete_inspeccion_dialog_component(codigo: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash_2"))),
        rx.dialog.content(
            rx.dialog.title("Eliminar Inspección"),
            rx.dialog.description(f"¿Está seguro de querer eliminar la inspección con código {codigo}?"),
            rx.flex(
                rx.dialog.close(
                    rx.button('Cancelar', color_scheme="crimson", variant="soft"),
                ),
                rx.dialog.close(
                    rx.button("Confirmar", on_click=InspeccionState.delete_inspeccion_by_codigo(codigo)),
                ),
                spacing="3",
                marging_top="16px",
                justify="end"
            )
        )
    )

def update_inspeccion_form(inspeccion: Inspeccion) -> rx.Component:
    return rx.form(
        rx.vstack(
            # Los campos 'ID' y 'Código' pueden estar ocultos si no deben ser editados directamente
            rx.input(placeholder="ID", name="id_inspeccion", value=inspeccion.id_inspeccion, is_readonly=True),
            rx.input(placeholder="Código", name="codigo_inspeccion", value=inspeccion.codigo_inspeccion, is_readonly=True),

            # Producto/Servicio
            rx.input(placeholder="Producto/Servicio", name="prod_o_serv_insp", default_value=inspeccion.prod_o_serv_insp),

            # Fecha de Inicio (rellenada con el valor actual de la inspección)
            rx.input(placeholder="Fecha Inicio", name="fecha_inicio", type="date", default_value=f"{inspeccion.fecha_inicio}"),

            # Fecha de Fin (rellenada con el valor actual de la inspección)
            rx.input(placeholder="Fecha Fin", name="fecha_fin", type="date", default_value=f"{inspeccion.fecha_fin}"),
            
            # Infracciones
            rx.text("Infracciones"),
            # Checkbox para 'Producto o Servicio'
            rx.checkbox(
                "Producto o Servicio", 
                name="infraccion_p_o_s", 
                default_checked=(inspeccion.infraccion_p_o_s  == 1)  # Marcado si infraccion_p_o_s es 1
            ),
            
            # Checkbox para 'Higiene'
            rx.checkbox(
                "Higiene", 
                name="infraccion_higiene", 
                default_checked=(inspeccion.infraccion_higiene == 1)  # Marcado si infraccion_higiene es 1
            ),
            
            # Checkbox para 'Metrología'
            rx.checkbox(
                "Metrología", 
                name="infraccion_metrologia", 
                default_checked=(inspeccion.infraccion_metrologia == 1)  # Marcado si infraccion_metrologia es 1
            ),

            # Selección de Inspector
            rx.text("Seleccionar Inspector"),
            rx.select.root(
                rx.select.trigger(placeholder="Inspector"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            InspeccionState.inspectores_lista,
                            lambda inspector: rx.select.item(inspector[0], value=inspector[1])
                        )
                    )
                ),
                default_value=inspeccion.codigo_inspector,
                name="codigo_inspector",
                required=True,
            ),

            # Selección de Establecimiento
            rx.select.root(
                rx.select.trigger(placeholder="Establecimiento"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            InspeccionState.establecimiento_lista,
                            lambda establecimiento: rx.select.item(establecimiento[0], value=establecimiento[1])
                        )
                    )
                ),
                default_value=f"{inspeccion.id_est}",
                name="id_est",
                required=True,
            ),

            rx.select.root(
                rx.select.trigger(placeholder="Informe"),
                rx.select.content(
                    rx.select.group(
                        rx.foreach(
                            InspeccionState.informes_lista,  # Lista de inspectores con nombre y código
                            lambda informe: rx.select.item(
                                informe[0], value=informe[1]  # Nombre y código del inspector
                            )
                        )
                    )
                ),
                name="id_informe", 
                default_value=f"{inspeccion.id_informe}"),

            # Selección de Lineamiento
            rx.select(lineamientos_list, placeholder="Lineamiento", name="numero_lineamiento", default_value=f"{inspeccion.numero_lineamiento}"),

            # Botón de guardar
            rx.dialog.close(rx.button("Guardar", type="submit")),
        ),
        on_submit=InspeccionState.update_inspeccion,
    )



def update_inspeccion_dialog_component(inspeccion: Inspeccion) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.flex(
    rx.icon("square-mouse-pointer"),
    
    gap="2",
))),
        rx.dialog.content(
            rx.flex(
                rx.dialog.title(f"Editar Inspección {inspeccion.codigo_inspeccion}"),
                update_inspeccion_form(inspeccion),
                justify="center",
                align="center",
                direction="column",
            ),
            style={"width": "300px"} 
        ),
    )


def filtro_mes_ano_component() -> rx.Component:
    return rx.hstack(
        rx.select(
                    [("1"), ("2"), ("3"), ("4"), ("5"), 
                    ("6"), ("7"), ("8"), ("9"), 
                    ("10"), ("11"), ("12")],
            placeholder="Seleccione Mes",
            on_change=InspeccionState.on_month_change,
                ),
        rx.input(
            placeholder="Ingrese Año",
            on_change=InspeccionState.on_year_change,
            type="number",
            min=2000,  # Ajustar según la necesidad
            max=2100,
        ),
        rx.button("Filtrar", on_click=InspeccionState.get_inspecciones_by_month)
    )

# Componente de filtro general
def filtro_general_component() -> rx.Component:
    return rx.hstack(
        rx.select(
                [("Seleccionar Filtro"),
                ("Mes y Año"),
                ("Conformidad"),
                ("Inspector"),
                ("Organismo"),
                ("Informe")
            ],
            placeholder="Seleccionar Filtro",
            on_change=InspeccionState.on_filter_change
        ),
        rx.cond(
            InspeccionState.selected_filter == "Mes y Año",
            filtro_mes_ano_component()
        ),
        rx.cond(
            InspeccionState.selected_filter == "Conformidad",
            filtro_infraccion_component()
        ),
        rx.cond(
            InspeccionState.selected_filter == "Inspector",
            filtro_inspeccion_por_inspector_component()
        ),
        rx.cond(
            InspeccionState.selected_filter == "Organismo",
            filtro_organismo_component()
        ),
        rx.cond(
            InspeccionState.selected_filter == "Informe",
            filtro_informe_component()
        ),
        rx.icon("filter", size=20),
    )


# Filtro por infracciones
def filtro_infraccion_component() -> rx.Component:
    return rx.hstack(
        rx.checkbox("Conforme", on_change=InspeccionState.on_infraccion_filter_change),
        rx.button("Aplicar Filtro", on_click=InspeccionState.get_inspecciones_with_infraccion)
    )






def filtro_inspeccion_por_inspector_component() -> rx.Component:
    return rx.hstack(
        rx.select(inspectores_nombres, 
                placeholder="Inspector", on_change=InspeccionState.nombre_inspector_on_change),
        rx.button("Filtrar por Inspector", on_click=InspeccionState.get_inspecciones_by_inspector)
    )

def filtro_informe_component() -> rx.Component:
    return rx.hstack(
        rx.select(informe_titulo, 
                placeholder="Informe", on_change=InspeccionState.titulo_informe_on_change),
        rx.button("Filtrar por Informe", on_click=InspeccionState.get_inspecciones_by_titulo_informe)
    )

organismos = select_all_organismo_service()
organismos_nombres=[]

for organismo in organismos:
    organismos_nombres.append(organismo.nombre) 

def filtro_organismo_component() -> rx.Component:
    return rx.hstack(
        rx.select(organismos_nombres,
                placeholder="Seleccione el Organismo", on_change=InspeccionState.buscar_organismo_on_change),
        rx.button("Aplicar Filtro", on_click=InspeccionState.get_inspecciones_by_organismo) 
    )




