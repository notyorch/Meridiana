# Especificación de frontmatter

## Propósito

Este documento define el frontmatter mínimo que deben llevar los documentos Markdown de Meridiana. El objetivo es estandarizar metadatos para facilitar búsqueda, clasificación y reutilización sin volver el sistema pesado. La propuesta se apoya en la estructura del proyecto, el CRM sintético y el tono editorial sobrio de la marca. [file:2][file:3][file:1]

## Campos obligatorios

| Campo | Tipo sugerido | Descripción |
|---|---|---|
| `title` | string | Título legible del documento. |
| `doc_type` | string | Tipo documental, por ejemplo `company_profile`, `property_brochure`, `lead_memo`. |
| `category` | string | Categoría general, por ejemplo `public`, `internal`, `restricted`, `template`. |
| `audience` | string | Audiencia principal del documento, por ejemplo `client`, `agent`, `owner`, `internal_team`. |
| `purpose` | string | Breve descripción de para qué sirve el documento. |
| `source` | array[string] o string | Fuentes de datos o archivos usados para construirlo. |
| `status` | string | Estado del documento, por ejemplo `draft`, `final`, `template`. |
| `version` | string | Versión del documento, por ejemplo `v01`. |
| `date` | date | Fecha de creación o actualización principal. |

## Campos opcionales

| Campo | Tipo sugerido | Descripción |
|---|---|---|
| `entity` | string | Entidad principal relacionada, por ejemplo `property`, `lead`, `owner`, `agent`. |
| `language` | string | Idioma del documento, normalmente `es`. |
| `tags` | array[string] | Etiquetas para búsqueda y clasificación. |
| `summary` | string | Resumen corto del contenido. |
| `owner` | string | Persona o área responsable del documento. |
| `related_docs` | array[string] | Documentos vinculados o versiones relacionadas. |
| `updated_at` | date | Fecha de última actualización. |
| `doc_id` | string | Identificador interno único si se necesita trazabilidad. |

## Reglas prácticas

- Mantener los campos en minúsculas y con nombres consistentes.
- Usar valores cortos y estables.
- No duplicar en el frontmatter información que ya aparece en el cuerpo.
- Usar `source` para dejar claro de dónde salió el contenido.
- Usar `tags` solo cuando ayuden a buscar mejor, no para llenar espacio.
- Si el documento es plantilla, marcar `status: template`.

## Ejemplo de frontmatter

```yaml
---
title: "Ficha de propiedad: Casa en Temozón Norte"
doc_type: property_brochure
category: public
audience: client
purpose: "Presentar una propiedad en formato comercial claro y elegante."
source:
  - properties.csv
  - property_features.csv
status: final
version: v01
date: 2026-06-14
entity: property
language: es
tags:
  - merida
  - temozon_norte
  - casa
  - venta
summary: "Ficha comercial de una casa premium en Temozón Norte con datos clave para publicación."
owner: "equipo comercial"
related_docs:
  - property_web_listing_longform_v01.md
  - property_brochure_template_v01.md
updated_at: 2026-06-14
doc_id: doc-0001
---
```

## Recomendación de uso

Para un equipo pequeño, este frontmatter es suficiente para ordenar archivos, filtrar por categoría y encontrar documentos por entidad o etiqueta. Si en el futuro el sistema crece, se pueden agregar campos sin romper la compatibilidad de los documentos existentes. La clave es mantener una estructura simple, estable y fácil de llenar manualmente o con scripts. [file:2][file:3]
