import time
import psutil
import numpy as np

# Función para medir el tiempo de respuesta
def medir_tiempo_respuesta(func, *args, **kwargs):
    """
    Función para medir el tiempo de respuesta de una operación.
    """
    start_time = time.time()
    result = func(*args, **kwargs)  # Llama a la función que estamos midiendo
    end_time = time.time()
    tiempo_respuesta = end_time - start_time
    return tiempo_respuesta, result

# Función para medir el uso de recursos del sistema (CPU y memoria)
def medir_uso_recursos():
    """
    Función para medir el uso de recursos del sistema (CPU y memoria).
    """
    # Monitorea el uso de la CPU y la memoria
    cpu = psutil.cpu_percent(interval=1)  # Porcentaje de CPU en el último segundo
    memoria = psutil.virtual_memory().percent  # Porcentaje de uso de la memoria RAM
    return cpu, memoria

# Función para ejecutar una serie de pruebas y obtener las métricas
def obtener_metricas(func, cantidad_muestras=100, *args, **kwargs):
    """
    Función para ejecutar 'cantidad_muestras' de una operación y calcular la media.
    """
    tiempos_respuesta = []
    uso_cpu = []
    uso_memoria = []

    for _ in range(cantidad_muestras):
        # Medir el tiempo de respuesta
        tiempo_respuesta, _ = medir_tiempo_respuesta(func, *args, **kwargs)
        tiempos_respuesta.append(tiempo_respuesta)
        
        # Medir el uso de recursos
        cpu, memoria = medir_uso_recursos()
        uso_cpu.append(cpu)
        uso_memoria.append(memoria)

    # Calcular medias
    media_tiempo_respuesta = np.mean(tiempos_respuesta)
    media_cpu = np.mean(uso_cpu)
    media_memoria = np.mean(uso_memoria)

    return media_tiempo_respuesta, media_cpu, media_memoria

# Funciones de prueba para simular las acciones en tu sistema (CRUD)
def crear_inspector():
    # Simula la creación de un inspector (puedes reemplazarlo con la lógica real)
    time.sleep(0.2)  # Simula un tiempo de espera
    return "Inspector creado"

def actualizar_inspector():
    # Simula la actualización de un inspector
    time.sleep(0.1)
    return "Inspector actualizado"

def borrar_inspector():
    # Simula la eliminación de un inspector
    time.sleep(0.15)
    return "Inspector borrado"

# Función principal para correr las pruebas y mostrar resultados
def ejecutar_metricas():
    # Métricas para la carga de cada página (puedes personalizar esta parte según las páginas de tu aplicación)
    print("Midiendo tiempo de respuesta y uso de recursos para cargar la página principal...")
    tiempo_respuesta_carga, cpu_carga, memoria_carga = obtener_metricas(cargar_pagina)

    # Métricas para el CRUD de inspectores
    print("Midiendo tiempo de respuesta y uso de recursos para crear un inspector...")
    tiempo_respuesta_crear, cpu_crear, memoria_crear = obtener_metricas(crear_inspector)

    print("Midiendo tiempo de respuesta y uso de recursos para actualizar un inspector...")
    tiempo_respuesta_actualizar, cpu_actualizar, memoria_actualizar = obtener_metricas(actualizar_inspector)

    print("Midiendo tiempo de respuesta y uso de recursos para borrar un inspector...")
    tiempo_respuesta_borrar, cpu_borrar, memoria_borrar = obtener_metricas(borrar_inspector)

    # Imprimir resultados
    print(f"Tiempo de respuesta al cargar la página: {tiempo_respuesta_carga} segundos")
    print(f"Uso promedio de CPU al cargar la página: {cpu_carga}%")
    print(f"Uso promedio de memoria al cargar la página: {memoria_carga}%\n")

    print(f"Tiempo de respuesta al crear un inspector: {tiempo_respuesta_crear} segundos")
    print(f"Uso promedio de CPU al crear un inspector: {cpu_crear}%")
    print(f"Uso promedio de memoria al crear un inspector: {memoria_crear}%\n")

    print(f"Tiempo de respuesta al actualizar un inspector: {tiempo_respuesta_actualizar} segundos")
    print(f"Uso promedio de CPU al actualizar un inspector: {cpu_actualizar}%")
    print(f"Uso promedio de memoria al actualizar un inspector: {memoria_actualizar}%\n")

    print(f"Tiempo de respuesta al borrar un inspector: {tiempo_respuesta_borrar} segundos")
    print(f"Uso promedio de CPU al borrar un inspector: {cpu_borrar}%")
    print(f"Uso promedio de memoria al borrar un inspector: {memoria_borrar}%\n")

# Simulación de la carga de una página
def cargar_pagina():
    # Simula la carga de una página
    time.sleep(0.3)  # Simula el tiempo de espera para cargar la página
    return "Página cargada"

# Ejecutar las métricas
if __name__ == "__main__":
    ejecutar_metricas()
