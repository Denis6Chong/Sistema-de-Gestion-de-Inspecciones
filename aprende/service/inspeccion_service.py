from ..repository.inspeccion_repository import (
    select_all_inspecciones,
    select_inspeccion_by_codigo,
    select_inspecciones_by_month,
    create_inspeccion_only,
    select_last_inspeccion_by_producto_servicio,
    create_inspeccion,
    update_inspeccion,
    delete_inspeccion,
    select_inspecciones_with_infraccion,
    select_inspecciones_with_infraccion_producto_servicio,
    select_inspecciones_with_infraccion_higiene,
    select_inspecciones_with_infraccion_metrologia,
    select_inspecciones_without_infraccion,
    select_inspecciones_by_inspectores,
    select_inspecciones_by_organismo,
    select_inspeccion_by_producto_servicio,
    select_inspeccion_by_nombre_inspector,
    select_inspecciones_by_nombre_inspector,
    count_inspecciones_by_month_year,
    count_inspecciones_with_infraccion_by_month_year,
    count_inspecciones_without_infraccion_by_month_year,
    select_inspeccion_by_titulo_informe
    
)
from ..repository.establecimiento_repository import (
    select_establecimiento_by_ide

)
from ..repository.municipio_repository import (
    select_municipio_by_nombre
)
from ..repository.provincia_repository import (
    select_provincia_by_nombre
)
from ..model.all_model import Inspeccion
from datetime import datetime, date

def select_all_inspeccion_service():
    """Obtiene todas las inspecciones."""
    return select_all_inspecciones()

def select_inspeccion_by_titulo_informe_service(titulo: str):
    if titulo:
        return select_inspeccion_by_titulo_informe(titulo)
    else:
        return select_all_inspecciones()

def select_inspeccion_by_codigo_service(codigo_inspeccion: str):
    """Obtiene una inspección por su código."""
    if codigo_inspeccion:
        return select_inspeccion_by_codigo(codigo_inspeccion)
    else:
        return select_all_inspecciones()

def select_inspecciones_by_inspector_service(codigo_inspector: str):
    """Obtiene las inspecciones por código de inspector."""
    if codigo_inspector:
        return select_inspeccion_by_nombre_inspector(codigo_inspector)
    else:
        raise ValueError("El código de inspector es requerido")

def select_inspecciones_by_month_service(month: int, year: int):
    """Obtiene las inspecciones realizadas en un mes y año específicos."""
    if 1 <= month <= 12 and year > 0:
        return select_inspecciones_by_month(month, year)
    else:
        raise ValueError("Mes o año inválidos")

def create_inspeccion_service(id_inspeccion,
                            codigo_inspeccion,
                            codigo_real, 
                            prod_o_serv_insp: str, 
                            fecha_inicio: date, 
                            fecha_fin: date,
                            infraccion_p_o_s: int,
                            infraccion_higiene: int,
                            infraccion_metrologia: int,
                            codigo_inspector: str,
                            id_est: int,
                            id_informe: int,
                            numero_lineamiento:int
                            ):

    if not prod_o_serv_insp or not fecha_inicio or not codigo_inspector or not id_est:
        raise ValueError("Faltan datos de la inspección")

    

    # Crear la inspección con el código_real generado
    inspeccion_save = Inspeccion(
        id_inspeccion=id_inspeccion,
        codigo_inspeccion=codigo_inspeccion, 
        prod_o_serv_insp=prod_o_serv_insp, 
        fecha_inicio=fecha_inicio, 
        fecha_fin=fecha_fin, 
        infraccion_p_o_s=infraccion_p_o_s,
        infraccion_higiene=infraccion_higiene, 
        infraccion_metrologia=infraccion_metrologia,
        codigo_inspector=codigo_inspector,
        id_est=id_est, 
        id_informe=id_informe, 
        numero_lineamiento=numero_lineamiento,
        codigo_real=codigo_real
    )

    create_inspeccion_only(inspeccion_save)
    inspeccion = select_last_inspeccion_by_producto_servicio(prod_o_serv_insp)
    return update_inspeccion_other_service(inspeccion)

