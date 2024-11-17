from ..model.all_model import Norma  # Importa el modelo de Norma
from .connect_db import connect  # Importa la función de conexión a la base de datos
from sqlmodel import Session, select  # Importa herramientas para consultas y sesiones

# Función para seleccionar todas las normas
def select_all() -> list[Norma]:
    """Devuelve una lista de todas las normas en la base de datos."""
    engine = connect()
    with Session(engine) as session:
        query = select(Norma)
        return session.exec(query).all()

# Función para crear una nueva norma
def create_norma(norma: Norma) -> list[Norma]:
    """Crea una nueva norma y devuelve la lista actualizada de normas."""
    engine = connect()
    with Session(engine) as session:
        session.add(norma)
        session.commit()
        return select_all()

# Función para seleccionar una norma por su código
def select_norma_by_codigo(codigo_norma: str) -> list[Norma]:
    """Devuelve una lista con la norma correspondiente al código proporcionado."""
    engine = connect()
    with Session(engine) as session:
        query = select(Norma).where(Norma.codigo_norma == codigo_norma)
        return session.exec(query).all()
    
def select_norma_by_codigo_and_return(codigo_norma: str) -> list[Norma]:
    """Devuelve una lista con la norma correspondiente al código proporcionado."""
    engine = connect()
    with Session(engine) as session:
        # Comprobamos si el código es realmente el que estamos buscando
        query = select(Norma).where(Norma.codigo_norma == codigo_norma)
        
        resultado = session.exec(query).all()
        
        return resultado

# Función para eliminar una norma por su código
def delete_norma(codigo_norma: str) -> list[Norma]:
    """Elimina una norma por su código y devuelve la lista actualizada de normas."""
    engine = connect()
    with Session(engine) as session:
        query = select(Norma).where(Norma.codigo_norma == codigo_norma)
        norma_delete = session.exec(query).one_or_none()  # Maneja el caso de que no exista
        if norma_delete:
            session.delete(norma_delete)
            session.commit()
        return select_all()  # Reutiliza la función para obtener todas

def update_norma(norma: Norma) -> list[Norma]:
    engine = connect()
    with Session(engine) as session:
        existing_norma = session.get(Norma, norma.codigo_norma)
        print(existing_norma)
        if existing_norma:
            existing_norma.codigo_norma = norma.codigo_norma
            existing_norma.titulo = norma.titulo
            session.commit()
        print("Norma no encontrada con el código proporcionado")
            # Refrescar el objeto existente para asegurarse de que está actualizado
        session.refresh(existing_norma)
        return select_all()