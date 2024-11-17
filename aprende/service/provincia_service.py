from ..repository.provincia_repository import select_all, create_provincia, select_provincia_by_nombre 
from ..model.all_model import Provincia

def select_all_provincia_service():
    provincia = select_all()
    return provincia

def select_provincia_by_nombre_service(nombre:str):
    if(len(nombre) != 0):
        return select_provincia_by_nombre(nombre)
    else:
        return select_all()
    
    
def create_provincia_service(nombre: str):
    if not nombre:
        raise ValueError("Faltan campos obligatorios")
    
    provincia = select_provincia_by_nombre_service(nombre)
    if(len(provincia) == 0):
        provincia_save = Provincia(
            nombre=nombre)
        return create_provincia(provincia_save)
    else:
        print("La provincia ya existe")
        raise BaseException("La provincia ya existe")