def update_inspeccion_other_service(inspeccion: Inspeccion):
    # Validación de la inspección
    if not inspeccion.prod_o_serv_insp or not inspeccion.id_inspeccion or not inspeccion.codigo_inspeccion or not inspeccion.fecha_inicio or not inspeccion.codigo_inspector or not inspeccion.id_est:
        raise ValueError("Faltan datos de la inspección")

    # Obtener la inspección por el código
    inspeccionn = select_inspeccion_by_codigo_service(inspeccion.codigo_inspeccion)

    # No es necesario convertir fecha_inicio si ya es un objeto 'date'
    # La validación de fecha_inicio debería hacerse solo si es necesario
    if isinstance(inspeccion.fecha_inicio, str):
        inspeccion.fecha_inicio = datetime.strptime(inspeccion.fecha_inicio, "%Y-%m-%d").date()

    # Obtener el establecimiento y validarlo
    establecimiento_list = select_establecimiento_by_ide(inspeccion.id_est)
    if not establecimiento_list:
        raise ValueError(f"No se encontró ningún establecimiento con id_est={inspeccion.id_est}")

    # Obtener el municipio y validarlo
    municipio = select_municipio_by_nombre(establecimiento_list[0].municipio_nombre)[0]
    if not municipio:
        raise ValueError(f"No se encontró ningún municipio con nombre={establecimiento_list[0].municipio_nombre}")

    # Obtener la provincia y validarla
    provincia = select_provincia_by_nombre(municipio.nombre_provincia)[0]
    if not provincia:
        raise ValueError(f"No se encontró ninguna provincia con nombre={municipio.nombre_provincia}")

    # Generar las iniciales de la provincia
    iniciales_provincia = {
        "Villa Clara": "VC",
        "Cienfuegos": "CF",
        "Sancti Spíritus": "SS",
        "Matanzas": "MT",
        "Ciego de Avila": "CA"
    }.get(provincia.nombre, "XX")  # Valor por defecto "XX" si no se encuentra la provincia

    anio_actual = inspeccion.fecha_inicio.year % 100  # Obtener los dos últimos dígitos del año

    # Generar el código real
    codigo_real = f"{iniciales_provincia} {inspeccion.numero_lineamiento}.{inspeccion.id_inspeccion}.{anio_actual}"

    # Crear una nueva instancia de inspección con los datos actualizados
    inspeccion_save = Inspeccion(
        id_inspeccion=inspeccion.id_inspeccion,
        codigo_inspeccion=inspeccion.codigo_inspeccion, 
        prod_o_serv_insp=inspeccion.prod_o_serv_insp, 
        fecha_inicio=inspeccion.fecha_inicio, 
        fecha_fin=inspeccion.fecha_fin, 
        infraccion_p_o_s=inspeccion.infraccion_p_o_s or 0, 
        infraccion_higiene=inspeccion.infraccion_higiene or 0, 
        infraccion_metrologia=inspeccion.infraccion_metrologia or 0,
        codigo_inspector=inspeccion.codigo_inspector, 
        id_est=inspeccion.id_est, 
        id_informe=inspeccion.id_informe, 
        numero_lineamiento=inspeccion.numero_lineamiento,
        codigo_real=codigo_real
    )

    # Actualizar la inspección
    return update_inspeccion(inspeccion_save)   

def update_inspeccion_service(
                            id_inspeccion: int,
                            codigo_inspeccion: str,
                            codigo_real: str, 
                            prod_o_serv_insp: str, 
                            fecha_inicio, 
                            fecha_fin,
                            infraccion_p_o_s: int,
                            infraccion_higiene: int,
                            infraccion_metrologia: int,
                            codigo_inspector: str,
                            id_est: int,
                            id_informe: int,
                            numero_lineamiento:int
                            ):
    if not prod_o_serv_insp or not id_inspeccion or not codigo_inspeccion or not fecha_inicio  or not codigo_inspector or not id_est:
    
        raise ValueError("Faltan datos de la inspección")
    inspeccion = select_inspeccion_by_codigo_service(codigo_inspeccion)

    # Convertir fechas a objetos de tipo date si son cadenas
    if isinstance(fecha_inicio, str):
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()

    # Obtener el establecimiento y validar
    establecimiento_list = select_establecimiento_by_ide(id_est)
    if not establecimiento_list or len(establecimiento_list) == 0:
        raise ValueError(f"No se encontró ningún establecimiento con id_est={id_est}")
    
    # Seleccionar el primer elemento de la lista
    establecimiento = establecimiento_list[0]
    print(establecimiento)

    # Obtener el municipio
    municipio = select_municipio_by_nombre(establecimiento.municipio_nombre)[0]
    if not municipio:
        raise ValueError(f"No se encontró ningún municipio con nombre={establecimiento.municipio_nombre}")
    print(municipio)

    # Obtener la provincia
    provincia = select_provincia_by_nombre(municipio.nombre_provincia)[0]
    if not provincia:
        raise ValueError(f"No se encontró ninguna provincia con nombre={municipio.nombre_provincia}")
    print(provincia)

    # Generar las iniciales de la provincia
    iniciales_provincia = {
        "Villa Clara": "VC",
        "Cienfuegos": "CF",
        "Santi Spíritus": "SS",
        "Matanzas": "MT",
        "Ciego de Avila": "CA"
    }.get(provincia.nombre, "XX")  # Valor por defecto "XX" si no se encuentra la provincia

    anio_actual = fecha_inicio.year % 100  # Obtener los dos últimos dígitos del año

    codigo_real = f"{iniciales_provincia} {numero_lineamiento}.{id_inspeccion}.{anio_actual}"

    


    
    inspeccion_save = Inspeccion(
            
            id_inspeccion=id_inspeccion,
            codigo_inspeccion=codigo_inspeccion, 
            prod_o_serv_insp=prod_o_serv_insp, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin, 
            infraccion_p_o_s=infraccion_p_o_s if infraccion_p_o_s is not None else 0, 
            infraccion_higiene=infraccion_higiene if infraccion_higiene is not None else 0, 
            infraccion_metrologia=infraccion_metrologia if infraccion_metrologia is not None else 0,
            codigo_inspector=codigo_inspector, 
            id_est=id_est, 
            id_informe=id_informe, 
            numero_lineamiento=numero_lineamiento,
            codigo_real=codigo_real)
    print("ESTO ES DEL SERVICIO", inspeccion_save)
    return update_inspeccion(inspeccion_save)
        

