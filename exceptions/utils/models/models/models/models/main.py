from utils.logger import configurar_logger
from models.cliente import Cliente
from models.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from models.reserva import Reserva, SistemaGestionFJ
from exceptions.custom_exceptions import SoftwareFJError


def ejecutar_simulaciones():
    logger = configurar_logger()
    sistema = SistemaGestionFJ()
    logger.info("=== INICIANDO SISTEMA INTEGRAL SOFTWARE FJ (MODO EN MEMORIA) ===")

    # 1. Registro válido de Cliente (try / except / else)
    try:
        c1 = Cliente("CLI-01", "Laura Martínez", "laura.martinez@correo.com", "3104567890")
        sistema.registrar_cliente(c1)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 1] Error registrando cliente: {e}")
    else:
        logger.info(f"[Simulación 1 - ÉXITO] {c1.obtener_resumen()}")

    # 2. Registro inválido de Cliente (correo mal formado)
    try:
        c_invalido = Cliente("CLI-02", "Carlos Ruiz", "carlos.ruiz_sin_arroba.com", "3001234567")
        sistema.registrar_cliente(c_invalido)
    except SoftwareFJError as e:
        logger.warning(f"[Simulación 2 - ERROR CONTROLADO] Registro rechazado: {e}")

    # 3. Registro inválido con Encadenamiento de Excepciones (teléfono no numérico)
    try:
        c_tel_malo = Cliente("CLI-03", "Andrés Gómez", "andres@empresa.co", "315ABC99")
        sistema.registrar_cliente(c_tel_malo)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 3 - ENCADENAMIENTO] {e} | Causa original: {repr(e.__cause__)}")

    # 4. Registro válido de segundo Cliente
    try:
        c2 = Cliente("CLI-04", "Sofía Herrera", "sofia.h@techcol.com", "3209876543")
        sistema.registrar_cliente(c2)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 4] Error inesperado: {e}")
    else:
        logger.info(f"[Simulación 4 - ÉXITO] {c2.obtener_resumen()}")

    # 5. Creación válida de 3 Servicios Especializados (Polimorfismo)
    try:
        s1 = ReservaSala("SRV-01", "Sala Innovación Norte", 85000.0, capacidad=15, tiene_proyector=True)
        s2 = AlquilerEquipo("SRV-02", "Workstation Dell Precision i9", 45000.0, categoria_hw="Estación CAD/3D", stock=3)
        s3 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud & DevOps", 150000.0, area_experta="Nube Híbrida", senior=True)
        for srv in (s1, s2, s3):
            sistema.registrar_servicio(srv)
            logger.info(f"[Simulación 5 - SERVICIO CREADO] {srv.describir_servicio()}")
    except SoftwareFJError as e:
        logger.error(f"[Simulación 5] Error creando servicios: {e}")

    # 6. Creación incorrecta de Servicio (tarifa negativa)
    try:
        s_malo = ReservaSala("SRV-04", "Sala Fantasma", -25000.0, capacidad=5)
        sistema.registrar_servicio(s_malo)
    except SoftwareFJError as e:
        logger.warning(f"[Simulación 6 - ERROR CONTROLADO] Servicio inválido bloqueado: {e}")

    # 7. Creación de Servicio sin disponibilidad (stock = 0)
    try:
        s_agotado = AlquilerEquipo("SRV-05", "Servidor GPU NVIDIA A100", 220000.0, categoria_hw="IA/ML", stock=0)
        sistema.registrar_servicio(s_agotado)
        logger.info(f"[Simulación 7 - SERVICIO AGOTADO REGISTRADO] {s_agotado.obtener_resumen()}")
    except SoftwareFJError as e:
        logger.error(f"[Simulación 7] Error: {e}")

    # 8. Reserva Exitosa con cálculo estándar (try / except / else / finally)
    try:
        r1 = Reserva("RES-01", c1, s1, horas=4)
        r1.procesar_y_confirmar()
        sistema.registrar_reserva(r1)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 8] Fallo en reserva: {e}")
    else:
        logger.info(f"[Simulación 8 - RESERVA CONFIRMADA] {r1.obtener_resumen()}")
    finally:
        logger.debug("[Simulación 8 - FINALLY] Auditoría de transacción RES-01 finalizada.")

    # 9. Reserva Exitosa con sobrecarga completa (descuento 15% + recargo fijo)
    try:
        r2 = Reserva("RES-02", c2, s3, horas=3)
        r2.procesar_y_confirmar(impuesto_iva=0.19, descuento_porcentaje=15.0, recargo_fijo=30000.0)
        sistema.registrar_reserva(r2)
    except SoftwareFJError as e:
        logger.error(f"[Simulación 9] Fallo en reserva: {e}")
    else:
        logger.info(f"[Simulación 9 - RESERVA CON DESCUENTO] {r2.obtener_resumen()}")
    finally:
        logger.debug("[Simulación 9 - FINALLY] Auditoría de transacción RES-02 finalizada.")

    # 10. Reserva Fallida por Servicio No Disponible (stock 0)
    try:
        r3 = Reserva("RES-03", c1, s_agotado, horas=5)
        r3.procesar_y_confirmar()
        sistema.registrar_reserva(r3)
    except SoftwareFJError as e:
        logger.warning(f"[Simulación 10 - ERROR CONTROLADO] Intento sobre servicio agotado: {e}")

    # 11. Reserva Fallida por regla de negocio (alquiler equipo < 2 horas)
    try:
        r4 = Reserva("RES-04", c2, s2, horas=1)
        r4.procesar_y_confirmar()
    except SoftwareFJError as e:
        logger.warning(f"[Simulación 11 - ERROR CONTROLADO] Restricción horaria aplicada: {e}")

    # 12. Cálculo Inconsistente (descuento 150%) y Cancelación duplicada
    try:
        r5 = Reserva("RES-05", c1, s2, horas=3)
        r5.procesar_y_confirmar(descuento_porcentaje=150.0)
    except SoftwareFJError as e:
        logger.warning(f"[Simulación 12A - ERROR CONTROLADO] Cálculo inconsistente detectado: {e}")

    try:
        r1.cancelar("Cambio de agenda")
        logger.info(f"[Simulación 12B - CANCELACIÓN] {r1.obtener_resumen()}")
        r1.cancelar("Reintento erróneo")
    except SoftwareFJError as e:
        logger.warning(f"[Simulación 12B - ERROR CONTROLADO] Doble cancelación bloqueada: {e}")

    logger.info("=== RESUMEN DE ESTADO FINAL EN MEMORIA ===")
    logger.info(
        f"Clientes activos: {len(sistema.clientes)} | "
        f"Servicios catálogo: {len(sistema.servicios)} | "
        f"Reservas registradas: {len(sistema.reservas)}"
    )
    logger.info("=== EJECUCIÓN FINALIZADA SIN INTERRUPCIONES ===")


if __name__ == "__main__":
    ejecutar_simulaciones()
