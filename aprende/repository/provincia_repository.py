from ..model.all_model import Provincia
from .connect_db import connect
from sqlmodel import Session, select


def select_all():
    engine = connect()
    with Session(engine) as session:
        query = select(Provincia)
        return session.exec(query).all()
    
def create_provincia(provincia: Provincia):
    engine = connect()
    with Session(engine) as session:
        session.add(provincia)
        session.commit()
        return select_all() 
    

def select_provincia_by_nombre(nombre: str):
    engine = connect()
    with Session(engine) as session:
        query = select(Provincia).where(Provincia.nombre == nombre)
        return session.exec(query).all()    