from datetime import date, datetime

# 1. Definición de las plantillas para los diccionarios

# Combo
plantilla_combo = {
    "id_combo": None, 
    "nombre": "", 
    "precio": 0.0, 
    "tiempo_preparacion": 0  # en minutos
}

# Detalle de Pedido
plantilla_detalle = {
    "id_combo": None,
    "cantidad": 0,
}

# Pedido
plantilla_pedido = {
    "id_pedido": None,
    "detalles": [],
    "subtotal": 0.0,
    "descuento": 0.0,
    "total": 0.0,
    "tiempo_estimado": 0,      # en minutos
    "estado": "",              # "en cola", "en cocina", "entregado"
    "marca_tiempo": None,      # “AAAA-MM-DD HH:MM:SS”
}

# Estadística diaria
plantilla_estadistica = {
    "id_estadistica": None,
    "total_dinero": 0.0,
    "total_pedidos": 0,
    "por_combo": {},
    "fecha": date.today().isoformat(),  # “AAAA-MM-DD”
}

# 2. Configuración de descuento

descuento = {
    "activo": True,
    "tope_descuento": 100000.0,
    "porcentaje_descuento": 0.10,
}

# 3. “Tablas” en memoria

combos: dict[int, dict] = {}  
pedidos: dict[int, dict] = {}
estadisticas_dia: dict[int, dict] = {}
fila: list[int] = []

# 4. Funciones

# Reiniciar datos
def reiniciar_datos()
    combos.clear()
    pedidos.clear()
    estadisticas_dia.clear()
    fila.clear()