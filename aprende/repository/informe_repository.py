from ..model.all_model import Informe  # Importa el modelo de Informe
from .connect_db import connect  # Importa la función de conexión a la base de datos
from sqlmodel import Session, select  # Importa herramientas para consultas y sesiones
from datetime import date
# Función para seleccionar todas las informes
def select_all() -> list[Informe]:
    """Devuelve una lista de todas las informes en la base de datos."""
    engine = connect()
    with Session(engine) as session:
        query = select(Informe)
        return session.exec(query).all()

# Función para crear una nueva informe
def create_informe(informe: Informe) -> list[Informe]:
    """Crea una nueva informe y devuelve la lista actualizada de informes."""
    engine = connect()
    with Session(engine) as session:
        session.add(informe)
        session.commit()
        return select_all()

# Función para seleccionar una informe por su código
def select_informe_by_codigo(id_informe: int) -> list[Informe]:
    """Devuelve una lista con la informe correspondiente al código proporcionado."""
    engine = connect()
    with Session(engine) as session:
        query = select(Informe).where(Informe.id_informe == id_informe)
        return session.exec(query).all()
    
def select_informe_by_titulo(titulo: str) -> list[Informe]:
    """Devuelve una lista con la informe correspondiente al código proporcionado."""
    engine = connect()
    with Session(engine) as session:
        query = select(Informe).where(Informe.titulo.ilike(f"%{titulo}%"))
        return session.exec(query).all()
    
def select_informe_by_codigo_and_return(id_informe: int) -> list[Informe]:
    """Devuelve una lista con la informe correspondiente al código proporcionado."""
    engine = connect()
    with Session(engine) as session:
        # Comprobamos si el código es realmente el que estamos buscando
        query = select(Informe).where(Informe.id_informe == id_informe)
        
        resultado = session.exec(query).all()
        
        return resultado

# Función para eliminar una informe por su código
def delete_informe(id_informe: int) -> list[Informe]:
    """Elimina una informe por su código y devuelve la lista actualizada de informes."""
    engine = connect()
    with Session(engine) as session:
        query = select(Informe).where(Informe.id_informe == id_informe)
        informe_delete = session.exec(query).one_or_none()  # Maneja el caso de que no exista
        if informe_delete:
            session.delete(informe_delete)
            session.commit()
        return select_all()  # Reutiliza la función para obtener todas
    

def update_informe(informe: Informe) -> list[Informe]:
    """Actualiza un informe existente y devuelve la lista actualizada de informees."""
    engine = connect()
    with Session(engine) as session:
        existing_informe = session.get(Informe, informe.id_informe)
        print(existing_informe)
    
        existing_informe.id_informe = informe.id_informe
        existing_informe.titulo = informe.titulo
        existing_informe.fecha = informe.fecha
        existing_informe.conclusiones = informe.conclusiones
        existing_informe.conforme = informe.conforme
        session.commit()
        # Refrescar el objeto existente para asegurarse de que está actualizado
        session.refresh(existing_informe)

    return select_all()


def select_informe_by_month(month: int, year: int) -> list[Informe]:
    """Obtiene las inspecciones realizadas en un mes y año específicos."""
    
    engine = connect()
    with Session(engine) as session:
        start_date = date(year, month, 1)
        end_date = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
        query = select(Informe).where(Informe.fecha >= start_date, Informe.fecha < end_date)
        return session.exec(query).all()