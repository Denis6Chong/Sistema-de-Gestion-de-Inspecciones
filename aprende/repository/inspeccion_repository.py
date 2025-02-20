from ..model.all_model import Inspeccion, Entidad, Informe, Establecimiento, Organismo, Inspector
from .connect_db import connect
from sqlmodel import Session, select
from datetime import date
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, and_

def select_all_inspecciones() -> list[Inspeccion]:
    """Obtiene todas las inspecciones."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspeccion).options(
            joinedload(Inspeccion.inspector), 
            joinedload(Inspeccion.establecimiento),
            joinedload(Inspeccion.informe), 
            joinedload(Inspeccion.lineamiento)
        )
        inspecciones = session.exec(query).all()

        return inspecciones
            
def select_inspeccion_by_titulo_informe(titulo: str) -> list[Inspeccion]:
    """Obtiene una inspección por el nombre del inspector."""
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Inspeccion)
            .join(Informe)  # Unimos con la tabla Inspector
            .where(Informe.titulo == titulo)
            .options(joinedload(Inspeccion.inspector), 
                    joinedload(Inspeccion.establecimiento),
                    joinedload(Inspeccion.informe),
                    joinedload(Inspeccion.lineamiento)
                    )
        )
        return session.exec(query).all()            


def select_inspeccion_by_codigo(codigo_inspeccion: str) -> list[Inspeccion]:
    """Obtiene una inspección por su código de inspección."""
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Inspeccion)
            .where(Inspeccion.codigo_inspeccion == codigo_inspeccion)
            .options(joinedload(Inspeccion.inspector), 
                    joinedload(Inspeccion.establecimiento),
                    joinedload(Inspeccion.informe),
                    joinedload(Inspeccion.lineamiento)
                    )
        )
        return session.exec(query).all()
    




def select_inspecciones_by_inspectores(codigo_inspector: str) -> list[Inspeccion]:
    """Obtiene las inspecciones asociadas a un inspector dado su código."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspeccion).where(Inspeccion.codigo_inspector == codigo_inspector).options(
            joinedload(Inspeccion.inspector), 
            joinedload(Inspeccion.establecimiento),
            joinedload(Inspeccion.informe), 
            joinedload(Inspeccion.lineamiento))
        return session.exec(query).all()



def select_inspeccion_by_nombre_inspector(nombre_inspector: str) -> list[Inspeccion]:
    """Obtiene una inspección por el nombre del inspector."""
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Inspeccion)
            .join(Inspector)  # Unimos con la tabla Inspector
            .where(Inspector.nombre.ilike(f"%{nombre_inspector}%"))  # Búsqueda parcial por nombre de inspector
            .options(joinedload(Inspeccion.inspector), 
                    joinedload(Inspeccion.establecimiento),
                    joinedload(Inspeccion.informe),
                    joinedload(Inspeccion.lineamiento)
                    )
        )
        return session.exec(query).all()

def select_inspecciones_by_month(month: int, year: int) -> list[Inspeccion]:
    """Obtiene las inspecciones realizadas en un mes y año específicos."""
    engine = connect()
    with Session(engine) as session:
        start_date = date(year, month, 1)
        end_date = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
        query = select(Inspeccion).where(Inspeccion.fecha_inicio >= start_date, Inspeccion.fecha_inicio < end_date).options(
            joinedload(Inspeccion.inspector), 
            joinedload(Inspeccion.establecimiento),
            joinedload(Inspeccion.informe), 
            joinedload(Inspeccion.lineamiento))
        return session.exec(query).all()

def create_inspeccion_only(inspeccion: Inspeccion) -> Inspeccion:
    """Crea una nueva inspección y devuelve la inspección recién creada."""
    engine = connect()
    with Session(engine) as session:
        session.add(inspeccion)
        session.commit()
        
    
def create_inspeccion(inspeccion: Inspeccion) -> list[Inspeccion]:
    """Crea una nueva inspección y devuelve la lista actualizada de inspecciones."""
    engine = connect()
    with Session(engine) as session:
        session.add(inspeccion)
        session.commit()
        return select_all_inspecciones()  # Reutiliza la función para obtener todas


