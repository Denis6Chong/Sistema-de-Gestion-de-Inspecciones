from ..model.all_model import Inspector, Inspeccion, Municipio, Provincia
from .connect_db import connect
from sqlmodel import Session, select
from sqlmodel import func
from datetime import datetime, timedelta

def select_all() -> list[Inspector]:
    """Obtiene todos los inspectores."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspector)
        return session.exec(query).all()

from sqlmodel import select, Session
from sqlalchemy.orm import joinedload

def select_all_disponibles() -> list[Inspector]:
    """Obtiene todos los inspectores."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspector).where(Inspector.baja == 0)
        return session.exec(query).all()
    

def select_all_oh() -> list[Inspector]:
    """Obtiene todos los inspectores con sus inspecciones relacionadas."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspector).options(joinedload(Inspector.inspecciones))  # Cargar inspecciones
        return session.exec(query).unique().all()
    
    
def select_inspector_by_codigo(codigo:str) -> Inspector:
    engine = connect()
    with Session(engine) as session:
        query = select(Inspector).where(Inspector.codigo_inspector == codigo)
        return session.exec(query).all()

def select_inspector_by_email(ci: str) -> list[Inspector]:
    """Obtiene un inspector por su correo electrónico."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspector).where(Inspector.ci.ilike(f"%{ci}%") | Inspector.nombre.ilike(f"%{ci}%") | Inspector.apellidos.ilike(f"%{ci}%"))
        return session.exec(query).all()


def create_inspector(inspector: Inspector) -> list[Inspector]:
    """Crea un nuevo inspector y devuelve la lista actualizada de inspectores."""
    engine = connect()
    with Session(engine) as session:
        session.add(inspector)
        session.commit()
        return select_all()  # Reutiliza la función para obtener todos


def delete_inspector(ci: str) -> list[Inspector]:
    """Elimina un inspector por su correo electrónico y devuelve la lista actualizada."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspector).where(Inspector.ci == ci)
        inspector_delete = session.exec(query).one_or_none()  # Maneja el caso de que no exista
        if inspector_delete:
            session.delete(inspector_delete)
            session.commit()
        return select_all()  # Reutiliza la función para obtener todos
    

def update_inspector(inspector: Inspector) -> list[Inspector]:
    """Actualiza una inspección existente y devuelve la lista actualizada de inspecciones."""
    engine = connect()
    with Session(engine) as session:
        existing_inspector = session.get(Inspector, inspector.codigo_inspector)
        print(existing_inspector)
        
        existing_inspector.nombre = inspector.nombre
        existing_inspector.apellidos = inspector.apellidos
        existing_inspector.direccion = inspector.direccion
        existing_inspector.telefono = inspector.telefono
        existing_inspector.sexo = inspector.sexo
        existing_inspector.ci = inspector.ci
        existing_inspector.baja = inspector.baja
        existing_inspector.municipio = inspector.municipio
        session.commit()

            # Refrescar el objeto existente para asegurarse de que está actualizado
        session.refresh(existing_inspector)

        return select_all()
    

def select_top_inspectores(cantidad: int) -> list[tuple[Inspector, int]]:
    """Obtiene los inspectores con más inspecciones en el último trimestre, limitando la cantidad."""
    engine = connect()
    with Session(engine) as session:
        # Calcula la fecha del inicio del último trimestre
        today = datetime.today()
        start_of_quarter = today - timedelta(days=90)  # Aproximadamente 3 meses

        query = (
            select(Inspector, func.count(Inspeccion.id_inspeccion).label("total_inspecciones"))
            .join(Inspeccion, Inspector.codigo_inspector == Inspeccion.codigo_inspector)
            .where(Inspeccion.fecha_inicio >= start_of_quarter)
            .group_by(Inspector.codigo_inspector)
            .order_by(func.count(Inspeccion.id_inspeccion).desc())
            .limit(cantidad)
        )

        results = session.exec(query).all()
        return results

def select_inspecciones_inspector(codigo_inspector:str) -> list[Inspeccion]:
        engine = connect()
        with Session(engine) as session:
            query = select(Inspeccion).where(Inspeccion.codigo_inspector == codigo_inspector)
            return session.exec(query).all()

            

def select_inspector_by_municipio(nombre_municipio: str) -> list[Inspeccion]:
    
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Inspector).where(Inspector.municipio == nombre_municipio)
            )
        
        return session.exec(query).all()

def select_inspector_by_provincia(nombre_provincia: str) -> list[Inspeccion]:
    
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Inspector)
            .join(Municipio)  # Une Inspeccion con Establecimiento
            .join(Provincia)         # Une Establecimiento con Entidad       # Une Entidad con Organismo
            .where(Provincia.nombre == nombre_provincia)  # Filtra por el ID del organismo

        )
        return session.exec(query).all()