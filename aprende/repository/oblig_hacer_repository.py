from ..model.all_model import Oblig_Hacer
from .connect_db import connect
from sqlmodel import Session, select
from datetime import date
from datetime import datetime, timedelta


def select_all_obligaciones() -> list[Oblig_Hacer]:
    """Obtiene todas las obligaciones de hacer."""
    engine = connect()
    with Session(engine) as session:
        query = select(Oblig_Hacer)
        obligaciones = session.exec(query).all()
        return obligaciones

def select_obligacion_by_codigo(codigo_obligacion: str) -> Oblig_Hacer:
    """Obtiene una obligación de hacer por su código."""
    engine = connect()
    with Session(engine) as session:
        query = select(Oblig_Hacer).where(Oblig_Hacer.codigo_obligacion == codigo_obligacion)
        return session.exec(query).one_or_none()

def select_obligaciones_by_inspeccion(id_inspeccion: int) -> list[Oblig_Hacer]:
    """Obtiene las obligaciones de hacer asociadas a una inspección específica."""
    engine = connect()
    with Session(engine) as session:
        query = select(Oblig_Hacer).where(Oblig_Hacer.id_inspeccion == id_inspeccion)
        return session.exec(query).all()

def select_obligaciones_by_resultado(resultado: str) -> list[Oblig_Hacer]:
    """Obtiene las obligaciones de hacer filtradas por su resultado."""
    engine = connect()
    with Session(engine) as session:
        query = select(Oblig_Hacer).where(Oblig_Hacer.resultado == resultado)
        obligaciones = session.exec(query).all()
        return obligaciones
    
def select_obligaciones_by_tipo(tipo: str) -> list[Oblig_Hacer]:
    """Obtiene las obligaciones de hacer filtradas por su resultado."""
    engine = connect()
    with Session(engine) as session:
        query = select(Oblig_Hacer).where(Oblig_Hacer.tipo_obligacion == tipo)
        obligaciones = session.exec(query).all()
        return obligaciones



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

        return select_all_obligaciones()


def select_obligaciones_with_time_less_than_15_days() -> list[Oblig_Hacer]:
    """Obtiene todas las obligaciones de hacer con tiempo menor a 15 días."""
    engine = connect()
    with Session(engine) as session:
        query = select(Oblig_Hacer).where(Oblig_Hacer.tiempo < 15)
        obligaciones = session.exec(query).all()
        return obligaciones
    
def obtener_obligaciones_por_categoria_y_fecha(categoria: str) -> list[Oblig_Hacer]:
    """
    Obtiene las obligaciones de hacer de una categoría específica con fecha de vencimiento en los próximos 30 días.
    
    :param categoria: Categoría de la obligación (Producto/Servicio, Higiene, Metrología)
    :return: Lista de obligaciones de hacer que cumplen con los criterios
    """
    engine = connect()
    with Session(engine) as session:
        fecha_actual = datetime.now().date()
        fecha_limite = fecha_actual + timedelta(days=30)
        
        query = (
            select(Oblig_Hacer)
            .where(Oblig_Hacer.categoria == categoria)  # Filtrar por la categoría especificada
            .where(Oblig_Hacer.fecha_venc.between(fecha_actual, fecha_limite))  # Filtrar por fecha de vencimiento
        )
        
        obligaciones = session.exec(query).all()
        return obligaciones
    

def obtener_obligaciones_por_categoria_y_fecha(dias: int) -> dict:
    """
    Obtiene las obligaciones de hacer agrupadas por categoría, con fecha de vencimiento en los próximos 'dias' días.

    :param dias: Número de días desde la fecha actual para filtrar las obligaciones de hacer
    :return: Diccionario con las categorías como claves y listas de obligaciones como valores
    """
    engine = connect()
    with Session(engine) as session:
        fecha_actual = datetime.now().date()
    
    
        
        # Consulta para obtener obligaciones dentro del rango de fechas especificado
        query = (
            select(Oblig_Hacer)
            .where(Oblig_Hacer.fecha_venc.between(fecha_actual, dias), Oblig_Hacer.resultado == "En Espera")
        )
        
        obligaciones = session.exec(query).all()
        
        # Agrupar las obligaciones por categoría
        obligaciones_por_categoria = {
            "Producto o Servicio": [],
            "Higiene": [],
            "Metrologia": []
        }
        
        for obligacion in obligaciones:
            if obligacion.tipo_obligacion in obligaciones_por_categoria:  
                obligaciones_por_categoria[obligacion.tipo_obligacion].append(obligacion)
        
        return obligaciones_por_categoria

def select_obligaciones_by_month_fecha_inicio(month: int, year: int) -> list[Oblig_Hacer]:
    """Obtiene las oblig realizadas en un mes y año específicos."""
    engine = connect()
    with Session(engine) as session:
        start_date = date(year, month, 1)
        end_date = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
        query = select(Oblig_Hacer).where(Oblig_Hacer.fecha_inicio >= start_date, Oblig_Hacer.fecha_inicio < end_date)
        return session.exec(query).all()
    
def select_obligaciones_by_month_fecha_venc(month: int, year: int) -> list[Oblig_Hacer]:
    """Obtiene las oblig realizadas en un mes y año específicos."""
    engine = connect()
    with Session(engine) as session:
        start_date = date(year, month, 1)
        end_date = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
        query = select(Oblig_Hacer).where(Oblig_Hacer.fecha_venc >= start_date, Oblig_Hacer.fecha_inicio < end_date)
        return session.exec(query).all()  

def select_obligaciones_by_month_fecha_comp(month: int, year: int) -> list[Oblig_Hacer]:
    """Obtiene las oblig realizadas en un mes y año específicos."""
    engine = connect()
    with Session(engine) as session:
        start_date = date(year, month, 1)
        end_date = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
        query = select(Oblig_Hacer).where(Oblig_Hacer.fecha_comp >= start_date, Oblig_Hacer.fecha_inicio < end_date)
        return session.exec(query).all()