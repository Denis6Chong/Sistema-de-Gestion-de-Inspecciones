from ..model.all_model import Organismo
from .connect_db import connect
from sqlmodel import Session, select


def select_all():
    engine = connect()
    with Session(engine) as session:
        query = select(Organismo)
        return session.exec(query).all()
    
def create_organismo(organismo: Organismo):
    engine = connect()
    with Session(engine) as session:
        session.add(organismo)
        session.commit()
        return select_all() 
    

def select_organismo_by_nombre(nombre: str):
    engine = connect()
    with Session(engine) as session:
        query = select(Organismo).where(Organismo.nombre == nombre)
        return session.exec(query).all()    
    
def select_organismo_by_id(id_organismo: str):
    engine = connect()
    with Session(engine) as session:
        query = select(Organismo).where(Organismo.id_organismo == id_organismo)
        return session.exec(query).all() 
    

def update_organismo(organismo: Organismo) -> list[Organismo]:
    engine = connect()
    with Session(engine) as session:
        existing_organismo = session.get(Organismo, organismo.id_est)
        print(existing_organismo)
        if existing_organismo:
            existing_organismo.id_organismo = organismo.id_organismo
            existing_organismo.nombre = organismo.nombre
            existing_organismo.telefono = organismo.telefono
            existing_organismo.direccion = organismo.direccion
            existing_organismo.siglas = organismo.siglas
            session.commit()
        print("Organismo no encontrada con el código proporcionado")
            # Refrescar el objeto existente para asegurarse de que está actualizado
        session.refresh(existing_organismo)
        return select_all()