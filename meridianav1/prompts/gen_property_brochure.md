---
title: "Prompt: Generar ficha de propiedad pública"
doc_type: prompt
category: template
audience: internal_team
purpose: "Prompt canónico para generar fichas comerciales de propiedades desde properties.csv."
source:
  - properties.csv
  - property_features.csv
  - agents.csv
status: final
version: v01
date: 2026-06-14
entity: property
language: es
tags:
  - prompt
  - generacion
  - property_brochure
  - public
doc_id: prompt-gen-property-brochure
output_category: public
output_doc_type: property_brochure
output_path: "knowledge_base/public/properties/{property_id}.md"
---

# Prompt: Generar ficha de propiedad pública

## Propósito

Genera una ficha comercial en Markdown con frontmatter para una propiedad de Meridiana, usando los datos de `properties.csv`, `property_features.csv` y `agents.csv`. El documento resultante va en `knowledge_base/public/properties/`.

---

## Variables de entrada

Antes de ejecutar, sustituir:

- `{property_id}` — ej. `P001`
- `{row_properties}` — fila completa de `properties.csv` para esta propiedad
- `{rows_features}` — filas de `property_features.csv` donde `property_id` coincide y `is_public = sí`
- `{row_agent}` — fila de `agents.csv` donde `agent_id` coincide con el de la propiedad

---

## Prompt

```
Eres redactor comercial de Meridiana, una inmobiliaria boutique premium en Mérida, Yucatán. Tu tono es elegante, sobrio y preciso. No uses superlativos vacíos ni frases de relleno.

Con los siguientes datos, genera una ficha de propiedad en Markdown con frontmatter YAML completo.

### Datos de la propiedad
{row_properties}

### Características públicas
{rows_features}

### Datos del asesor
{row_agent}

### Instrucciones de formato

1. Frontmatter obligatorio:
   - title, doc_type: property_brochure, category: public, audience: client
   - purpose, source, status, version, date, entity: property, language: es
   - tags (municipio, colonia, tipo, operación, luxury_tier)
   - summary (máximo 150 caracteres, basado en public_description)
   - property_id, listing_code, listing_type, property_type, neighborhood, municipality, price, luxury_tier, agent_id

2. Cuerpo del documento:
   - H1: commercial_name
   - H3: title
   - Línea de identificación: listing_code · tipo en operación · colonia, municipio
   - Referencia a imagen: `![Render principal](../../properties/{property_id}/render1.png)`
   - Sección Precio: formateado con comas, indicar si es MXN/mes para rentas
   - Sección Características principales: tabla con recámaras, baños, construcción m², terreno m², estacionamientos, año, amueblado, mascotas, comunidad privada
   - Sección Descripción: usar public_description tal como está, sin modificar ni resumir
   - Sección Amenidades (solo si hay features públicas): agrupar por categoría
   - Sección Asesor responsable: nombre, email, teléfono
   - Footer: "Meridiana · Mérida · Yucatán · meridiana.mx"

3. Reglas de contenido:
   - NUNCA incluir internal_summary ni notas del propietario
   - NUNCA mencionar circunstancias del vendedor (divorcio, urgencia, precio mínimo)
   - Para propiedades con status = vendida o rentada: agregar nota "Esta propiedad ya no está disponible"
   - Para propiedades con status = borrador: NO generar ficha pública
   - El precio debe usar formato ${precio:,} MXN o ${precio:,} MXN/mes

Genera únicamente el documento Markdown. Sin explicaciones adicionales.
```

---

## Notas de uso

- Ejecutar una vez por propiedad o en lote con el script `scripts/generate_kb.py`
- Los campos `internal_summary` y `notes_internal` del CSV **nunca** deben aparecer en el output
- La imagen se referencia con ruta relativa desde `knowledge_base/public/properties/` hacia `properties/{property_id}/render1.png`
- Si `property_features.csv` no tiene features con `is_public = sí` para esa propiedad, omitir la sección de amenidades
