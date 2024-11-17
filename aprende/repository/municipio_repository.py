from ..model.all_model import Municipio
from .connect_db import connect
from sqlmodel import Session, select


def select_all():
    engine = connect()
    with Session(engine) as session:
        query = select(Municipio)
        return session.exec(query).all()
    
def create_municipio(municipio: Municipio):
    engine = connect()
    with Session(engine) as session:
        session.add(municipio)
        session.commit()
        return select_all() 
    

def select_municipio_by_nombre(nombre: str):
    engine = connect()
    with Session(engine) as session:
        query = select(Municipio).where(Municipio.nombre == nombre)
        return session.exec(query).all()    
    

