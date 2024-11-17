import reflex as rx
from ..templates import template
from ..model.all_model import *
from ..service.tabs_service import *
import asyncio
from datetime import date
from ..notify import notify_component


class TabsState(rx.State):
    """State for handling inspection creation steps."""
    
    current_tab = "principal"
    next_tab = ""
    inspeccion: list[Inspeccion]
    error: str = ""


    def set_tab(self, tab_name):
        """Set the current tab."""
        self.current_tab = tab_name

    def initialize_tab(self):
        """Initialize the tab to the default value on page load."""
        self.set_tab("principal")
    
    
    @rx.background
    
    async def create_inspeccion(self, data: dict):
        
        print("estoy dentro")
        async with self:
            try:
                self.inspeccion = create_inspeccion_service(
                    id_inspeccion=data["id_inspeccion"],
                    codigo_inspeccion=data["codigo_inspeccion"],
                    prod_o_serv_insp=data["prod_o_serv_insp"],
                    fecha_inicio=data["fecha_inicio"],
                    fecha_fin=data["fecha_fin"],
                    infraccion_p_o_s=data["infraccion_p_o_s"],
                    infraccion_higiene=data["infraccion_higiene"],
                    infraccion_metrologia=data["infraccion_metrologia"],
                    codigo_inspector=data["codigo_inspector"],
                    id_est=data["id_est"],
                    id_informe=data["id_informe"],
                    numero_lineamiento=data["numero_lineamiento"],
                )
            except BaseException as be:
                print(be.args)
                self.error = be.args    
        await self.handleNotify()

    async def handleNotify(self):
        async with self:
            await asyncio.sleep(3)
            self.error = ""


@template(route="/creacion", title="Crear", on_load=TabsState.initialize_tab)


def inspection_creation() -> rx.Component:
    return rx.container(
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger("Principal", value="principal"),
                rx.tabs.trigger("Obligaciones de Hacer - Producto/Servicio", value="producto"),
                rx.tabs.trigger("Obligaciones de Hacer - Higiene", value="higiene"),
                rx.tabs.trigger("Obligaciones de Hacer - Metrología", value="metrologia"),
            ),
            rx.tabs.content(
                # Tab principal con los campos iniciales de la inspección
                rx.text("Llene la información principal de la inspección aquí."),
                create_inspeccion_form(),
                
                value="principal",
                
            ),
            rx.tabs.content(
                # Tab para Obligaciones de Hacer - Producto o Servicio
                rx.text("Obligaciones de Producto o Servicio."),
                # Agrega aquí los componentes necesarios para la infracción de Producto/Servicio
                value="producto",
            ),
            rx.tabs.content(
                # Tab para Obligaciones de Hacer - Higiene
                rx.text("Obligaciones de Higiene."),
                # Agrega aquí los componentes necesarios para la infracción de Higiene
                value="higiene",
            ),
            rx.tabs.content(
                # Tab para Obligaciones de Hacer - Metrología
                rx.text("Obligaciones de Metrología."),
                # Agrega aquí los componentes necesarios para la infracción de Metrología
                value="metrologia",
            ),
            default_value="principal",
            value=TabsState.current_tab,
            on_change=lambda x: TabsState.set_tab(x),
        ),
        padding="2em",
        font_size="2em",
        text_align="center",
    )



def create_inspeccion_form() -> rx.Component:
    return rx.form(
        rx.center(
            rx.vstack(
                rx.input(placeholder="ID", name="id_inspeccion"),
                rx.input(placeholder="Código", name="codigo_inspeccion"),
                rx.input(placeholder="Producto/Servicio", name="prod_o_serv_insp"),
                padding="0.3em",),
            rx.vstack(
                rx.input(placeholder="Fecha Inicio", name="fecha_inicio", type="date"),
                rx.input(placeholder="Fecha Fin", name="fecha_fin", type="date"),
                rx.input(placeholder="Código Inspector", name="codigo_inspector"),
                padding="0.3em"),
        
            rx.vstack(
                rx.input(placeholder="ID Establecimiento", name="id_est", type="number"),
                rx.input(placeholder="ID Informe", name="id_informe", type="number"),
                rx.input(placeholder="Número Lineamiento", name="numero_lineamiento", type="number"),
                padding="0.3em",
            )),
        rx.center(
            rx.hstack(
                rx.checkbox("Infracción P/S", name="infraccion_p_o_s"),
                rx.checkbox("Infracción Higiene", name="infraccion_higiene"),
                rx.checkbox("Infracción Metrología", name="infraccion_metrologia"),
                
                padding="0.3em",
                spacing="8"),
                ),
        rx.button(
                    rx.icon(tag="heart"),
                    "Añadir",
                    type="submit"),
        on_submit=TabsState.create_inspeccion,
                ) 
                
        

    