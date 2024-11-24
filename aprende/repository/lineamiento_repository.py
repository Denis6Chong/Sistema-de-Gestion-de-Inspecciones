from ..model.all_model import Lineamiento
from .connect_db import connect
from sqlmodel import Session, select

def select_all():
    engine = connect()
    with Session(engine) as session:
        query = select(Lineamiento)
        return session.exec(query).all()
    
    

def create_lineamiento(lineamiento: Lineamiento):
    engine = connect()
    with Session(engine) as session:
        session.add(lineamiento)
        session.commit()
        return select_all()

def select_lineamiento_by_titulo(titulo: str):
    
    engine = connect()
    with Session(engine) as session:
        query = select(Lineamiento).where(Lineamiento.titulo.ilike(f"%{titulo}%") )
        return session.exec(query).all()
    
def select_lineamiento_by_numero(numero: int):
    
    engine = connect()
    with Session(engine) as session:
        query = select(Lineamiento).where(Lineamiento.numero == numero)
        return session.exec(query).all()


def delete_lineamiento(numero: int) -> list[Lineamiento]:
    """Elimina un lineamiento por su correo electrónico y devuelve la lista actualizada."""
    engine = connect()
    with Session(engine) as session:
        query = select(Lineamiento).where(Lineamiento.numero == numero)
        lineamiento_delete = session.exec(query).one_or_none()  # Maneja el caso de que no exista
        if lineamiento_delete:
            session.delete(lineamiento_delete)
            session.commit()
        return select_all()  # Reutiliza la función para obtener todos
    
def update_lineamiento(lineamiento: Lineamiento) -> list[Lineamiento]:
    """Actualiza un lineamiento existente y devuelve la lista actualizada de lineamientoes."""
    engine = connect()
    with Session(engine) as session:
        existing_lineamiento = session.get(Lineamiento, lineamiento.numero)
        existing_lineamiento.numero = lineamiento.numero
        existing_lineamiento.titulo = lineamiento.titulo
        session.commit()
        
        # Refrescar el objeto existente para asegurarse de que está actualizado
        session.refresh(existing_lineamiento)

        return select_all()
        
#consultas para ver que inspecciones tiene un lineamiento
"""def select_inspecciones_by_lineamiento(numero_lineamiento: int):
    engine = connect()
    with Session(engine) as session:
        query = select(Inspeccion).join(LineamientoInspeccion).where(LineamientoInspeccion.numero_lineamiento == numero_lineamiento)
        return session.exec(query).all()

# Función para agregar lineamientos a una inspección
def add_lineamientos_to_inspeccion(id_inspeccion: int, lineamientos: List[int]):
    engine = connect()
    with Session(engine) as session:
        for numero_lineamiento in lineamientos:
            lineamiento_inspeccion = LineamientoInspeccion(
                id_inspeccion=id_inspeccion,
                numero_lineamiento=numero_lineamiento
            )
            session.add(lineamiento_inspeccion)
        session.commit()"""