def update_inspeccion(inspeccion: Inspeccion) -> list[Inspeccion]:
    """Actualiza una inspección existente y devuelve la lista actualizada de inspecciones."""
    engine = connect()
    with Session(engine) as session:
        existing_inspeccion = session.get(Inspeccion, inspeccion.codigo_inspeccion)
        if existing_inspeccion:
            existing_inspeccion.id_inspeccion=inspeccion.id_inspeccion
            existing_inspeccion.codigo_inspeccion=inspeccion.codigo_inspeccion
            existing_inspeccion.prod_o_serv_insp = inspeccion.prod_o_serv_insp
            existing_inspeccion.fecha_inicio = inspeccion.fecha_inicio
            existing_inspeccion.fecha_fin = inspeccion.fecha_fin
            existing_inspeccion.infraccion_p_o_s = inspeccion.infraccion_p_o_s
            existing_inspeccion.infraccion_higiene = inspeccion.infraccion_higiene
            existing_inspeccion.infraccion_metrologia = inspeccion.infraccion_metrologia
            existing_inspeccion.codigo_inspector = inspeccion.codigo_inspector
            existing_inspeccion.id_est = inspeccion.id_est
            existing_inspeccion.id_informe = inspeccion.id_informe
            existing_inspeccion.numero_lineamiento = inspeccion.numero_lineamiento

            session.commit()
        print("Inspección no encontrada con el código proporcionado")       
        return select_all_inspecciones()  # Reutiliza la función para obtener todas
# Reutiliza la función para obtener todas
    

def delete_inspeccion(codigo_inspeccion: str) -> list[Inspeccion]:
    """Elimina una inspección por su código y devuelve la lista actualizada."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspeccion).where(Inspeccion.codigo_inspeccion == codigo_inspeccion)
        inspeccion_delete = session.exec(query).one_or_none()  # Maneja el caso de que no exista
        if inspeccion_delete:
            session.delete(inspeccion_delete)
            session.commit()
        return select_all_inspecciones()  # Reutiliza la función para obtener todas
    
from ..model.all_model import Inspeccion
from .connect_db import connect
from sqlmodel import Session, select

def select_inspecciones_with_infraccion():
    engine = connect()
    with Session(engine) as session:
        statement = select(Inspeccion).where(
            or_(
                Inspeccion.infraccion_p_o_s == 1,
                Inspeccion.infraccion_higiene == 1,
                Inspeccion.infraccion_metrologia == 1
            )
        ).options(
            joinedload(Inspeccion.inspector), 
            joinedload(Inspeccion.establecimiento),
            joinedload(Inspeccion.informe), 
            joinedload(Inspeccion.lineamiento))
        result = session.exec(statement)
        return result.all()


def select_inspecciones_with_infraccion_producto_servicio() -> list[Inspeccion]:
    """Obtiene todas las inspecciones donde hubo infracción de tipo Producto o Servicio."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspeccion).where(Inspeccion.infraccion_p_o_s == 1).options(
            joinedload(Inspeccion.inspector), 
            joinedload(Inspeccion.establecimiento),
            joinedload(Inspeccion.informe), 
            joinedload(Inspeccion.lineamiento))
        return session.exec(query).all()

def select_inspecciones_with_infraccion_higiene() -> list[Inspeccion]:
    """Obtiene todas las inspecciones donde hubo infracción de tipo Higiene."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspeccion).where(Inspeccion.infraccion_higiene == 1).options(
            joinedload(Inspeccion.inspector), 
            joinedload(Inspeccion.establecimiento),
            joinedload(Inspeccion.informe), 
            joinedload(Inspeccion.lineamiento))
        return session.exec(query).all()

def select_inspecciones_with_infraccion_metrologia() -> list[Inspeccion]:
    """Obtiene todas las inspecciones donde hubo infracción de tipo Metrología."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspeccion).where(Inspeccion.infraccion_metrologia == 1).options(
            joinedload(Inspeccion.inspector), 
            joinedload(Inspeccion.establecimiento),
            joinedload(Inspeccion.informe), 
            joinedload(Inspeccion.lineamiento))
        return session.exec(query).all()

