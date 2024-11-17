import re
from datetime import datetime

def validate_ci(ci: str) -> bool:
    """
    Valida el formato de un CI (Cédula de Identidad) de 11 dígitos.
    Los primeros 6 dígitos deben corresponder a una fecha válida en el formato YYMMDD.
    
    :param ci: La cédula de identidad a validar.
    :return: True si el CI es válido, False de lo contrario.
    """
    # Verifica que el CI tenga exactamente 11 dígitos
    if len(ci) != 11 or not ci.isdigit():
        return False
    
    # Extraemos los primeros 6 dígitos para validar la fecha
    fecha_str = ci[:6]
    
    try:
        # Convertimos los primeros 6 dígitos en un objeto datetime para verificar la validez de la fecha
        fecha = datetime.strptime(fecha_str, "%y%m%d")
        return True
    except ValueError:
        # Si la fecha no es válida, retornamos False
        return False