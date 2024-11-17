from ..repository.oblig_hacer_repository import (
    select_all_obligaciones,
    select_obligacion_by_codigo,
    select_obligaciones_by_inspeccion,
    update_obligacion_hacer,
    select_obligaciones_by_resultado,
    select_obligaciones_with_time_less_than_15_days,
    obtener_obligaciones_por_categoria_y_fecha,
    select_obligaciones_by_tipo,
    select_obligaciones_by_month_fecha_inicio,
    select_obligaciones_by_month_fecha_comp,
    select_obligaciones_by_month_fecha_venc
)
from dateutil.relativedelta import relativedelta
from ..model.all_model import Oblig_Hacer
from datetime import date, datetime

def select_all_oblig_hacer_service() -> list[Oblig_Hacer]:
    """Obtiene todas las obligaciones de hacer."""
    return select_all_obligaciones()

def get_obligacion_by_codigo_service(codigo_obligacion: str) -> Oblig_Hacer:
    """Obtiene una obligación de hacer por su código."""
    return select_obligacion_by_codigo(codigo_obligacion)

def get_obligaciones_by_inspeccion_service(id_inspeccion: int) -> list[Oblig_Hacer]:
    """Obtiene todas las obligaciones asociadas a una inspección específica."""
    if id_inspeccion:
        return select_obligaciones_by_inspeccion(id_inspeccion)
    else:
        raise ValueError("El ID de inspeccion es requerido")
    
def get_obligaciones_by_tipo(tipo: str) -> list[Oblig_Hacer]:
    """Obtiene todas las obligaciones asociadas a una inspección específica."""
    if tipo:

        return select_obligaciones_by_tipo(tipo)
    else:
        raise ValueError("El ID de inspeccion es requerido")

def update_obligacion_service(codigo_obligacion: str, fecha_venc: date = None, fecha_comp: date = None, resultado: str = None, multa: float=None, codigo_norma: str = None) -> Oblig_Hacer:
    """Actualiza una obligación de hacer."""
    return update_obligacion_hacer(codigo_obligacion, fecha_venc, fecha_comp, resultado, multa, codigo_norma)


def get_obligaciones_by_resultado_service(resultado: str) -> list[Oblig_Hacer]:
    """Obtiene las obligaciones de hacer filtradas por su resultado."""
    return select_obligaciones_by_resultado(resultado)

def select_obligaciones_with_time_less_than_15_days_service() -> list[Oblig_Hacer]:
    """Obtiene las obligaciones de hacer filtradas por su resultado."""
    return select_obligaciones_with_time_less_than_15_days()

def obtener_obligaciones_por_categoria_y_fecha_service(dias: int):
    """
    Obtiene las obligaciones de hacer agrupadas por categoría, con fecha de vencimiento en los próximos 'dias' días.

    :param dias: Número de días desde la fecha actual para filtrar las obligaciones de hacer.
    :return: Diccionario con categorías como claves y listas de obligaciones como valores.
    """
    return obtener_obligaciones_por_categoria_y_fecha(dias)

def cant_obligaciones_en_espera(anterior=False) -> int:
    # Obtener todas las obligaciones en "En Espera"
    en_espera = select_obligaciones_by_resultado("En Espera")
    
    # Filtrar las obligaciones para el mes especificado
    if not anterior:
        obligaciones_en_mes = [
            obligacion for obligacion in en_espera 
            if obligacion.fecha_venc is not None and obligacion.fecha_venc.month == datetime.now().month and obligacion.fecha_venc.year == datetime.now().year
        ]
    else:
        obligaciones_en_mes = [
            obligacion for obligacion in en_espera 
            if obligacion.fecha_venc is not None and obligacion.fecha_venc.month == (datetime.now().month-1) and obligacion.fecha_venc.year == datetime.now().year
        ]
    # Retornar la cantidad de obligaciones en espera para el mes dado
    return len(obligaciones_en_mes)


def cant_obligaciones_falta_datos() -> int:
    # Obtener todas las obligaciones
    obligaciones = select_all_obligaciones()
    
    
    obligaciones_falta_datos = [
            obligacion for obligacion in obligaciones
            if (obligacion.fecha_venc is None or obligacion.fecha_comp is None or 
                (obligacion.resultado == "No Cumplida" and obligacion.multa is None))
        ]
    
        
    # Retornar la cantidad de obligaciones con datos faltantes
    return len(obligaciones_falta_datos)

def obligaciones_falta_datos() -> list[Oblig_Hacer]:
    # Obtener todas las obligaciones
    obligaciones = select_all_obligaciones()
    
    
    obligaciones_falta_datos = [
            obligacion for obligacion in obligaciones
            if (obligacion.fecha_venc is None or obligacion.fecha_comp is None or 
                (obligacion.resultado == "No Cumplida" and obligacion.multa is None))
        ]
    
        
    # Retornar la cantidad de obligaciones con datos faltantes
    return (obligaciones_falta_datos)


def cant_obligaciones_no_cumplidas(anterior=True) -> int:
    # Obtener las obligaciones que no han sido cumplidas
    no_cumplidas = select_obligaciones_by_resultado("No Cumplida")
    # Obtener la fecha actual y determinar el trimestre
    fecha_actual = datetime.now()
    
    if anterior:
        fecha_actual -= relativedelta(months=3)
    mes_actual = fecha_actual.month

    # Determinar el rango de fechas para el trimestre actual
    if mes_actual in [1, 2, 3]:
        inicio_trimestre = datetime(fecha_actual.year, 1, 1)
        fin_trimestre = datetime(fecha_actual.year, 3, 31)
    elif mes_actual in [4, 5, 6]:
        inicio_trimestre = datetime(fecha_actual.year, 4, 1)
        fin_trimestre = datetime(fecha_actual.year, 6, 30)
    elif mes_actual in [7, 8, 9]:
        inicio_trimestre = datetime(fecha_actual.year, 7, 1)
        fin_trimestre = datetime(fecha_actual.year, 9, 30)
    else:  # Meses de octubre, noviembre y diciembre
        inicio_trimestre = datetime(fecha_actual.year, 10, 1)
        fin_trimestre = datetime(fecha_actual.year, 12, 31)

    inicio_trimestre = inicio_trimestre.date()
    fin_trimestre = fin_trimestre.date()
    # Filtrar las obligaciones no cumplidas que están en el trimestre actual
    
    no_cumplidas_en_trimestre = [
        obligacion for obligacion in no_cumplidas
        if obligacion.fecha_venc is not None and  # Asegúrate de que fecha_venc no sea None
        inicio_trimestre <= obligacion.fecha_venc <= fin_trimestre
    ]
    
    # Retornar la cantidad de obligaciones no cumplidas en el trimestre
    return len(no_cumplidas_en_trimestre)

def select_obligaciones_by_month_service(tipo_fecha: str, month: int, year: int):
    
    if tipo_fecha:
        if tipo_fecha == "Fecha Inicio":
            if 1 <= month <= 12 and year > 0:
                return select_obligaciones_by_month_fecha_inicio(month, year)
            else:
                raise ValueError("Mes o año inválidos")

        if tipo_fecha == "Fecha Vencimiento":
            if 1 <= month <= 12 and year > 0:
                return select_obligaciones_by_month_fecha_venc(month, year)
            else:
                raise ValueError("Mes o año inválidos")
        else:
            if 1 <= month <= 12 and year > 0:
                return select_obligaciones_by_month_fecha_comp(month, year)
            else:
                raise ValueError("Mes o año inválidos")
    else:
        raise ValueError("Tipo de Fecha necesario")           