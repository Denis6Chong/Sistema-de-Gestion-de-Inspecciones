from ..repository.establecimiento_repository import (
    select_all,
    select_establecimiento_by_nombre,
    create_establecimiento,
    delete_establecimiento,
    select_establecimientos_by_municipio,
    select_establecimientos_by_entidad,
    select_establecimiento_by_id,
    update_establecimiento,
    select_establecimiento_by_nombre_organismo,
    select_establecimientos_by_nombre_entidad,
    select_establecimiento_by_nombre_provincia
)
from ..model.all_model import Establecimiento

def select_all_establecimientos_service():
    return select_all()

def select_establecimiento_by_nombre_service(nombre: str):
    if len(nombre) != 0:
        return select_establecimiento_by_nombre(nombre)
    else:
        return select_all()

def create_establecimiento_service(id_est, nombre: str, direccion: str, telefono: str, municipio_nombre: str, id_entidad: str):
    if not nombre or not id_entidad:
        raise ValueError("Faltan campos obligatorios")
    
    establecimiento = select_establecimiento_by_nombre_service(nombre)
    if not establecimiento:  # Cambiado para comprobar si es None
        establecimiento_save = Establecimiento(
            id_est=id_est,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            municipio_nombre=municipio_nombre,
            id_entidad=id_entidad,
        )
        return create_establecimiento(establecimiento_save)

    
def delete_establecimiento_service(id_est: int):
    if id_est is None:
        raise ValueError("El ID del establecimiento no puede ser None")
    return delete_establecimiento(id_est)

def select_establecimiento_by_nombre_provincia_service(nombre_provincia: str):
    if not nombre_provincia:
        raise ValueError("El nombre del municipio no puede estar vacío")
    return select_establecimiento_by_nombre_provincia(nombre_provincia)

def select_establecimientos_by_nombre_entidad_service(nombre_entidad: str):
    if not nombre_entidad:
        raise ValueError("El nombre del municipio no puede estar vacío")
    return select_establecimientos_by_nombre_entidad(nombre_entidad)


def select_establecimiento_by_nombre_organismo_service(nombre_organismo: str):
    if not nombre_organismo:
        raise ValueError("El nombre del municipio no puede estar vacío")
    return select_establecimiento_by_nombre_organismo(nombre_organismo)


def select_establecimientos_by_municipio_service(nombre_municipio: str):
    if not nombre_municipio:
        raise ValueError("El nombre del municipio no puede estar vacío")
    return select_establecimientos_by_municipio(nombre_municipio)

def select_establecimientos_by_entidad_service(id_entidad: int):
    if id_entidad is None:
        raise ValueError("El ID de la entidad no puede ser None")
    return select_establecimientos_by_entidad(id_entidad)


def update_establecimiento_service(
                            id_est: int,
                            nombre: str, 
                            direccion: str, 
                            telefono: str,
                            municipio_nombre: str,
                            id_entidad: int,
                            ):
    if not nombre or not id_entidad:
    
        raise ValueError("Faltan datos del Establecimiento")
    establecimiento = select_establecimiento_by_id(id_est)
    establecimiento_save = Establecimiento(
            
            id_est=id_est,
            nombre=nombre, 
            direccion=direccion, 
            telefono=telefono, 
            municipio_nombre=municipio_nombre, 
            id_entidad=id_entidad)
    
    return update_establecimiento(establecimiento_save)