from typing import List
from ..model.all_model import Lineamiento#, Inspeccion, LineamientoInspeccion
from ..repository.lineamiento_repository import (
    create_lineamiento,
    delete_lineamiento,
    select_all,
    select_lineamiento_by_numero,
    update_lineamiento,
    select_lineamiento_by_titulo
    #select_inspecciones_by_lineamiento,
    #add_lineamientos_to_inspeccion,
)
def select_all_lineamientos_service():
    """Devuelve todos los lineamientos."""
    return select_all()
def select_lineamiento_by_titulo_service(titulo: str):
    """Devuelve lineamientos por su numero."""
    if len(titulo) != 0:
        return select_lineamiento_by_titulo(titulo)
    else:
        return select_all_lineamientos_service()

def select_lineamiento_by_numero_service(numero: str):
    """Devuelve lineamientos por su numero."""
    if len(numero) != 0:
        return select_lineamiento_by_numero(numero)
    else:
        return select_all_lineamientos_service()
def create_lineamiento_service(numero: int, titulo: str):
    """Crea un nuevo lineamiento."""
    if numero is None or titulo is None or titulo.strip() == "":
        raise ValueError("El número y el título no pueden estar vacíos")

    lineamiento = select_lineamiento_by_numero_service(titulo)
    if not lineamiento:  # Cambiado para comprobar si es None o vacío
        nuevo_lineamiento = Lineamiento(
            numero=numero,
            titulo=titulo,
        )
        return create_lineamiento(nuevo_lineamiento)
    else:
        print("El lineamiento ya existe")
        raise BaseException("El lineamiento ya existe")

def delete_lineamiento_service(numero: int):
    """Elimina un lineamiento por su número."""
    if numero is None:
        raise ValueError("El número del lineamiento no puede ser None")
    return delete_lineamiento(numero=numero)

def delete_lineamiento_service(numero: int):
    """Elimina un lineamiento por su número."""
    if numero is None:
        raise ValueError("El número del lineamiento no puede ser None")
    return delete_lineamiento(numero)


def update_lineamiento_service(
                            numero: int, titulo: str 
                            ):
    if not titulo or not numero:
    
        raise ValueError("Faltan datos del lineamiento")
    

    


    
    inspeccion_save = Lineamiento(
            
            numero=numero,
            titulo=titulo,
            
    )
    return update_lineamiento(inspeccion_save)



"""def select_inspecciones_for_lineamiento_service(numero_lineamiento: int):
    #Obtiene todas las inspecciones asociadas a un lineamiento específico
    return select_inspecciones_by_lineamiento(numero_lineamiento)

def link_lineamientos_to_inspeccion_service(id_inspeccion: int, lineamientos: List[int]):
    #Agrega lineamientos a una inspección específica
    add_lineamientos_to_inspeccion(id_inspeccion, lineamientos)"""