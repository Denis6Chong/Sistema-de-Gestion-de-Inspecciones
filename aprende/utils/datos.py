from enum import Enum  # Para el uso de ENUM


# Definir ENUM para Sexo y Tipo de Obligación
class SexoEnum(str, Enum):
    M = "M"
    F = "F"


class TipoObligacionEnum(str, Enum):
    PRODUCTO_SERVICIO = "Producto o Servicio"
    HIGIENE = "Higiene"
    METROLOGIA = "Metrologia"


class ResultadoEnum(str, Enum):
    EN_ESPERA = "En Espera"
    CUMPLIDA = "Cumplida"
    NO_CUMPLIDA = "No Cumplida"