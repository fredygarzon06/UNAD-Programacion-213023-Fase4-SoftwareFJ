from typing import List, Optional
from models.base import EntidadBase
from models.cliente import Cliente
from models.servicios import Servicio
from exceptions.custom_exceptions import (
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    DatoInvalidoError
)


class Reserva(EntidadBase):
    """Integra un Cliente, un Servicio y gestiona el estado y costo de la reserva."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, horas: int):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente) or not cliente.activo:
            raise ReservaInvalidaError("La reserva requiere un cliente válido y activo.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio asociado no es válido.")
        if not isinstance(horas, int) or horas <= 0:
            raise DatoInvalidoError(f"La duración en horas debe ser un entero positivo (recibido: {horas}).")

        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def procesar_y_confirmar(
        self,
        impuesto_iva: float = 0.19,
        descuento_porcentaje: float = 0.0,
        recargo_fijo: Optional[float] = None
    ) -> float:
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError(f"No se puede confirmar la reserva {self._id} porque ya fue cancelada.")
        if self._estado == "CONFIRMADA":
            raise ReservaInvalidaError(f"La reserva {self._id} ya se encuentra confirmada.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' no está disponible para confirmar.")

        self._costo_total = self._servicio.calcular_costo(
            horas=self._horas,
            impuesto_iva=impuesto_iva,
            descuento_porcentaje=descuento_porcentaje,
            recargo_fijo=recargo_fijo
        )
        self._estado = "CONFIRMADA"
        return self._costo_total

    def cancelar(self, motivo: str = "Solicitud del cliente") -> None:
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self._id} ya estaba cancelada previamente.")
        self._estado = "CANCELADA"

    def validar(self) -> bool:
        return self._estado in self.ESTADOS_VALIDOS and self._horas > 0

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self._id}] | Estado: {self._estado} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} ({self._horas}h) | Total: ${self._costo_total:,.2f}"
        )


class SistemaGestionFJ:
    """Controlador en memoria (sin BD) con listas internas para clientes, servicios y reservas."""

    def __init__(self):
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []

    def registrar_cliente(self, cliente: Cliente) -> None:
        if any(c.id == cliente.id for c in self.clientes):
            raise DatoInvalidoError(f"Ya existe un cliente registrado con el ID '{cliente.id}'.")
        self.clientes.append(cliente)

    def registrar_servicio(self, servicio: Servicio) -> None:
        if any(s.id == servicio.id for s in self.servicios):
            raise DatoInvalidoError(f"Ya existe un servicio registrado con el ID '{servicio.id}'.")
        self.servicios.append(servicio)

    def registrar_reserva(self, reserva: Reserva) -> None:
        if any(r.id == reserva.id for r in self.reservas):
            raise ReservaInvalidaError(f"Ya existe una reserva con el ID '{reserva.id}'.")
        self.reservas.append(reserva)
