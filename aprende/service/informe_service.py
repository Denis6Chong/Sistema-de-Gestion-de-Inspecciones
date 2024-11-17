from typing import List
from ..model.all_model import Informe#, Inspeccion, InformeInspeccion
from datetime import date
from ..repository.informe_repository import (
    create_informe,
    delete_informe,
    select_all,
    select_informe_by_codigo,
    select_informe_by_codigo_and_return,
    update_informe,
    select_informe_by_month,
    select_informe_by_titulo
    #select_inspecciones_by_informe,
    #add_informes_to_inspeccion,
)
def select_all_informes_service():
    """Devuelve todos los informes."""
    return select_all()


def select_informe_by_codigo_informe_service_and_return(id_informe: int):
    """Devuelve informes por su codigo_informe."""
    if len(id_informe) != 0:
        return select_informe_by_codigo_and_return(id_informe)
    else:
        return []
    
def select_informe_by_codigo_informe_service(id_informe: int):
    """Devuelve informes por su codigo_informe."""
    if len(id_informe) != 0:
        return select_informe_by_codigo(id_informe)
    else:
        return select_all_informes_service()
    
def select_informe_by_titulo_service(titulo: str):
    """Devuelve informes por su codigo_informe."""
    if len(titulo) != 0:
        return select_informe_by_titulo(titulo)
    else:
        return select_all_informes_service()
    
def create_informe_service(id_informe: str, titulo: str, fecha:date, conclusiones: str, conforme: int ):
    """Crea un nuevo informe."""
    if not titulo:
        raise ValueError("El título no puede estar vacíos")
    
    

    informe = select_informe_by_codigo_informe_service_and_return(id_informe)

    
    
    
    if not informe:  # Cambiado para comprobar si es None o vacío
        nuevo_informe = Informe(
            id_informe=id_informe,
            titulo=titulo,
            fecha=fecha,
            conclusiones=conclusiones,
            conforme = conforme

        )
        return create_informe(nuevo_informe)
    else:
        print("El codigo ya existe")
        raise BaseException("El informe ya existe")

def delete_informe_service(id_informe: int):
    """Elimina un informe por su número."""
    if id_informe is None:
        raise ValueError("El número del informe no puede ser None")
    return delete_informe(id_informe=id_informe)


def update_informe_service(
                            id_informe: str, titulo: str, fecha:date, conclusiones: str, conforme: int 
                            ):
    if not titulo:
    
        raise ValueError("Faltan datos de la inspección")
    informe = select_informe_by_codigo_informe_service_and_return(id_informe)

    


    
    inspeccion_save = Informe(
            
            id_informe=id_informe,
            titulo=titulo,
            fecha=fecha, 
            conclusiones=conclusiones, 
            conforme=conforme if conforme is not None else 0, 
    )
    return update_informe(inspeccion_save)



def select_informe_by_month_service(month: int, year: int):
    """Obtiene las inspecciones realizadas en un mes y año específicos."""
    if 1 <= month <= 12 and year > 0:
        return select_informe_by_month(month, year)
    else:
        raise ValueError("Mes o año inválidos")
    

"""def select_inspecciones_for_informe_service(codigo_informe_informe: int):
    #Obtiene todas las inspecciones asociadas a un informe específico
    return select_inspecciones_by_informe(codigo_informe_informe)

def link_informes_to_inspeccion_service(id_inspeccion: int, informes: List[int]):
    #Agrega informes a una inspección específica
    add_informes_to_inspeccion(id_inspeccion, informes)"""