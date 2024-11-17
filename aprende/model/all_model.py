import reflex as rx
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
import re  # Necesario para la validación del formato con expresiones regulares
import datetime as date
from ..utils.datos import SexoEnum,ResultadoEnum,TipoObligacionEnum
from pydantic import validator

class Provincia(rx.Model, table=True):
    nombre: str = Field(default=None, primary_key=True)
    municipios: List["Municipio"] = Relationship(back_populates="provincia_relation")


class Municipio(rx.Model, table=True):
    nombre: str = Field(default=None, primary_key=True)
    nombre_provincia: str = Field(default=None, foreign_key="provincia.nombre")
    provincia_relation: Optional[Provincia] = Relationship(back_populates="municipios")
    
    # Relaciones hacia inspectores y establecimientos
    inspectores: List["Inspector"] = Relationship(back_populates="municipio_relation")
    establecimientos: List["Establecimiento"] = Relationship(back_populates="est_municipio_relation")



class Inspector(rx.Model, table=True):
    codigo_inspector: Optional[str] = Field(default=None, primary_key=True )  # Llave primaria
    nombre: str = Field(default="")
    apellidos: str = Field(default="")
    direccion: str = Field(default=None)
    municipio: Optional[str] = Field(default=None, foreign_key="municipio.nombre")  # Llave foránea
    telefono: str = Field(default=None)
    sexo: SexoEnum = Field(default=SexoEnum.F)
    ci: Optional[str] = Field(default=None)
    baja: int = Field(default=0)

    # Relación hacia municipio
    municipio_relation: Optional[Municipio] = Relationship(back_populates="inspectores")
    # Relación hacia inspeccion
    inspecciones: list["Inspeccion"] = Relationship(back_populates="inspector")
    # Validador para el campo `ci`
    

class Organismo(rx.Model, table=True):
    id_organismo: Optional[int] = Field(default=None, primary_key=True)  # Llave primaria, autoincremental
    nombre: str = Field(default=None)
    siglas: str = Field(default=None)
    direccion: str = Field(default=None)
    telefono: str = Field(default=None)

    entidades: List["Entidad"] = Relationship(back_populates="organismo_relation")


class Entidad(rx.Model, table=True):
    id_entidad: Optional[int] = Field(default=None, primary_key=True)  # Llave primaria, autoincremental
    nombre: str = Field(default=None)
    siglas: str = Field(default=None)
    id_organismo: Optional[int] = Field(default=None, foreign_key="organismo.id_organismo")  # Llave foránea

    organismo_relation: Optional[Organismo] = Relationship(back_populates="entidades")
    establecimientos: List["Establecimiento"] = Relationship(back_populates="entidad_relation")
    @property
    def nombre_organismo(self):
        return self.organismo_relation.nombre if self.organismo_relation else "Desconocido"


class Establecimiento(rx.Model, table=True):
    id_est: Optional[int] = Field(default=None, primary_key=True)  # Llave primaria, autoincremental
    nombre: str = Field(default="")
    direccion: str = Field(default=None)
    telefono: str = Field(default=None)
    municipio_nombre: Optional[str] = Field(default=None, foreign_key="municipio.nombre")  # Llave foránea por nombre
    id_entidad: Optional[int] = Field(default=None, foreign_key="entidad.id_entidad")  # Llave foránea

    est_municipio_relation: Optional[Municipio] = Relationship(back_populates="establecimientos")
    entidad_relation: Optional[Entidad] = Relationship(back_populates="establecimientos")
    inspecciones: list["Inspeccion"] = Relationship(back_populates="establecimiento")


class Lineamiento(rx.Model, table=True):
    numero: int = Field(primary_key=True)  # Llave primaria autoincremental
    titulo: str = Field(nullable=False)  # Título no puede ser nulo
    
    # Relación inversa hacia inspecciones (si hay relación)
    #inspecciones: List["LineamientoInspeccion"] = Relationship(back_populates="lineamiento")
    inspecciones: list["Inspeccion"] = Relationship(back_populates="lineamiento")



class Norma(rx.Model, table=True):
    # Código de la norma, llave primaria
    codigo_norma: str = Field(
        primary_key=True,
        nullable=False,
            # Validación del formato: 'ISO' seguido de 1 a 5 dígitos
    )
    # Título de la norma, obligatorio
    titulo: str = Field(nullable=False)
    obligaciones: List["Oblig_Hacer"] = Relationship(back_populates="norma")
    requisitos: List["Requisito"] = Relationship(back_populates="norma")


class Requisito(rx.Model, table=True):
    # ID del requi, llave primaria
    id: Optional[int] = Field(primary_key=True)
    
    # Título del requisito, obligatorio
    titulo: str = Field(nullable=False)
    
    # Código de la norma, clave foránea
    codigo_norma: str = Field(foreign_key="norma.codigo_norma", nullable=False)
    
    # Relación con el modelo Norma
    norma: Optional[Norma] = Relationship(back_populates="requisitos")


    # Método para validar el formato de 'codigo_norma' al establecerlo
    
