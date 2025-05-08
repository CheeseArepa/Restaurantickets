from dataclasses import dataclass, field
from typing import List, Dict
from datetime import date, datetime

@dataclass
class Combo:
    id_combo: int
    nombre: str
    precio: float
    tiempo_preparacion: int  # en minutos

descuento = {
    "activo": True,
    "tope_descuento": 100000.0,
    "porcentaje_descuento": 0.10,
}

@dataclass
class DetallePedido:
    id_combo: int
    cantidad: int

@dataclass
class Pedido:
    id_pedido: int
    detalles: List[DetallePedido]
    subtotal: float
    descuento: float
    total: float
    tiempo_estimado: int      # en minutos
    estado: str               # "en cola", "en cocina", "entregado"
    marca_tiempo: datetime

@dataclass
class EstadisticaDia:
    id_estadistica: int
    total_dinero: float
    total_pedidos: int
    por_combo: Dict[int, int] = field(default_factory=dict)
    fecha: date = date.today()

# Estructuras de almacenamiento en memoria
combos: Dict[int, Combo]          = {}
pedidos: Dict[int, Pedido]        = {}
estadisticas_dia: Dict[int, EstadisticaDia] = {}
fila: List[int]                   = []