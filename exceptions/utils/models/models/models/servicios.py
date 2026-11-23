from abc import abstractmethod
from typing import Optional
from models.base import EntidadBase
from exceptions.custom_exceptions import (
    DatoInvalidoError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError
)


class Servicio(EntidadBase):
    """Clase abstracta que modela los servicios ofrecidos por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise DatoInvalidoError("El nombre del servicio no puede estar vacío.")
        if tarifa_hora <= 0:
            raise DatoInvalidoError(f"La tarifa por hora ({tarifa_hora}) debe ser mayor a cero.")

        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    @abstractmethod
    def validar_parametros_operacion(self, horas: int) -> None:
        pass

    def calcular_costo(
        self,
        horas: int,
        impuesto_iva: float = 0.19,
        descuento_porcentaje: float = 0.0,
        recargo_fijo: Optional[float] = None
    ) -> float:
        """
        Método sobrecargado mediante parámetros opcionales para calcular costos:
        - Base (solo horas)
        - Con impuestos personalizados
        - Con descuentos promocionales
        - Con recargos adicionales opcionales
        """
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' no se encuentra disponible.")

        self.validar_parametros_operacion(horas)

        if not (0 <= descuento_porcentaje <= 100):
            raise CalculoInconsistenteError(f"Porcentaje de descuento fuera de rango: {descuento_porcentaje}%.")
        if impuesto_iva < 0:
            raise CalculoInconsistenteError(f"El impuesto IVA no puede ser negativo: {impuesto_iva}.")

        subtotal = self._tarifa_hora * horas
        if recargo_fijo is not None:
            if recargo_fijo < 0:
                raise CalculoInconsistenteError("El recargo fijo no puede ser negativo.")
            subtotal += recargo_fijo

        valor_descuento = subtotal * (descuento_porcentaje / 100.0)
        base_gravable = subtotal - valor_descuento

        if base_gravable < 0:
            raise CalculoInconsistenteError("La base gravable resultó negativa tras aplicar descuentos.")

        total = base_gravable * (1 + impuesto_iva)
        return round(total, 2)

    def validar(self) -> bool:
        return self._tarifa_hora > 0

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self._disponible else "No Disponible"
        return f"[{self._id}] {self._nombre} | ${self._tarifa_hora:,.2f}/h | {estado}"


class ReservaSala(Servicio):
    """Servicio especializado para alquiler de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, tiene_proyector: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a 0 personas.")
        self._capacidad = capacidad
        self._tiene_proyector = tiene_proyector

    def validar_parametros_operacion(self, horas: int) -> None:
        if horas < 1 or horas > 12:
            raise DatoInvalidoError(f"Las salas solo se reservan entre 1 y 12 horas (solicitado: {horas}h).")

    def describir_servicio(self) -> str:
        proyector = "con proyector 4K" if self._tiene_proyector else "sin proyector"
        return f"Sala '{self._nombre}' (Capacidad: {self._capacidad} pax, {proyector}) - ${self._tarifa_hora:,.2f}/h"


class AlquilerEquipo(Servicio):
    """Servicio especializado para préstamo de hardware y estaciones de trabajo."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, categoria_hw: str, stock: int):
        super().__init__(id_servicio, nombre, tarifa_hora, disponible=(stock > 0))
        if stock < 0:
            raise DatoInvalidoError("El stock inicial del equipo no puede ser negativo.")
        self._categoria_hw = categoria_hw
        self._stock = stock

    def validar_parametros_operacion(self, horas: int) -> None:
        if self._stock <= 0:
            raise ServicioNoDisponibleError(f"Sin unidades en inventario para '{self._nombre}'.")
        if horas < 2:
            raise DatoInvalidoError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def describir_servicio(self) -> str:
        return f"Equipo '{self._nombre}' [{self._categoria_hw}] (Stock: {self._stock}) - ${self._tarifa_hora:,.2f}/h"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría en ingeniería y desarrollo."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, area_experta: str, senior: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora)
        if not area_experta:
            raise DatoInvalidoError("Debe especificar el área de especialidad de la asesoría.")
        self._area_experta = area_experta
        self._senior = senior

    def validar_parametros_operacion(self, horas: int) -> None:
        if horas <= 0:
            raise DatoInvalidoError("La duración de la asesoría debe ser de al menos 1 hora.")

    def describir_servicio(self) -> str:
        nivel = "Consultor Senior" if self._senior else "Consultor Semi-Senior"
        return f"Asesoría '{self._nombre}' en {self._area_experta} ({nivel}) - ${self._tarifa_hora:,.2f}/h"
