from ..repository.entidad_repository import delete_entidad,select_entidad_by_nombre_organismo, update_entidad, select_all, create_entidad, select_entidad_by_nombre, get_nombre_organismo_by_entidad_nombre, get_organismo_by_entidad_nombre 
from ..model.all_model import Entidad, Organismo
from sqlalchemy.orm import joinedload
from ..repository.entidad_repository import connect
from sqlmodel import Session, select

def select_all_entidad_service():
    engine = connect()
    with Session(engine) as session:
        # Usamos joinedload para cargar la relación 'organismo_relation' de forma anticipada
        query = select(Entidad).options(joinedload(Entidad.organismo_relation))
        entidades = session.exec(query).all()

        for entidad in entidades:
            if entidad.organismo_relation:
                print(f"Entidad: {entidad.nombre}, Organismo: {entidad.organismo_relation.nombre}")
            else:
                print(f"Entidad: {entidad.nombre}, Organismo: N/A")
        return entidades
    

def select_entidad_by_nombre_service(nombre:str):
    if(len(nombre) != 0):
        return select_entidad_by_nombre(nombre)
    else:
        return select_all()
    
    
def create_entidad_service(id_entidad: int, nombre: str, siglas: str, id_organismo: int):
    if not nombre:
        raise ValueError("Faltan campos obligatorios")
    
    entidad = select_entidad_by_nombre_service(nombre)
    if(len(entidad) == 0):
        entidad_save = Entidad(
            id_entidad=id_entidad,
            nombre=nombre,
            siglas=siglas,
            id_organismo=id_organismo

            )
        return create_entidad(entidad_save)
    else:
        print("La entidad ya existe")
        raise BaseException("La entidad ya existe")
    

def get_nombre_organismo_by_entidad_nombre_service(nombre: str):
    if not nombre:
        raise ValueError("El nombre de la entidad no puede estar vacío")
    
    # Utilizar el método del repositorio para obtener el nombre del organismo
    nombre_organismo = get_nombre_organismo_by_entidad_nombre(nombre)
    
    if nombre_organismo:
        return nombre_organismo
    else:
        raise ValueError(f"No se encontró el organismo para la entidad con nombre: {nombre}")

def get_organismo_by_entidad_nombre_service(nombre: str):
    if not nombre:
        raise ValueError("El nombre de la entidad no puede estar vacío")
    
    # Utilizar el método del repositorio para obtener los datos del organismo
    organismo = get_organismo_by_entidad_nombre(nombre)
    
    if organismo:
        return organismo
    else:
        raise ValueError(f"No se encontró el organismo para la entidad con nombre: {nombre}")
    
def update_entidad_service(
                            id_entidad: int,
                            nombre: str, 
                            siglas: str, 
                            id_organismo: str
                            ):
    if not id_organismo or not nombre:
    
        raise ValueError("Faltan datos de la Entidad")
    
    entidad_save = Entidad(
            
            id_entidad=id_entidad,
            nombre=nombre, 
            siglas=siglas, 
            id_organismo=id_organismo)
    
    return update_entidad(entidad_save)

def select_entidad_by_nombre_organismo_service(nombre_organismo: str):
    if not nombre_organismo:
        raise ValueError("El nombre del municipio no puede estar vacío")
    return select_entidad_by_nombre_organismo(nombre_organismo)

def delete_entidad_service(id_est: int):
    if id_est is None:
        raise ValueError("El ID del entidad no puede ser None")
    return delete_entidad(id_est)