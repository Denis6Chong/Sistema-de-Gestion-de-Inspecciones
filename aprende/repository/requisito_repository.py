from ..model.all_model import Requisito, Norma # Importa el modelo de Requisito
from .connect_db import connect  # Importa la función de conexión a la base de datos
from sqlmodel import Session, select  # Importa herramientas para consultas y sesiones

# Función para seleccionar todas las requisitos
def select_all() -> list[Requisito]:
    """Devuelve una lista de todas las requisitos en la base de datos."""
    engine = connect()
    with Session(engine) as session:
        query = select(Requisito)
        return session.exec(query).all()

# Función para crear una nueva requisito
def create_requisito(requisito: Requisito) -> list[Requisito]:
    """Crea una nueva requisito y devuelve la lista actualizada de requisitos."""
    engine = connect()
    with Session(engine) as session:
        session.add(requisito)
        session.commit()
        return select_all()

# Función para seleccionar una requisito por su código
def select_requisito_by_codigo(id: int) -> list[Requisito]:
    """Devuelve una lista con la requisito correspondiente al código proporcionado."""
    engine = connect()
    with Session(engine) as session:
        query = select(Requisito).where(Requisito.id == id)
        return session.exec(query).all()
    


def select_requisito_by_titulo(titulo: str) -> list[Requisito]:
    """Devuelve una lista con la requisito correspondiente al código proporcionado."""
    engine = connect()
    with Session(engine) as session:
        query = select(Requisito).where(Requisito.titulo.ilike(f"%{titulo}%"))
        return session.exec(query).all()
    
def select_requisito_by_codigo_and_return(id: int) -> list[Requisito]:
    """Devuelve una lista con la requisito correspondiente al código proporcionado."""
    engine = connect()
    with Session(engine) as session:
        # Comprobamos si el código es realmente el que estamos buscando
        query = select(Requisito).where(Requisito.id == id)
        
        resultado = session.exec(query).all()
        
        return resultado

# Función para eliminar una requisito por su código
def delete_requisito(id: int) -> list[Requisito]:
    """Elimina una requisito por su código y devuelve la lista actualizada de requisitos."""
    engine = connect()
    with Session(engine) as session:
        query = select(Requisito).where(Requisito.id == id)
        requisito_delete = session.exec(query).one_or_none()  # Maneja el caso de que no exista
        if requisito_delete:
            session.delete(requisito_delete)
            session.commit()
        return select_all()  # Reutiliza la función para obtener todas

def update_requisito(requisito: Requisito) -> list[Requisito]:
    engine = connect()
    with Session(engine) as session:
        existing_requisito = session.get(Requisito, requisito.id)
        print(existing_requisito)
        if existing_requisito:
            existing_requisito.id = requisito.id
            existing_requisito.titulo = requisito.titulo
            existing_requisito.codigo_norma = requisito.codigo_norma
            session.commit()
        print("Requisito no encontrada con el código proporcionado")
            # Refrescar el objeto existente para asegurarse de que está actualizado
        session.refresh(existing_requisito)
        return select_all()
    

def select_requisito_by_nombre_norma(titulo: str):
    
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Requisito)
            .join(Norma)  
            .where(Norma.titulo.ilike(f"{titulo}"))
        )
        return session.exec(query).all()