from typing import List
from ..model.all_model import Norma#, Inspeccion, NormaInspeccion
from ..repository.norma_repository import (
    create_norma,
    delete_norma,
    select_all,
    select_norma_by_codigo,
    select_norma_by_codigo_and_return,
    update_norma
    #select_inspecciones_by_norma,
    #add_normas_to_inspeccion,
)
def select_all_normas_service():
    """Devuelve todos los normas."""
    return select_all()


def select_norma_by_codigo_norma_service_and_return(codigo_norma: str):
    """Devuelve normas por su codigo_norma."""
    if len(codigo_norma) != 0:
        return select_norma_by_codigo_and_return(codigo_norma)
    else:
        return select_all_normas_service()
    
def select_norma_by_codigo_norma_service(codigo_norma: str):
    """Devuelve normas por su codigo_norma."""
    if len(codigo_norma) != 0:
        return select_norma_by_codigo(codigo_norma)
    else:
        return select_all_normas_service()
    
def create_norma_service(codigo_norma: str, titulo: str):
    """Crea un nuevo norma."""
    if codigo_norma is None or titulo is None or titulo.strip() == "":
        raise ValueError("El número y el título no pueden estar vacíos")
    
    

    norma = select_norma_by_codigo_norma_service_and_return(codigo_norma)

    
    
    
    if not norma:  # Cambiado para comprobar si es None o vacío
        nuevo_norma = Norma(
            codigo_norma=codigo_norma,
            titulo=titulo,
        )
        return create_norma(nuevo_norma)
    else:
        print("El codigo ya existe")
        raise BaseException("El norma ya existe")

def delete_norma_service(codigo_norma: str):
    """Elimina un norma por su número."""
    if codigo_norma is None:
        raise ValueError("El número del norma no puede ser None")
    return delete_norma(codigo_norma=codigo_norma)

def update_norma_service(
                            codigo_norma: int,
                            titulo: str, 
                            ):
    if not titulo:
    
        raise ValueError("Faltan datos del Norma")
    norma = select_norma_by_codigo(codigo_norma)
    norma_save = Norma(
            
            codigo_norma=codigo_norma,
            titulo=titulo)
    return update_norma(norma_save)

"""def select_inspecciones_for_norma_service(codigo_norma_norma: int):
    #Obtiene todas las inspecciones asociadas a un norma específico
    return select_inspecciones_by_norma(codigo_norma_norma)

def link_normas_to_inspeccion_service(id_inspeccion: int, normas: List[int]):
    #Agrega normas a una inspección específica
    add_normas_to_inspeccion(id_inspeccion, normas)"""