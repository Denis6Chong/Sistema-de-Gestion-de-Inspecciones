from ..model.all_model import Inspeccion, Informe, Entidad, Establecimiento, Organismo, Oblig_Hacer
from .connect_db import connect
from sqlmodel import Session, select
from datetime import date
from sqlalchemy.orm import joinedload
from sqlalchemy import or_


            
            

def create_inspeccion(inspeccion: Inspeccion) -> Inspeccion:
    """Crea una nueva inspección y devuelve la lista actualizada de inspecciones."""
    engine = connect()
    with Session(engine) as session:
        session.add(inspeccion)
        session.commit()
        return inspeccion
    
def create_informe(informe: Informe) -> Informe:
    engine = connect()
    with Session(engine) as session:
        session.add(informe)
        session.commit()
        return informe

def update_obligacion_hacer(codigo_obligacion: str, fecha_venc: date = None, fecha_comp: date = None, resultado: str = None, multa: float=None, codigo_norma: str = None) -> Oblig_Hacer:
    """Actualiza solo los atributos fecha_venc, fecha_comp, resultado y codigo_norma de una obligación de hacer."""
    engine = connect()
    with Session(engine) as session:
        # Obtener la obligación existente
        obligacion = session.get(Oblig_Hacer, codigo_obligacion)
        if obligacion:
            # Actualizar los atributos proporcionados
            if fecha_venc:
                obligacion.fecha_venc = fecha_venc
            if fecha_comp:    
                obligacion.fecha_comp = fecha_comp
            if resultado:  
                print (resultado)
                obligacion.resultado = resultado
            if multa:
                obligacion.multa = multa 
                print (multa)   
            if codigo_norma:
                obligacion.codigo_norma = codigo_norma

            # Guardar los cambios en la base de datos
        session.commit()
        session.refresh(obligacion)

        return obligacion


def select_inspecciones_with_infraccion():
    engine = connect()
    with Session(engine) as session:
        statement = select(Inspeccion).where(
            or_(
                Inspeccion.infraccion_p_o_s == 1,
                Inspeccion.infraccion_higiene == 1,
                Inspeccion.infraccion_metrologia == 1
            )
        ).options(
            joinedload(Inspeccion.inspector), 
            joinedload(Inspeccion.establecimiento),
            joinedload(Inspeccion.informe), 
            joinedload(Inspeccion.lineamiento))
        result = session.exec(statement)
        return result.all()