def delete_inspeccion_service(codigo_inspeccion: str):
    """Elimina una inspección."""
    if codigo_inspeccion:
        return delete_inspeccion(codigo_inspeccion)
    else:
        raise ValueError("El código de inspección es requerido")

def select_inspecciones_with_infraccion_service():
    """Obtiene todas las inspecciones donde hubo alguna infracción."""
    return select_inspecciones_with_infraccion()

def select_inspecciones_with_infraccion_producto_servicio_service():
    """Obtiene todas las inspecciones donde hubo infracción de tipo Producto o Servicio."""
    return select_inspecciones_with_infraccion_producto_servicio()

def select_inspecciones_with_infraccion_higiene_service():
    """Obtiene todas las inspecciones donde hubo infracción de tipo Higiene."""
    return select_inspecciones_with_infraccion_higiene()

def select_inspecciones_with_infraccion_metrologia_service():
    """Obtiene todas las inspecciones donde hubo infracción de tipo Metrología."""
    return select_inspecciones_with_infraccion_metrologia()

def select_inspecciones_without_infraccion_service():
    """Obtiene todas las inspecciones donde no hubo ninguna infracción."""
    return select_inspecciones_without_infraccion()

def select_inspecciones_by_organismo_service(nombre_organismo: str):
    """Obtiene las inspecciones por código de organismo."""
    if nombre_organismo:
        return select_inspecciones_by_organismo(nombre_organismo)
    else:
        raise ValueError("El código de organismo es requerido")
    
    
    
def select_inspecciones_by_nombre_inspector_service(inspector_nombre: str):
    """Obtiene las inspecciones por código de organismo."""
    if inspector_nombre:
        return select_inspecciones_by_nombre_inspector(inspector_nombre)
    else:
        raise ValueError("El nombre de inspector es requerido")

    
    
def select_inspeccion_by_producto_servicio_service(producto_servicio: str):
    if producto_servicio:
        return select_inspeccion_by_producto_servicio(producto_servicio)
    else:
        return select_all_inspecciones()



def count_inspecciones_by_month_year_service(month: int, year: int) -> int:
    """Servicio que devuelve la cantidad de inspecciones realizadas en un mes y año específicos."""
    if 1 <= month <= 12 and year > 0:
        return count_inspecciones_by_month_year(month, year)
    else:
        raise ValueError("Mes o año inválidos")

def count_inspecciones_without_infraccion_by_month_year_service(month: int, year: int) -> int:
    """Servicio que devuelve la cantidad de inspecciones sin infracciones en un mes y año específicos."""
    if 1 <= month <= 12 and year > 0:
        return count_inspecciones_without_infraccion_by_month_year(month, year)
    else:
        raise ValueError("Mes o año inválidos")

def count_inspecciones_with_infraccion_by_month_year_service(month: int, year: int) -> int:
    """Servicio que devuelve la cantidad de inspecciones con infracciones en un mes y año específicos."""
    if 1 <= month <= 12 and year > 0:
        return count_inspecciones_with_infraccion_by_month_year(month, year)
    else:
        raise ValueError("Mes o año inválidos")