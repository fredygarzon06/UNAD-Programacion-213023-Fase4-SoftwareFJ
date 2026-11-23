class SoftwareFJError(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""
    pass


class DatoInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos ingresados no cumplen el formato o rango esperado."""
    pass


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio."""
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando el servicio está inactivo o sin cupo/stock."""
    pass


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza ante conflictos de estado, duración inválida o clientes no aptos."""
    pass


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un descuento, impuesto o tarifa genera valores negativos o incoherentes."""
    pass
