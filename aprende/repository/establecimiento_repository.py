from ..model.all_model import Establecimiento, Municipio, Entidad, Provincia, Organismo
from .connect_db import connect
from sqlmodel import Session, select, func
from sqlalchemy.orm import joinedload

def select_all():
    engine = connect()
    with Session(engine) as session:
        query = select(Establecimiento).options(
            joinedload(Establecimiento.entidad_relation), 
            joinedload(Establecimiento.est_municipio_relation)
        )
        establecimientos = session.exec(query).all()
        
        return establecimientos
    
def select_establecimiento_by_id(id_est: int):
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Establecimiento)
            .where(Establecimiento.id_est == id_est)
            .options(joinedload(Establecimiento.est_municipio_relation), 
                    joinedload(Establecimiento.entidad_relation))
        )
        return session.exec(query).all()
    
def select_establecimiento_by_ide(id_est: int):
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Establecimiento)
            .where(Establecimiento.id_est == id_est))
        return session.exec(query).all()



def select_establecimiento_by_nombre(nombre: str):
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Establecimiento)
            .where(Establecimiento.nombre.ilike(f"%{nombre}%"))
            .options(joinedload(Establecimiento.est_municipio_relation), 
                    joinedload(Establecimiento.entidad_relation))
        )
        return session.exec(query).all()

def create_establecimiento(establecimiento: Establecimiento):
    engine = connect()
    with Session(engine) as session:
        session.add(establecimiento)
        session.commit()
        return select_all()  

def delete_establecimiento(id_est: int):
    engine = connect()
    with Session(engine) as session:
        query = select(Establecimiento).where(Establecimiento.id_est == id_est)
        establecimiento_delete = session.exec(query).one()
        session.delete(establecimiento_delete)
        session.commit()
        return select_all()  # Retorna todos los establecimientos

def select_establecimientos_by_municipio(municipio_nombre: str):
    engine = connect()
    with Session(engine) as session:
        query = select(Establecimiento).where(Establecimiento.municipio_nombre == municipio_nombre).options(joinedload(Establecimiento.entidad_relation), 
                    joinedload(Establecimiento.est_municipio_relation))
        return session.exec(query).all()   

def select_establecimientos_by_entidad(id_entidad: int):
    engine = connect()
    with Session(engine) as session:
        query = select(Establecimiento).where(Establecimiento.id_entidad == id_entidad)
        return session.exec(query).all()

def get_entidad_by_establecimiento_nombre(nombre: str):
    engine = connect()
    with Session(engine) as session:
        # Buscar la entidad por su nombre
        entidad = session.exec(select(Establecimiento).where(Establecimiento.nombre == nombre)).first()
        
        # Verificar si la entidad existe y tiene un entidad relacionado
        if entidad and entidad.entidad_relation:
            return entidad.entidad_relation
        
        

def get_nombre_entidad_by_establecimiento_nombre(nombre: str):
    engine = connect()
    with Session(engine) as session:
        # Buscar la entidad por su nombre
        entidad = session.exec(select(Establecimiento).where(Establecimiento.nombre == nombre)).first()
        
        if entidad and entidad.entidad_relation:
            return entidad.entidad_relation.nombre
        
        
def update_establecimiento(establecimiento: Establecimiento) -> list[Establecimiento]:
    engine = connect()
    with Session(engine) as session:
        existing_establecimiento = session.get(Establecimiento, establecimiento.id_est)
        print(existing_establecimiento)
        if existing_establecimiento:
            existing_establecimiento.nombre = establecimiento.nombre
            existing_establecimiento.direccion = establecimiento.direccion
            existing_establecimiento.telefono = establecimiento.telefono
            existing_establecimiento.municipio_nombre = establecimiento.municipio_nombre
            existing_establecimiento.id_entidad = establecimiento.id_entidad
            session.commit()
        print("Inspección no encontrada con el código proporcionado")
            # Refrescar el objeto existente para asegurarse de que está actualizado
        session.refresh(existing_establecimiento)
        return select_all()
    


def select_establecimiento_by_nombre_provincia(nombre_provincia: str):

    engine = connect()
    with Session(engine) as session:
        query = (
            select(Establecimiento)
            .join(Municipio)
            .join(Provincia)
            .where(Provincia.nombre.ilike(f"{nombre_provincia}"))
            .options(joinedload(Establecimiento.est_municipio_relation), 
                    joinedload(Establecimiento.entidad_relation))
        )
        return session.exec(query).all()

def select_establecimientos_by_nombre_entidad(nombre_entidad: str):
    
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Establecimiento)
            .join(Establecimiento.entidad_relation)
            .where(Entidad.nombre.ilike(f"{nombre_entidad}"))
            .options(joinedload(Establecimiento.entidad_relation), 
                    joinedload(Establecimiento.est_municipio_relation))
        )
        return session.exec(query).all()

def select_establecimiento_by_nombre_organismo(nombre_organismo: str):
    
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Establecimiento)
            .join(Entidad)  
            .join(Organismo)# Asumiendo que la relación de organismo está a través de la entidad
            .where(Organismo.nombre.ilike(f"{nombre_organismo}"))
            .options(joinedload(Establecimiento.entidad_relation), 
                    joinedload(Establecimiento.est_municipio_relation))
        )
        return session.exec(query).all()