def select_inspecciones_without_infraccion() -> list[Inspeccion]:
    """Obtiene todas las inspecciones donde no hubo ninguna infracción."""
    engine = connect()
    with Session(engine) as session:
        query = select(Inspeccion).where(
            and_(
                Inspeccion.infraccion_p_o_s == 0,
                Inspeccion.infraccion_higiene == 0,
                Inspeccion.infraccion_metrologia == 0
            )
        ).options(
            joinedload(Inspeccion.inspector), 
            joinedload(Inspeccion.establecimiento),
            joinedload(Inspeccion.informe), 
            joinedload(Inspeccion.lineamiento))
        return session.exec(query).all()


def select_inspecciones_by_organismo(nombre_organismo: str) -> list[Inspeccion]:
    """Filtra las inspecciones por el ID de un organismo."""
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Inspeccion)
            .join(Establecimiento)  # Une Inspeccion con Establecimiento
            .join(Entidad)         # Une Establecimiento con Entidad
            .join(Organismo)       # Une Entidad con Organismo
            .where(Organismo.nombre == nombre_organismo)  # Filtra por el ID del organismo
            .options(
                joinedload(Inspeccion.inspector),
                joinedload(Inspeccion.establecimiento),
                joinedload(Inspeccion.informe),
                joinedload(Inspeccion.lineamiento)
            )
        )
        return session.exec(query).all()
    

def select_inspecciones_by_nombre_inspector(inspector_nombre: str) -> list[Inspeccion]:
    """Filtra las inspecciones por el primer nombre y el primer apellido del inspector."""
    engine = connect()
    with Session(engine) as session:
        # Separar el parámetro en nombre y apellido
        nombre_partes = inspector_nombre.split()

        # Verificar si se tiene al menos un nombre y un apellido
        if len(nombre_partes) >= 2:
            primer_nombre = nombre_partes[0]
            primer_apellido = nombre_partes[1]
        else:
            primer_nombre = nombre_partes[0]
            primer_apellido = ""  # Si no hay apellido en el input, lo dejamos vacío

        # Construir la consulta utilizando ilike
        query = (
            select(Inspeccion)
            .join(Inspector)  # Unir con la tabla Inspector
            .where(
                Inspector.nombre.ilike(f"{primer_nombre}%") &  # Comparar con ilike por el primer nombre
                Inspector.apellidos.ilike(f"{primer_apellido}%")  # Comparar con ilike por el primer apellido
            )
            .options(
                joinedload(Inspeccion.inspector),
                joinedload(Inspeccion.establecimiento),
                joinedload(Inspeccion.informe),
                joinedload(Inspeccion.lineamiento)
            )
        )
        return session.exec(query).all()


def select_last_inspeccion_by_producto_servicio(producto_servicio: str) -> Inspeccion:
    """Obtiene la última inspección por su producto o servicio."""
    engine = connect()
    with Session(engine) as session:
        # Consulta para obtener la última inspección basada en el nombre del producto o servicio
        query = (
            select(Inspeccion)
            .where(Inspeccion.prod_o_serv_insp.ilike(f"%{producto_servicio}%"))
            .order_by(Inspeccion.id_inspeccion.desc())  # Ordenar por id_inspeccion descendente
            .limit(1)  # Limitar a 1 solo resultado
            
        )
        # Ejecutar la consulta y devolver el primer (y único) resultado encontrado
        return session.exec(query).one_or_none()
def select_inspeccion_by_producto_servicio(producto_servicio: str) -> list[Inspeccion]:
    """Obtiene una inspección por su producto o servicio."""
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Inspeccion)
            .where(Inspeccion.prod_o_serv_insp.ilike(f"%{producto_servicio}%") )
            .options(joinedload(Inspeccion.inspector),
                    joinedload(Inspeccion.establecimiento),
                    joinedload(Inspeccion.informe),
                    joinedload(Inspeccion.lineamiento)
                    )
        )
        return session.exec(query).all()
    
def select_inspeccion_by_producto_servicio(producto_servicio: str) -> list[Inspeccion]:
    """Obtiene una inspección por su producto o servicio."""
    engine = connect()
    with Session(engine) as session:
        query = (
            select(Inspeccion)
            .where(Inspeccion.prod_o_serv_insp.ilike(f"%{producto_servicio}%") )
            .options(joinedload(Inspeccion.inspector),
                    joinedload(Inspeccion.establecimiento),
                    joinedload(Inspeccion.informe),
                    joinedload(Inspeccion.lineamiento)
                    )
        )
        return session.exec(query).all()

