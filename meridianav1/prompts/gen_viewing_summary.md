---
title: "Prompt: Generar resumen de visita"
doc_type: prompt
category: template
audience: internal_team
purpose: "Prompt canónico para generar resúmenes narrativos de visitas desde viewings.csv."
source:
  - viewings.csv
  - properties.csv
  - leads.csv
status: final
version: v01
date: 2026-06-14
entity: viewing
language: es
tags:
  - prompt
  - generacion
  - viewing_summary
  - internal
doc_id: prompt-gen-viewing-summary
output_category: internal
output_doc_type: viewing_summary
output_path: "knowledge_base/internal/viewings/{viewing_id}.md"
---

# Prompt: Generar resumen de visita

## Propósito

Genera un resumen narrativo de una visita a propiedad para uso del equipo comercial. Incluye contexto del prospecto, observaciones del recorrido, objeciones identificadas y recomendaciones de seguimiento.

---

## Variables de entrada

- `{viewing_id}` — ej. `V001`
- `{row_viewing}` — fila de `viewings.csv`
- `{row_property}` — fila de `properties.csv` correspondiente
- `{row_lead}` — fila de `leads.csv` correspondiente

---

## Prompt

```
Eres asesor comercial senior de Meridiana. Tu estilo de escritura es directo, observacional y útil para quien dará el seguimiento. Sin adornos.

Con los siguientes datos, genera un resumen de visita en Markdown con frontmatter YAML.

### Datos de la visita
{row_viewing}

### Propiedad visitada
{row_property}

### Perfil del prospecto
{row_lead}

### Instrucciones de formato

1. Frontmatter obligatorio:
   - title: "Resumen de visita {viewing_id}: {property_id} · {lead_id}"
   - doc_type: viewing_summary, category: internal, audience: agent
   - purpose, source: [viewings.csv, properties.csv, leads.csv]
   - status: final, version, date, entity: viewing, language: es
   - tags: viewing_id, property_id, lead_id, agent_id, status de visita
   - summary: una línea con viewing_id, propiedad, prospecto, estado e interés
   - viewing_id, property_id, lead_id, agent_id, visit_status, interest_level, follow_up_required

2. Cuerpo del documento:
   - Sección Datos de la visita: tabla con fecha, tipo, estado, nivel de interés, requiere seguimiento
   - Sección Feedback del recorrido: texto narrativo del feedback_summary tal como está
   - Sección Objeciones identificadas: texto de objections tal como está
   - Sección Contexto del prospecto (solo para visitas realizadas): 2-3 líneas conectando el perfil del lead con lo observado en la visita
   - Sección Recomendación de seguimiento (solo si follow_up_required = sí): una acción concreta basada en los datos disponibles
   - Footer con fecha

3. Reglas de contenido:
   - Para visitas canceladas o programadas: el feedback y las objeciones pueden estar vacíos; indicarlo con "Pendiente"
   - La sección "Contexto del prospecto" solo se genera para visitas con status = "realizada"
   - No inventar detalles de la visita ni inferir intenciones no registradas
   - Las notas internas del lead (notes_internal) pueden usarse para la recomendación de seguimiento, pero no deben citarse literalmente

Genera únicamente el documento Markdown. Sin explicaciones adicionales.
```

---

## Notas de uso

- Las visitas con `status = cancelada` tienen `feedback_summary` y `objections` vacíos normalmente
- El `notes_internal` del lead es contexto de soporte, no debe transcribirse al documento de visita
- Las visitas `programadas` son futuras: no inventar resultado
