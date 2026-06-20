---
title: "Prompt: Generar perfil de propietario"
doc_type: prompt
category: template
audience: internal_team
purpose: "Prompt canónico para generar perfiles de propietarios con enrutamiento automático por nivel de confidencialidad."
source:
  - owners.csv
  - properties.csv
status: final
version: v01
date: 2026-06-14
entity: owner
language: es
tags:
  - prompt
  - generacion
  - owner_profile
  - internal
  - restricted
doc_id: prompt-gen-owner-profile
output_category: "internal (conf. baja/media) · restricted (conf. alta/muy alta)"
output_doc_type: owner_profile
output_path: "knowledge_base/internal/owners/{owner_id}.md ó knowledge_base/restricted/owners/{owner_id}.md"
---

# Prompt: Generar perfil de propietario

## Propósito

Genera una ficha interna del propietario. El nivel de confidencialidad del CSV determina automáticamente si el documento va a `internal/owners/` (baja, media) o `restricted/owners/` (alta, muy alta).

---

## Variables de entrada

- `{owner_id}` — ej. `OWN-011`
- `{row_owner}` — fila de `owners.csv`
- `{rows_properties}` — filas de `properties.csv` donde `owner_id` coincide

---

## Regla de enrutamiento por confidencialidad

| Nivel en CSV | Categoría del doc | Audiencia | Carpeta de salida |
|---|---|---|---|
| `baja` | internal | agent | `internal/owners/` |
| `media` | internal | agent | `internal/owners/` |
| `alta` | restricted | director | `restricted/owners/` |
| `muy alta` | restricted | director | `restricted/owners/` |

---

## Prompt

```
Eres coordinador de relaciones con propietarios de Meridiana. Genera un perfil de propietario en Markdown con frontmatter YAML. Aplica el nivel de advertencia correcto según el nivel de confidencialidad.

### Datos del propietario
{row_owner}

### Propiedades vinculadas
{rows_properties}

### Instrucciones de formato

1. Frontmatter obligatorio:
   - title: "Perfil de propietario: {owner_name} ({owner_id})"
   - doc_type: owner_profile
   - category: "internal" si confidentiality_level es baja o media; "restricted" si es alta o muy alta
   - audience: "agent" para internal; "director" para restricted
   - purpose, source: [owners.csv, properties.csv]
   - status: final, version, date, entity: owner, language: es
   - tags: owner_id, confidentiality_level, owner_type
   - summary: nombre · tipo · confidencialidad
   - owner_id, confidentiality_level

2. Cuerpo del documento:
   - Advertencia de uso según categoría:
     - Internal: "Uso interno del equipo Meridiana. No compartir con prospectos."
     - Restricted: "RESTRINGIDO — Información de alta confidencialidad. Uso exclusivo de dirección."
   - Sección Datos de contacto: tabla con tipo, email, teléfono, canal preferido, país de residencia, representante legal (si aplica)
   - Sección Condiciones y preferencias: tabla con nivel de confidencialidad, permite fotos públicas, permite open house
   - Sección Propiedades vinculadas: lista con property_id, commercial_name, status y listing_type
   - Sección Notas internas: notes_internal con advertencia de confidencialidad
   - Footer con fecha

3. Reglas de contenido:
   - Para propietarios tipo fideicomiso: resaltar el nombre del representante legal y su email como canal único de comunicación
   - Para confidencialidad muy alta: agregar nota explícita de que no se debe contactar directamente al propietario bajo ninguna circunstancia
   - Para propietarios en el exterior: anotar el país y la preferencia de idioma si se infiere de las notas
   - No revelar en ningún campo el nombre del representante legal si el propietario es persona física con confidencialidad muy alta

Genera únicamente el documento Markdown. Sin explicaciones adicionales.
```

---

## Notas de uso

- El enrutamiento a `internal/` vs `restricted/` debe hacerse antes de escribir el archivo, no después
- Propietarios en proceso legal activo (divorcio, fideicomiso con herederos en conflicto) siempre van a `restricted/`
- La información de contacto de un propietario de confidencialidad `muy alta` no debe aparecer en ningún documento de categoría `public` ni `internal` compartido
