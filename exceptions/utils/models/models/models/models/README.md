# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ

**Curso:** Programación (Código: 213023) — UNAD  
**Fase:** 4 — Componente Práctico (Prácticas Simuladas)  
**Lenguaje:** Python 3.10+ (Sin dependencias externas ni motores de base de datos)

## Descripción General
Aplicación modular orientada a objetos que gestiona clientes, catálogo de servicios especializados (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) y reservas en memoria mediante colecciones internas, garantizando tolerancia a fallos y trazabilidad completa en archivos de registro (`logs/sistema_fj.log`).

## Arquitectura y Principios Aplicados
1. **Abstracción:** Clases abstractas `EntidadBase` y `Servicio` implementadas con el módulo estándar `abc`.
2. **Encapsulación:** Atributos privados (`_nombre`, `_correo`, `_telefono`, `_estado`) protegidos con propiedades y validaciones estrictas en setters.
3. **Herencia y Polimorfismo:** Tres clases derivadas de `Servicio` que sobrescriben `describir_servicio()` y `validar_parametros_operacion()`.
4. **Sobrecarga de Métodos:** `Servicio.calcular_costo()` admite cálculos base, impuestos variables, descuentos porcentuales y recargos fijos opcionales.
5. **Manejo Avanzado de Excepciones:** Jerarquía personalizada (`SoftwareFJError`), bloques `try/except`, `try/except/else`, `try/except/finally` y encadenamiento (`raise ... from e`).

## Instrucciones de Ejecución
1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/fredygarzon06/UNAD-Programacion-213023-Fase4-SoftwareFJ.git](https://github.com/fredygarzon06/UNAD-Programacion-213023-Fase4-SoftwareFJ.git)
   cd UNAD-Programacion-213023-Fase4-SoftwareFJ