def update_inspeccion(inspeccion: Inspeccion) -> list[Inspeccion]:
    """Actualiza una inspección existente y devuelve la lista actualizada de inspecciones."""
    engine = connect()
    with Session(engine) as session:
        existing_inspeccion = session.get(Inspeccion, inspeccion.codigo_inspeccion)
        print(existing_inspeccion)
        #
        
        if existing_inspeccion:
            existing_inspeccion.infraccion_p_o_s = inspeccion.infraccion_p_o_s
            existing_inspeccion.infraccion_higiene = inspeccion.infraccion_higiene
            existing_inspeccion.infraccion_metrologia = inspeccion.infraccion_metrologia

            # Generar el nuevo código de inspección basado en las infracciones actualizadas
            binario_infracciones = f"{inspeccion.infraccion_p_o_s}{inspeccion.infraccion_higiene}{inspeccion.infraccion_metrologia}"
            nuevo_codigo_inspeccion = f"{inspeccion.id_inspeccion}-{binario_infracciones}"

            # Actualiza otros campos
            existing_inspeccion.id_inspeccion = inspeccion.id_inspeccion
            existing_inspeccion.codigo_inspeccion = nuevo_codigo_inspeccion
            existing_inspeccion.prod_o_serv_insp = inspeccion.prod_o_serv_insp
            existing_inspeccion.fecha_inicio = inspeccion.fecha_inicio
            existing_inspeccion.fecha_fin = inspeccion.fecha_fin
            existing_inspeccion.codigo_inspector = inspeccion.codigo_inspector
            existing_inspeccion.id_est = inspeccion.id_est
            existing_inspeccion.id_informe = inspeccion.id_informe
            existing_inspeccion.numero_lineamiento = inspeccion.numero_lineamiento
            existing_inspeccion.codigo_real = inspeccion.codigo_real

            session.commit()

            # Refrescar el objeto existente para asegurarse de que está actualizado
            session.refresh(existing_inspeccion)

        return select_all_inspecciones()
    

def count_inspecciones_by_month_year(month: int, year: int) -> int:
    """Devuelve la cantidad de inspecciones realizadas en un mes y año específicos."""
    engine = connect()
    with Session(engine) as session:
        start_date = date(year, month, 1)
        end_date = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
        query = select(Inspeccion).where(
            Inspeccion.fecha_inicio >= start_date,
            Inspeccion.fecha_inicio < end_date
        )
        result = session.exec(query).all()  # Obtener todos los resultados
        return len(result)  # Contar el número de inspecciones


def count_inspecciones_without_infraccion_by_month_year(month: int, year: int) -> int:
    """Devuelve la cantidad de inspecciones sin infracciones en un mes y año específicos."""
    engine = connect()
    with Session(engine) as session:
        start_date = date(year, month, 1)
        end_date = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
        query = select(Inspeccion).where(
            Inspeccion.fecha_inicio >= start_date,
            Inspeccion.fecha_inicio < end_date,
            Inspeccion.infraccion_p_o_s == 0,
            Inspeccion.infraccion_higiene == 0,
            Inspeccion.infraccion_metrologia == 0
        )
        result = session.exec(query).all()  # Obtener todos los resultados
        return len(result)  # Contar el número de inspecciones sin infracción


def count_inspecciones_with_infraccion_by_month_year(month: int, year: int) -> int:
    """Devuelve la cantidad de inspecciones con infracciones en un mes y año específicos."""
    engine = connect()
    with Session(engine) as session:
        start_date = date(year, month, 1)
        end_date = date(year, month + 1, 1) if month < 12 else date(year + 1, 1, 1)
        query = select(Inspeccion).where(
            Inspeccion.fecha_inicio >= start_date,
            Inspeccion.fecha_inicio < end_date,
            or_(
                Inspeccion.infraccion_p_o_s == 1,
                Inspeccion.infraccion_higiene == 1,
                Inspeccion.infraccion_metrologia == 1
            )
        )
        result = session.exec(query).all()  # Obtener todos los resultados
        return len(result)  # Contar el número de inspecciones con infracción
