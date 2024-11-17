from ..repository.tabs_reposiroty import create_informe, create_inspeccion,update_obligacion_hacer
from ..model.all_model import *
from datetime import date


def create_inspeccion_service(id_inspeccion: int,
                            codigo_inspeccion: str, 
                            prod_o_serv_insp: str, 
                            fecha_inicio: date, 
                            fecha_fin: date,
                            infraccion_p_o_s: bool,
                            infraccion_higiene: bool,
                            infraccion_metrologia: bool,
                            codigo_inspector: str,
                            id_est: int,
                            id_informe: int,
                            numero_lineamiento:int
                            ):
    print("estoy en servicios")
    if not prod_o_serv_insp or not fecha_inicio or not infraccion_p_o_s or not infraccion_higiene or not infraccion_metrologia or not codigo_inspector or not id_est:
    
        raise ValueError("Faltan datos de la inspección")
    if infraccion_p_o_s == "on":
        infraccion_p_o_s = 1
    else: infraccion_p_o_s = 0

    if infraccion_higiene == "on":
        infraccion_higiene = 1
    else: infraccion_higiene = 0

    if infraccion_metrologia == "on":
        infraccion_metrologia = 1
    else: infraccion_metrologia = 0
    

    inspeccion_save = Inspeccion(
        id_inspeccion=id_inspeccion,
        codigo_inspeccion=codigo_inspeccion, 
        prod_o_serv_insp=prod_o_serv_insp, 
        fecha_inicio=fecha_inicio, 
        fecha_fin=fecha_fin, 
        infraccion_p_o_s=infraccion_p_o_s, 
        infraccion_higiene=infraccion_higiene, 
        infraccion_metrologia=infraccion_metrologia,
        codigo_inspector=codigo_inspector, 
        id_est=id_est, 
        id_informe=id_informe, 
        numero_lineamiento=numero_lineamiento)
    print(inspeccion_save)
    return create_inspeccion(inspeccion_save)
    
def update_obligacion_service(codigo_obligacion: str, fecha_venc: date = None, fecha_comp: date = None, resultado: str = None, multa: float=None, codigo_norma: str = None) -> Oblig_Hacer:
    """Actualiza una obligación de hacer."""
    return update_obligacion_hacer(codigo_obligacion, fecha_venc, fecha_comp, resultado, multa, codigo_norma)