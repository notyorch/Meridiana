# Valores de estado

## Propósito

Este documento define los estados estándar que puede usar el sistema documental y operativo de Meridiana. La idea es mantener una propuesta simple, consistente y realista para una inmobiliaria promedio, sin crear demasiadas variantes. La clasificación toma como base los estados ya presentes en los datasets y la lógica operativa del proyecto. [file:3][file:2]

## Estados de documentos

- `draft`: Documento en elaboración. Puede cambiar en contenido, estructura o tono.
- `review`: Documento listo para revisión interna antes de publicarse o cerrarse.
- `final`: Versión aprobada y lista para uso.
- `template`: Plantilla reutilizable que aún no es un documento final.
- `archived`: Documento descontinuado o reemplazado por una versión más reciente.

## Estados de propiedad o listing

Los datasets usan estados como `activa`, `apartada`, `vendida`, `rentada` y `borrador`, por lo que conviene conservar una lógica cercana y fácil de entender. [file:3]

- `borrador`: La propiedad todavía no está lista para publicación.
- `activa`: La propiedad está publicada y disponible.
- `apartada`: Hay una intención fuerte de cierre o reserva temporal.
- `vendida`: La operación de venta ya se concretó.
- `rentada`: La operación de renta ya se concretó.
- `inactiva`: La propiedad ya no se promociona, pero no está cerrada como vendida o rentada.

## Estados de lead

Los leads del dataset se manejan con una lógica sencilla de avance comercial. [file:3]

- `nuevo`: Lead recién captado y todavía sin contacto útil.
- `en_contacto`: Ya existe conversación inicial y se está recolectando información.
- `calificado`: El lead tiene presupuesto, intención y perfil suficientemente claros.
- `descartado`: No encaja con el inventario, el presupuesto o el momento de compra.
- `seguimiento`: Lead con interés real que requiere seguimiento activo antes de avanzar.

## Estados de versión

Si el documento necesita control de cambios, estos estados son suficientes para una pyme. [file:2][file:3]

- `draft`: Primera versión en desarrollo.
- `review`: Versión en validación.
- `approved`: Versión autorizada para uso.
- `superseded`: Versión reemplazada por otra más reciente.
- `archived`: Versión histórica conservada por referencia.

## Recomendación general

Para Meridiana conviene mantener pocos estados, bien entendidos por todo el equipo, y evitar duplicar significados entre documento, versión y operación comercial. Si un estado no ayuda a decidir qué hacer con el archivo o el registro, probablemente no hace falta. La prioridad es legibilidad operativa y consistencia entre personas y herramientas. [file:2][file:3]
