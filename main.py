from datetime import date, datetime

# 1. Definición de las plantillas para los diccionarios

# Combo
plantilla_combo = {
    "id_combo": None,       # identificador
    "nombre": "",           # nombre del combo
    "precio": 0.0,          # precio en pesos
    "tiempo_preparacion": 0 # tiempo estimado de preparación en minutos
}

# Detalle de Pedido
plantilla_detalle = {
    "id_combo": None,       # id del combo pedido
    "cantidad": 0           # cantidad de unidades de ese combo
}

# Pedido
plantilla_pedido = {
    "id_pedido": None,      # identificador único del pedido
    "detalles": [],         # lista de detalles (cada uno es un dict `plantilla_detalle`)
    "subtotal": 0.0,        # suma de (precio * cantidad)
    "descuento": 0.0,       # monto de descuento aplicado
    "total": 0.0,           # subtotal - descuento
    "tiempo_estimado": 0,   # tiempo total de preparación calculado
    "estado": "",           # "en cola", "en cocina" o "entregado"
    "marca_tiempo": None    # timestamp: “AAAA-MM-DD HH:MM:SS”
}

# Estadística diaria
plantilla_estadistica = {
    "id_estadistica": None,     # id de la estadística del día
    "total_dinero": 0.0,        # total recaudado
    "total_pedidos": 0,         # conteo de pedidos realizados
    "por_combo": {},            # dict: {id_combo: cantidad_vendida}
    "fecha": date.today().isoformat()  # fecha actual “AAAA-MM-DD”
}

# 2. Configuración de descuento
descuento = {
    "activo": True,             # si el descuento está habilitado
    "tope_descuento": 100000.0, # umbral mínimo para aplicar descuento
    "porcentaje_descuento": 0.10# porcentaje a descontar (p.ej. 0.10 = 10%)
}

# 3. "Tablas" en memoria
combos: dict[int, dict] = {
    1: {**plantilla_combo, "id_combo": 1, "nombre": "Combo de Tacos al Pastor", "precio": 42000.0, "tiempo_preparacion": 15},
    2: {**plantilla_combo, "id_combo": 2, "nombre": "Combo de Tacos de Birria", "precio": 42000.0, "tiempo_preparacion": 20},
    3: {**plantilla_combo, "id_combo": 3, "nombre": "Combo de Quesadillas",      "precio": 35000.0, "tiempo_preparacion": 10},
}
pedidos: dict[int, dict] = {}
estadisticas_dia: dict[int, dict] = {}
fila: list[int] = []

global id_pedido_counter
id_pedido_counter = 0

# 4. Funciones
def reiniciar_datos():
    """
    Limpia los pedidos, estadísticas y fila sin tocar combos ni descuento.
    """
    pedidos.clear()
    estadisticas_dia.clear()
    fila.clear()
    print("Datos reiniciados correctamente.")

def listar_combos():
    """
    Muestra los combos disponibles con id, nombre, precio y tiempo de preparación.
    """
    print("\n--- Combos disponibles ---")
    for c in combos.values():
        print(f"ID: {c['id_combo']}, Nombre: {c['nombre']}, Precio: {c['precio']:.2f} pesos, Tiempo: {c['tiempo_preparacion']} min")

def leer_entero(prompt: str, minimo: int = None, maximo: int = None) -> int:
    """
    Lee un entero, repitiendo hasta que el usuario ingrese un número válido
    y opcionalmente dentro de un rango especificado.
    """
    while True:
        try:
            valor = int(input(prompt))
            if (minimo is not None and valor < minimo) or (maximo is not None and valor > maximo):
                print("Número fuera de rango. Intenta de nuevo.")
            else:
                return valor
        except ValueError:
            print("Entrada no válida. Debes ingresar un número entero.")

def mostrar_menu() -> int:
    """
    Imprime el menú de opciones y devuelve la elección del usuario (1-5).
    """
    print("\n===== MENÚ DE OPCIONES =====")
    print("1. Registrar orden")
    print("2. Ver fila")
    print("3. Ver estadísticas")
    print("4. Reiniciar datos")
    print("5. Salir")
    print("============================\n")
    return leer_entero("Seleccione una opción (1-5): ", minimo=1, maximo=5)

def generar_id_pedido():
    """Genera un ID único incremental."""
    global id_pedido_counter
    id_pedido_counter += 1
    return id_pedido_counter


def calcular_descuento(subtotal: float) -> float:
    """Calcula descuento si aplica."""
    if descuento.get("activo") and subtotal >= descuento.get("tope_descuento", float('inf')):
        return subtotal * descuento.get("porcentaje_descuento", 0)
    return 0.0

def crear_pedido():
    """Solicita combo y cantidad, calcula subtotal, ID y timestamp."""
    listar_combos()
    # Selección combo
    while True:
        id_combo = leer_entero("Ingrese el ID del combo: ")
        if id_combo in combos:
            break
        print("ID inválido. Intente de nuevo.")
    cantidad = leer_entero("Cantidad de unidades: ", minimo=1)
    combo = combos[id_combo]
    subtotal = combo['precio'] * cantidad
    monto_desc = calcular_descuento(subtotal)
    total = subtotal - monto_desc
    nuevo_id = generar_id_pedido()
    marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    detalle = {**plantilla_detalle, 'id_combo': id_combo, 'cantidad': cantidad}
    return nuevo_id, detalle, subtotal, monto_desc, total, marca_tiempo

def añadir_a_cola(id_pedido: int):
    """Inserta el pedido en la cola y marca estado."""
    fila.append(id_pedido)

def calcular_tiempo_estimado():
    """Suma tiempos de preparación de todos los pedidos en fila."""
    total_min = 0
    for pid in fila:
        pedido = pedidos.get(pid)
        if pedido:
            total_min += pedido['tiempo_estimado']
    return total_min

def guardar_pedido(id_pedido, detalle, subtotal, descuento_monto, total, tiempo_estimado, marca_tiempo):
    """Guarda el pedido completo en el dict pedidos y actualiza estadísticas."""
    pedido = {
        **plantilla_pedido,
        'id_pedido': id_pedido,
        'detalles': [detalle],
        'subtotal': subtotal,
        'descuento': descuento_monto,
        'total': total,
        'tiempo_estimado': tiempo_estimado,
        'estado': 'en cola',
        'marca_tiempo': marca_tiempo
    }
    pedidos[id_pedido] = pedido