class Informe(rx.Model, table=True):
    # Código de la norma, llave primaria
    id_informe: Optional[int] = Field(
        primary_key=True,
        nullable=False,
    # Validación del formato: 'ISO' seguido de 1 a 5 dígitos
    )
    # Título de la norma, obligatorio
    titulo: Optional[str]
    fecha: Optional[date.date] = Field(nullable=False)
    conclusiones: Optional[str]
    conforme: int

    inspecciones: list["Inspeccion"] = Relationship(back_populates="informe")

class Inspeccion(rx.Model, table=True):
    id_inspeccion: Optional[int] = Field(default=None, unique=True)
    codigo_inspeccion: Optional[str] = Field(default=None, primary_key=True )  # Llave primaria
    prod_o_serv_insp: str = Field(default="")
    fecha_inicio: date.date = Field(default="")
    fecha_fin: Optional[date.date] = Field(default=None)
    infraccion_p_o_s: int = Field(default=0)
    infraccion_higiene: int = Field(default=0)
    infraccion_metrologia: int = Field(default=0)
    codigo_inspector: str = Field(default=None, foreign_key="inspector.codigo_inspector")  # Llave foránea
    id_est: int = Field(default=None, foreign_key="establecimiento.id_est")
    id_informe: Optional[int] = Field(default=None, foreign_key="informe.id_informe") 
    numero_lineamiento: Optional[int] = Field(default=None, foreign_key="lineamiento.numero")

    #Relacicones inversas
    establecimiento: Establecimiento | None = Relationship(back_populates="inspecciones")
    inspector: Inspector | None = Relationship(back_populates="inspecciones")
    informe: Informe | None = Relationship(back_populates="inspecciones")
    lineamiento: Lineamiento | None = Relationship(back_populates="inspecciones")

    # Relación con Oblig_Hacer
# obligaciones: List["Oblig_Hacer"] = Relationship(back_populates="inspeccion")

class Oblig_Hacer(rx.Model, table=True):
    codigo_obligacion: Optional[str] = Field(primary_key=True)  # Llave primaria que combina el id de inspección y el tipo de obligación
    id_inspeccion: Optional[int] = Field(default=None)  
    tipo_obligacion: Optional[str] = Field(default=None)  # Tipo de obligación ('Producto o Servicio', 'Higiene', 'Metrologia')
    fecha_inicio: Optional[date.date] = Field(default=None)  # Fecha de inicio de la obligación
    fecha_venc: Optional[date.date]= Field(default=None)  # Fecha de vencimiento de la obligación (si aplica)
    fecha_comp: Optional[date.date] = Field(default=None)  # Fecha de cumplimiento de la obligación (si aplica)
    tiempo: Optional[int] = Field(default=None)  # Tiempo estimado para cumplir la obligación (en días)
    resultado: Optional[str] = Field(default=None)  # Estado de la obligación (por ejemplo, 'En Espera')
    multa: Optional[float] = Field(default=0.0)  # Multa asociada a la obligación (inicialmente 0)
    codigo_norma: Optional[str] = Field(default=None, foreign_key="norma.codigo_norma") 
    
    norma: Optional[Norma] = Relationship(back_populates="obligaciones")



class User(rx.Model, table=True):
    """A table of Users."""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str 
    password: str




""" if hero.team:
    print(hero.team.name)
    
    Incluir objetos de relación en el lado Varios¶
Dijimos antes que esta es una relación de muchos a uno, porque puede haber muchos héroes que pertenezcan a un equipo.

También podemos conectar los datos con estos atributos de relación en el lado múltiple.

Como el atributo se comporta como una lista, simplemente podemos agregarle.team.heroes

Vamos a crear algunos héroes más y añadirlos al atributo de lista:team_preventers.heroes


Python 3.10+
Python 3.9+
Python 3.7+

# Code above omitted 👆

def create_heroes():
    with Session(engine) as session:

        # Previous code here omitted 👈

        hero_tarantula = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
        hero_dr_weird = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
        hero_cap = Hero(
            name="Captain North America", secret_name="Esteban Rogelios", age=93
        )

        team_preventers.heroes.append(hero_tarantula)
        team_preventers.heroes.append(hero_dr_weird)
        team_preventers.heroes.append(hero_cap)
        session.add(team_preventers)
        session.commit()
        session.refresh(hero_tarantula)
        session.refresh(hero_dr_weird)
        session.refresh(hero_cap)
        print("Preventers new hero:", hero_tarantula)
        print("Preventers new hero:", hero_dr_weird)
        print("Preventers new hero:", hero_cap)

# Code below omitted 👇
    """
