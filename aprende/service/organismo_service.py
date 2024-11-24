from ..repository.organismo_repository import delete_organismo, update_organismo,select_organismo_by_id, select_all, create_organismo, select_organismo_by_nombre 
from ..model.all_model import Organismo

def select_all_organismo_service():
    organismo = select_all()
    
    return organismo

def select_organismo_by_nombre_service(nombre:str):
    if(len(nombre) != 0):
        return select_organismo_by_nombre(nombre)
    else:
        return select_all()
    
    
def create_organismo_service(id_organismo: int, nombre: str, siglas: str, direccion: str, telefono: str):
    if not nombre:
        raise ValueError("Faltan campos obligatorios")
    
    organismo = select_organismo_by_nombre_service(nombre)
    if(len(organismo) == 0):
        organismo_save = Organismo(
            id_organismo=id_organismo,
            nombre=nombre,
            siglas=siglas,
            direccion=direccion,
            telefono=telefono,

            )
        return create_organismo(organismo_save)
    else:
        print("La organismo ya existe")
        raise BaseException("La organismo ya existe")
    

def update_organismo_service(
                            id_organismo: int,
                            nombre: str, 
                            direccion: str, 
                            telefono: str,
                            siglas: str,
                            ):
    if not nombre:
    
        raise ValueError("Faltan datos del Organismo")
    organismo = select_organismo_by_id(id_organismo)
    organismo_save = Organismo(
            
            id_organismo=id_organismo,
            nombre=nombre, 
            siglas=siglas, 
            telefono=telefono, 
            direccion=direccion)
    
    return update_organismo(organismo_save)

def delete_organismo_service(id_organismo: int):
    """Elimina un organismo por su número."""
    if id_organismo is None:
        raise ValueError("El número del organismo no puede ser None")
    return delete_organismo(id_organismo=id_organismo)
