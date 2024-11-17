from ..repository.inspector_repository import select_inspector_by_provincia, select_inspector_by_municipio, select_all_disponibles, select_inspecciones_inspector, select_inspector_by_codigo, select_all, select_all_oh, select_inspector_by_email, create_inspector, delete_inspector,update_inspector
from ..model.all_model import Inspector
from ..utils.validate import validate_ci

def select_all_inspector_service():
    inspector = select_all()
    return inspector

def select_all_disponibles_service():
    inspector = select_all_disponibles()
    return inspector

def select_inspector_by_email_service(ci:str):
    if(len(ci) != 0):
        return select_inspector_by_email(ci)
    else:
        return select_all()
    

def select_inspector_by_codigo_service(codigo:str):
    if(len(codigo) != 0):
        return select_inspector_by_codigo(codigo)
    else:
        return select_all()
    
    
def create_inspector_service(codigo_inspector: str,nombre: str, apellidos: str, direccion: str ,municipio: str, telefono: str, sexo: str, ci: str, baja: int):
    if  not nombre or not apellidos or not ci:
        raise ValueError("Faltan campos obligatorios")
    if not validate_ci(ci):
        raise ValueError("CI no válido")
    
    inspector = select_inspector_by_email_service(ci)
    if(len(inspector) == 0):
        inspector_save = Inspector(
            codigo_inspector=codigo_inspector, 
            nombre=nombre, 
            apellidos=apellidos, 
            direccion=direccion, 
            municipio=municipio, 
            telefono=telefono, 
            sexo=sexo, 
            ci=ci, 
            baja=baja if baja is not None else 0)
        return create_inspector(inspector_save)
    else:
        raise BaseException("El usuario ya existe")

def delete_inspector_service(ci:str):
    return delete_inspector(ci=ci)

def select_all_inspectors_oh():
    oh_inspectors= []
    inspectors = select_all_oh()
    for inspector in inspectors:
        if inspector.inspecciones:
            for inspeccion in inspector.inspecciones:
                if inspeccion.codigo_inspeccion[-3:] != "000":
                    oh_inspectors.append(inspector)

    return oh_inspectors            


def update_inspector_service(
                            codigo_inspector: str,
                            nombre: str, 
                            apellidos: str, 
                            direccion: str, 
                            telefono: str,
                            sexo: str,
                            ci: str,
                            baja: int,
                            municipio: str
                            ):
    if not nombre or not ci:
    
        raise ValueError("Faltan datos de la inspección")
    
    if not validate_ci(ci):
        raise ValueError("CI no válido")
    
    inspector = select_inspector_by_codigo_service(codigo_inspector)

    inspector_save = Inspector(
            
            codigo_inspector=codigo_inspector,
            nombre=nombre, 
            apellidos=apellidos, 
            direccion=direccion, 
            telefono=telefono, 
            sexo=sexo, 
            ci=ci,
            baja=baja,
            municipio=municipio)
    
    return update_inspector(inspector_save)



from ..repository.inspector_repository import select_top_inspectores

def select_top_inspectores_service_handler(cantidad: int):
    """Servicio que obtiene los inspectores con mayor cantidad de inspecciones."""
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a 0.")
    
    top_inspectores = select_top_inspectores(cantidad)
    if not top_inspectores:
        raise ValueError(f"No se encontraron inspectores con inspecciones.")
    
    return top_inspectores


def cant_inspecciones_inspector_service(codigo_inspector: str):
    if codigo_inspector:
        return len(select_inspecciones_inspector(codigo_inspector))
    else:
        raise ValueError("El código de inspector es requerido")
    

def tiene_inspecciones_service(codigo_inspector: str):
    print(f"Recibiendo código inspector: {codigo_inspector}")
    inspecciones = select_inspecciones_inspector(codigo_inspector)
    print(f"Inspecciones para {codigo_inspector}: {inspecciones}")
    
    if inspecciones == []:
        return True
    else:
        return False
def select_inspector_by_municipio_service(nombre_municipio: str):
    """Obtiene las inspecciones por código de municipio."""
    
    if nombre_municipio:
        return select_inspector_by_municipio(nombre_municipio)
    else:
        raise ValueError("El nombre de municipio es requerido")
    
def select_inspector_by_provincia_service(nombre_provincia: str):
    """Obtiene las inspecciones por código de provincia."""
    if nombre_provincia:
        return select_inspector_by_provincia(nombre_provincia)
    else:
        raise ValueError("El nombre de organismo es requerido")