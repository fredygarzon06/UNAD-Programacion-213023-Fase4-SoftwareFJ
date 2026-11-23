from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    """Clase abstracta que representa las entidades generales del sistema."""

    def __init__(self, id_entidad: str):
        self._id = id_entidad
        self._fecha_creacion = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @abstractmethod
    def validar(self) -> bool:
        """Método abstracto obligatorio para validar la integridad de la entidad."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto para representar la entidad de forma legible."""
        pass
