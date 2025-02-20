from ..repository.municipio_repository import select_all, create_municipio, select_municipio_by_nombre 
from ..model.all_model import Municipio

def select_all_municipio_service():
    municipio = select_all()
    print(municipio)
    return municipio

def select_municipio_by_nombre_service(nombre:str):
    if(len(nombre) != 0):
        return select_municipio_by_nombre(nombre)
    else:
        return select_all()
    
    
def create_municipio_service(nombre: str, nombre_provincia: str):
    if not nombre or not nombre_provincia:
        raise ValueError("Faltan campos obligatorios")
    
    municipio = select_municipio_by_nombre_service(nombre)
    if(len(municipio) == 0):
        municipio_save = Municipio(
            nombre=nombre,
            nombre_provincia=nombre_provincia)
        return create_municipio(municipio_save)
    else:
        print("La municipio ya existe")
        raise BaseException("La municipio ya existe")
    