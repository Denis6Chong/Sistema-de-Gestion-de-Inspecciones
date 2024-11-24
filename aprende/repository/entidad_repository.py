from ..model.all_model import Entidad, Organismo
from .connect_db import connect
from sqlmodel import Session, select


def select_all():
    engine = connect()
    with Session(engine) as session:
        query = select(Entidad)
        return session.exec(query).all()
    
def create_entidad(entidad: Entidad):
    engine = connect()
    with Session(engine) as session:
        session.add(entidad)
        session.commit()
        return select_all() 

def select_entidad_by_nombre(nombre: str):
    engine = connect()
    with Session(engine) as session:
        query = select(Entidad).where(Entidad.nombre == nombre)
        return session.exec(query).all()    
    

def get_organismo_by_entidad_nombre(nombre: str):
    engine = connect()
    with Session(engine) as session:
        # Buscar la entidad por su nombre
        entidad = session.exec(select(Entidad).where(Entidad.nombre == nombre)).first()
        
        # Verificar si la entidad existe y tiene un organismo relacionado
        if entidad and entidad.organismo_relation:
            return entidad.organismo_relation
        
        # Si no se encuentra la entidad o no tiene organismo relacionado, devolver None
        return None

def get_nombre_organismo_by_entidad_nombre(nombre: str):
    engine = connect()
    with Session(engine) as session:
        # Buscar la entidad por su nombre
        entidad = session.exec(select(Entidad).where(Entidad.nombre == nombre)).first()
        
        # Verificar si la entidad existe y tiene un organismo relacionado
        if entidad and entidad.organismo_relation:
            return entidad.organismo_relation.nombre
        
        # Si no se encuentra la entidad o no tiene organismo relacionado, devolver None
        return None
    
def select_entidad_by_nombre_organismo(nombre_organismo: str):
    
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Entidad)
            .join(Organismo)  
            .where(Organismo.nombre.ilike(f"{nombre_organismo}"))
        )
        return session.exec(query).all()
    

def update_entidad(entidad: Entidad) -> list[Entidad]:
    engine = connect()
    with Session(engine) as session:
        existing_entidad = session.get(Entidad, entidad.id_entidad)
        print(existing_entidad)
        if existing_entidad:
            existing_entidad.nombre = entidad.nombre
            existing_entidad.siglas = entidad.siglas
            existing_entidad.id_organismo = entidad.id_organismo
            session.commit()
        print("Entidad no encontrada con el id proporcionado")
            # Refrescar el objeto existente para asegurarse de que está actualizado
        session.refresh(existing_entidad)
        return select_all()
    

def delete_entidad(id_est: int):
    engine = connect()
    with Session(engine) as session:
        query = select(Entidad).where(Entidad.id_est == id_est)
        entidad_delete = session.exec(query).one()
        session.delete(entidad_delete)
        session.commit()
        return select_all()