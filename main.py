from datetime import date, datetime

# 1. Definición de las plantillas para los diccionarios

# Combo
plantilla_combo = {
    "id_combo": None, # identificador 
    "nombre": "", # nombre del combo
    "precio": 0.0, # precio en pesos
    "tiempo_preparacion": 0 # tiempo estimado de preparación en minutos
}

# Detalle de Pedido
plantilla_detalle = {
    "id_combo": None, # id del combo pedido
    "cantidad": 0 # cantidad de unidades de ese combo
}

# Pedido
plantilla_pedido = {
    "id_pedido": None, # identificador único del pedido
    "detalles": [], # lista de detalles (cada uno es un dict `plantilla_detalle`)
    "subtotal": 0.0, # suma de (precio * cantidad)
    "descuento": 0.0, # monto de descuento aplicado
    "total": 0.0, # subtotal - descuento
    "tiempo_estimado": 0, # tiempo total de preparación calculado
    "estado": "", # "en cola", "en cocina" o "entregado"
    "marca_tiempo": None # timestamp: “AAAA-MM-DD HH:MM:SS”
}

# Estadística diaria
plantilla_estadistica = {
    "id_estadistica": None, # id de la estadística del día
    "total_dinero": 0.0, # total recaudado
    "total_pedidos": 0, # conteo de pedidos realizados
    "por_combo": {}, # dict: {id_combo: cantidad_vendida}
    "fecha": date.today().isoformat() # fecha actual “AAAA-MM-DD”
}

# 2. Configuración de descuento

descuento = {
    "activo": True, # si el descuento está habilitado
    "tope_descuento": 100000.0, # umbral mínimo para aplicar descuento
    "porcentaje_descuento": 0.10 # porcentaje a descontar (p.ej. 0.10 = 10%)
}

# 3. "Tablas" en memoria

# Catálogo de combos
combos: dict[int, dict] = {
    1: {
        **plantilla_combo, # dictionary unpacking: clona la plantilla base
        "id_combo": 1,
        "nombre": "Combo de Tacos al Pastor",
        "precio": 42000.0,
        "tiempo_preparacion": 15
    },
    2: {
        **plantilla_combo,
        "id_combo": 2,
        "nombre": "Combo de Tacos de Birria",
        "precio": 42000.0,
        "tiempo_preparacion": 20
    },
    3: {
        **plantilla_combo,
        "id_combo": 3,
        "nombre": "Combo de Quesadillas",
        "precio": 35000.0,
        "tiempo_preparacion": 10
    },
}

pedidos: dict[int, dict] = {}
estatisticas_dia: dict[int, dict] = {}
fila: list[int] = []

# 4. Funciones
# Esta función limpia los pedidos, estadísticas y fila sin tocar combos ni descuento
def reiniciar_datos():
    pedidos.clear() # elimina todos los pedidos almacenados
    estatisticas_dia.clear() # borra las estadísticas acumuladas del día
    fila.clear() # vacía la lista de IDs en la fila de preparación