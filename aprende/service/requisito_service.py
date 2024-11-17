from typing import List
from ..model.all_model import Requisito#, Inspeccion, RequisitoInspeccion
from ..repository.requisito_repository import (
    create_requisito,
    delete_requisito,
    select_all,
    select_requisito_by_codigo,
    select_requisito_by_codigo_and_return,
    update_requisito,
    select_requisito_by_titulo,
    select_requisito_by_nombre_norma
    #select_inspecciones_by_requisito,
    #add_requisitos_to_inspeccion,
)
def select_all_requisitos_service():
    """Devuelve todos los requisitos."""
    return select_all()


def select_requisito_by_codigo_requisito_service_and_return(id: int):
    """Devuelve requisitos por su codigo_requisito."""
    if len(id) != 0:
        return select_requisito_by_codigo_and_return(id)
    else:
        return []
    
def select_requisito_by_codigo_requisito_service(id: int):
    """Devuelve requisitos por su codigo_requisito."""
    if len(id) != 0:
        return select_requisito_by_codigo(id)
    else:
        return select_all_requisitos_service()
    

def select_requisito_by_titulo_requisito_service(titulo: str):
    """Devuelve requisitos por su codigo_requisito."""
    if len(titulo) != 0:
        return select_requisito_by_titulo(titulo)
    else:
        return select_all_requisitos_service()
    
    
def create_requisito_service(id: int, titulo: str, codigo_norma:str):
    """Crea un nuevo requisito."""
    if titulo is None or titulo.strip() == "" or codigo_norma is None:
        raise ValueError("Faltan campos obligatorios")
    
    

    requisito = select_requisito_by_codigo_requisito_service_and_return(id)

    
    
    
    if not requisito:  # Cambiado para comprobar si es None o vacío
        nuevo_requisito = Requisito(
            id=id,
            titulo=titulo,
            codigo_norma=codigo_norma
        )
        return create_requisito(nuevo_requisito)
    else:
        print("El codigo ya existe")
        raise BaseException("El requisito ya existe")

def delete_requisito_service(id: int):
    """Elimina un requisito por su número."""
    if id is None:
        raise ValueError("El número del requisito no puede ser None")
    return delete_requisito(id=id)


def update_requisito_service(
                            id: int,
                            titulo: str, 
                            codigo_norma: str
                            ):
    if not titulo or not codigo_norma:
    
        raise ValueError("Faltan datos del Requisito")
    requisito = select_requisito_by_codigo(id)
    requisito_save = Requisito(
            
            id=id,
            titulo=titulo,
            codigo_norma=codigo_norma)
    return update_requisito(requisito_save)


def select_requisito_by_nombre_norma_service(titulo: str):
    if not titulo:
        raise ValueError("El nombre del municipio no puede estar vacío")
    return select_requisito_by_nombre_norma(titulo)

"""def select_inspecciones_for_requisito_service(codigo_requisito_requisito: int):
    #Obtiene todas las inspecciones asociadas a un requisito específico
    return select_inspecciones_by_requisito(codigo_requisito_requisito)

def link_requisitos_to_inspeccion_service(id_inspeccion: int, requisitos: List[int]):
    #Agrega requisitos a una inspección específica
    add_requisitos_to_inspeccion(id_inspeccion, requisitos)"""