from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Cliente(BaseModel):
    id: str = Field(..., description="ID único del cliente, formato: cliente_XXX")
    nombre: str = Field(..., description="Nombre del cliente")
    telefono: str = Field(..., description="Teléfono del cliente")
    monto_deuda_inicial: float = Field(..., description="Monto inicial de la deuda")
    fecha_prestamo: datetime = Field(..., description="Fecha del préstamo")
    tipo_deuda: str = Field(..., description="Tipo de deuda: tarjeta_credito, prestamo_personal, hipoteca, auto")

class Interaccion(BaseModel):
    id: str = Field(..., description="ID único de la interacción")
    cliente_id: str = Field(..., description="ID del cliente relacionado")
    timestamp: datetime = Field(..., description="Fecha y hora de la interacción")
    tipo: str = Field(..., description="Tipo de interacción: llamada_saliente, llamada_entrante, email, sms, pago_recibido")
    duracion_segundos: Optional[int] = Field(None, description="Duración de la llamada en segundos")
    agente_id: Optional[str] = Field(None, description="ID del agente que realizó la interacción")
    resultado: Optional[str] = Field(None, description="Resultado de la interacción")
    sentimiento: Optional[str] = Field(None, description="Sentimiento detectado en la interacción")
    monto_prometido: Optional[float] = Field(None, description="Monto prometido en una promesa de pago")
    fecha_promesa: Optional[datetime] = Field(None, description="Fecha de la promesa de pago")
    monto: Optional[float] = Field(None, description="Monto pagado en la interacción")
    metodo_pago: Optional[str] = Field(None, description="Método de pago")
    pago_completo: Optional[bool] = Field(None, description="Si el pago fue completo")
    # Relación a PlanPago si resultado == "renegociacion"
    # Relación a PromesaPago si resultado == "promesa_pago"

class Agente(BaseModel):
    id: str = Field(..., description="ID del agente")

class PlanPago(BaseModel):
    cuotas: int = Field(..., description="Cantidad de cuotas del plan de pago")
    monto_mensual: float = Field(..., description="Monto mensual del plan de pago")

class Pago(BaseModel):
    monto: float = Field(..., description="Monto pagado")
    metodo_pago: str = Field(..., description="Método de pago")
    pago_completo: bool = Field(..., description="Si el pago fue completo")

class PromesaPago(BaseModel):
    monto_prometido: float = Field(..., description="Monto prometido en la promesa de pago")
    fecha_promesa: datetime = Field(..., description="Fecha de la promesa de pago")

# Edges

class TieneInteraccion(BaseModel):
    pass

class RealizadaPor(BaseModel):
    pass

class ProponePlan(BaseModel):
    pass

class RealizaPago(BaseModel):
    pass

class ConcretadaCon(BaseModel):
    pass

class Metadata(BaseModel):
    fecha_generacion: datetime = Field(..., description="Fecha de generación del archivo")
    total_clientes: int = Field(..., description="Cantidad total de clientes")
    total_interacciones: int = Field(..., description="Cantidad total de interacciones")
    periodo: str = Field(..., description="Periodo de los datos")

class InteraccionesClientes(BaseModel):
    metadata: Metadata = Field(..., description="Metadatos del lote de datos")
    clientes: List[Cliente] = Field(..., description="Lista de clientes")
    interacciones: List[Interaccion] = Field(..., description="Lista de interacciones")