# Source map

## Propósito

Este archivo conecta los datasets de Meridiana con los tipos de documentos que pueden generarse a partir de ellos. La intención es dejar claro qué CSV alimenta cada plantilla o documento, y qué dependencias existen entre tablas para construir materiales consistentes. La guía se basa en el esquema documentado del README y en la estructura general del proyecto. [file:3][file:2]

## Mapa de fuentes por documento

| Dataset | Datos principales | Documentos o plantillas que alimenta | Dependencias obvias |
|---|---|---|---|
| `properties.csv` | Identificador de propiedad, tipo, precio, ubicación, metraje, estado, descripción pública e interna. | Property brochure, property web listing longform, company profile, internal property memo, comparativos de inventario. | Se relaciona con `agents.csv`, `owners.csv`, `property_features.csv`, `viewings.csv` y `offers.csv`. [file:3] |
| `agents.csv` | Nombre, rol, especialidad, idiomas, jerarquía, comisión y actividad. | Agent profile, directorio del equipo, company profile, asignación comercial, firmas internas. | Se relaciona con `properties.csv`, `leads.csv`, `interactions.csv`, `viewings.csv` y `offers.csv`. [file:3] |
| `owners.csv` | Nombre del propietario, tipo, contacto, canal preferido, confidencialidad y notas internas. | Owner profile, internal ownership memo, confidential property strategy memo, property intake summary. | Se relaciona con `properties.csv`. [file:3] |
| `leads.csv` | Nombre del prospecto, fuente, presupuesto, zona de interés, tipo de propiedad, timeline, score y notas. | Lead qualification memo, buyer FAQ response log, prospect profile, follow-up summary. | Se relaciona con `agents.csv`, `interactions.csv`, `viewings.csv` y `offers.csv`. [file:3] |
| `interactions.csv` | Fecha, canal, dirección, resumen, sentimiento, intención, siguiente acción y visibilidad. | Interaction log, CRM narrative, lead follow-up memo, sales chronology, internal case summary. | Se relaciona con `leads.csv`, `agents.csv` y, a veces, `properties.csv`. [file:3] |
| `viewings.csv` | Fecha de visita, tipo, estado, feedback, nivel de interés, objeciones y seguimiento requerido. | Viewing summary, post-visit memo, buyer interest report, internal follow-up plan. | Se relaciona con `properties.csv`, `leads.csv` y `agents.csv`. [file:3] |
| `offers.csv` | Monto ofertado, fecha, estatus, contraoferta, ventana de cierre, depósito y notas internas. | Negotiation notes, offer history, closing memo, internal strategy memo. | Se relaciona con `properties.csv`, `leads.csv` y `agents.csv`. [file:3] |
| `property_features.csv` | Nombre de feature, categoría, valor descriptivo e indicador de publicación. | Property brochure, web listing longform, feature inventory, comparative property sheet, amenity highlights. | Se relaciona exclusivamente con `properties.csv`. [file:3] |

## Documentos compuestos

Algunos documentos se construyen mejor con más de un dataset. Esto ayuda a que el contenido final no quede fragmentado y refleje mejor la operación real de Meridiana. [file:3]

| Documento | Datasets principales | Uso combinado |
|---|---|---|
| Property brochure | `properties.csv` + `property_features.csv` | Resume la propiedad y destaca atributos relevantes. |
| Property web listing longform | `properties.csv` + `property_features.csv` | Genera una ficha extensa con lenguaje comercial. |
| Lead qualification memo | `leads.csv` + `interactions.csv` | Une perfil declarado y contexto conversacional. |
| Viewing summary | `viewings.csv` + `properties.csv` + `leads.csv` | Explica qué se visitó, quién asistió y qué ocurrió. |
| Negotiation notes | `offers.csv` + `properties.csv` + `leads.csv` | Reúne oferta, contraoferta y contexto comercial. |
| Owner profile | `owners.csv` + `properties.csv` | Muestra relación del propietario con su inmueble. |
| Agent profile | `agents.csv` + `properties.csv` | Describe al asesor y su cartera o especialidad. |
| Company profile | `agents.csv` + `properties.csv` + `owners.csv` | Permite presentar equipo, cartera y tipo de operación. |

## Dependencias recomendadas

- `properties.csv` es la base más importante porque conecta gran parte del sistema documental. [file:3]
- `property_features.csv` enriquece las descripciones de `properties.csv` y permite fichas más completas. [file:3]
- `leads.csv`, `interactions.csv`, `viewings.csv` y `offers.csv` forman el ciclo comercial completo de atención y cierre. [file:3]
- `owners.csv` es clave para documentos de cartera y estrategia, aunque no siempre aparezca en materiales públicos. [file:3]
- `agents.csv` da identidad al equipo y permite atribuir documentos a responsables concretos. [file:3]

## Regla práctica

Si un documento habla de una propiedad, casi siempre debe empezar por `properties.csv` y luego sumar `property_features.csv` si necesita detalle. Si habla de un cliente o prospecto, la base será `leads.csv`, complementada por `interactions.csv`, `viewings.csv` o `offers.csv` según el momento comercial. Si habla del equipo o de la operación, `agents.csv` y `owners.csv` suelen aportar el contexto necesario. [file:3][file:2]
