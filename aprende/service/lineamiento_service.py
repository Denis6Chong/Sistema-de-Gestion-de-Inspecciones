from typing import List
from ..model.all_model import Lineamiento#, Inspeccion, LineamientoInspeccion
from ..repository.lineamiento_repository import (
    create_lineamiento,
    delete_lineamiento,
    select_all,
    select_lineamiento_by_numero,
    #select_inspecciones_by_lineamiento,
    #add_lineamientos_to_inspeccion,
)
def select_all_lineamientos_service():
    """Devuelve todos los lineamientos."""
    return select_all()

def select_lineamiento_by_numero_service(numero: int):
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

"""def select_inspecciones_for_lineamiento_service(numero_lineamiento: int):
    #Obtiene todas las inspecciones asociadas a un lineamiento específico
    return select_inspecciones_by_lineamiento(numero_lineamiento)

def link_lineamientos_to_inspeccion_service(id_inspeccion: int, lineamientos: List[int]):
    #Agrega lineamientos a una inspección específica
    add_lineamientos_to_inspeccion(id_inspeccion, lineamientos)"""