import re
from models.base import EntidadBase
from exceptions.custom_exceptions import DatoInvalidoError, ParametroFaltanteError


class Cliente(EntidadBase):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self._activo = True
        self.validar()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError(f"El nombre '{valor}' es inválido (mínimo 3 caracteres).")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor:
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, valor):
            raise DatoInvalidoError(f"Formato de correo electrónico inválido: '{valor}'.")
        self._correo = valor.lower()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        try:
            digitos = str(valor).strip()
            int(digitos)
            if len(digitos) < 7:
                raise ValueError("Longitud insuficiente")
            self._telefono = digitos
        except ValueError as e:
            raise DatoInvalidoError(
                f"Teléfono inválido '{valor}': debe contener solo números (mín. 7 dígitos)."
            ) from e

    @property
    def activo(self) -> bool:
        return self._activo

    def validar(self) -> bool:
        if not self._id or not self._id.strip():
            raise ParametroFaltanteError("El ID del cliente no puede estar vacío.")
        return True

    def obtener_resumen(self) -> str:
        return f"Cliente [{self._id}] - {self._nombre} ({self._correo})"
