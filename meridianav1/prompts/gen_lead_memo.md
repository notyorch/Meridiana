---
title: "Prompt: Generar memo de calificación de lead"
doc_type: prompt
category: template
audience: internal_team
purpose: "Prompt canónico para generar memos de calificación de prospectos desde leads.csv."
source:
  - leads.csv
status: final
version: v01
date: 2026-06-14
entity: lead
language: es
tags:
  - prompt
  - generacion
  - lead_qualification_memo
  - internal
doc_id: prompt-gen-lead-memo
output_category: internal
output_doc_type: lead_qualification_memo
output_path: "knowledge_base/internal/leads/{lead_id}.md"
---

# Prompt: Generar memo de calificación de lead

## Propósito

Genera un memo operativo del prospecto para uso del agente asignado. Consolida datos de contacto, criterios de búsqueda, score de calificación y notas internas en un documento estructurado.

---

## Variables de entrada

- `{lead_id}` — ej. `L001`
- `{row_lead}` — fila completa de `leads.csv`

---

## Escala de calificación

| Score | Etiqueta |
|---|---|
| 0–39 | bajo |
| 40–59 | medio-bajo |
| 60–74 | medio |
| 75–87 | alto |
| 88–100 | muy alto |

---

## Prompt

```
Eres coordinador comercial de Meridiana. Genera un memo de calificación de prospecto en Markdown con frontmatter YAML para uso exclusivo del equipo comercial.

### Datos del lead
{row_lead}

### Instrucciones de formato

1. Frontmatter obligatorio:
   - title: "Memo de calificación: {full_name} ({lead_id})"
   - doc_type: lead_qualification_memo, category: internal, audience: agent
   - purpose, source: [leads.csv]
   - status: final, version, date, entity: lead, language: es
   - tags: lead_id, tipo de propiedad (primer valor), lead_status, investment_profile
   - summary: nombre · estado · score/100 (etiqueta)
   - lead_id, assigned_agent, qualification_score

2. Cuerpo del documento:
   - Advertencia de uso interno
   - Sección Perfil del prospecto: tabla con nombre, email, teléfono, origen, estado, score con etiqueta
   - Sección Criterios de búsqueda: tabla con presupuesto, financiamiento, municipio, zonas, tipo de propiedad, recámaras mínimas, horizonte de compra, perfil de inversión
   - Sección Notas del prospecto: notes_public (lo que el prospecto sabe que registramos)
   - Sección Notas internas del equipo: notes_internal con advertencia de confidencialidad
   - Footer con fecha

3. Reglas de contenido:
   - Las notas internas van en sección separada con advertencia de "No compartir con el prospecto"
   - El presupuesto se formatea como "${budget_min:,} MXN — ${budget_max:,} MXN"
   - Para leads con status = "descartado": añadir nota al inicio indicando que el lead está cerrado
   - No inferir intenciones ni agregar recomendaciones no presentes en los datos

Genera únicamente el documento Markdown. Sin explicaciones adicionales.
```

---

## Notas de uso

- `notes_internal` es el campo más sensible: no debe aparecer en ningún documento de categoría `public`
- Para leads con `lead_status = descartado`, el memo se genera igualmente para trazabilidad
- El `assigned_agent_id` determina quién es el `owner` del documento en el frontmatter
