---
title: "Prompt: Generar perfil público de asesor"
doc_type: prompt
category: template
audience: internal_team
purpose: "Prompt canónico para generar perfiles públicos de asesores desde agents.csv."
source:
  - agents.csv
status: final
version: v01
date: 2026-06-14
entity: agent
language: es
tags:
  - prompt
  - generacion
  - agent_profile
  - public
doc_id: prompt-gen-agent-profile-public
output_category: public
output_doc_type: agent_profile
output_path: "knowledge_base/public/agents/{agent_id}.md"
---

# Prompt: Generar perfil público de asesor

## Propósito

Genera un perfil de asesor orientado a clientes en Markdown con frontmatter. Solo expone información pública: nombre, rol, zona, especialidad, idiomas y contacto. El documento resultante va en `knowledge_base/public/agents/`.

---

## Variables de entrada

- `{agent_id}` — ej. `AGT-01`
- `{row_agent}` — fila completa de `agents.csv` para este asesor

---

## Prompt

```
Eres redactor de contenido institucional de Meridiana, inmobiliaria boutique en Mérida, Yucatán. Tono: profesional, cálido y concreto. Sin frases genéricas de marketing.

Con los siguientes datos, genera un perfil de asesor en Markdown con frontmatter YAML.

### Datos del asesor
{row_agent}

### Instrucciones de formato

1. Frontmatter obligatorio:
   - title: "Perfil de asesor: {full_name}"
   - doc_type: agent_profile, category: public, audience: client
   - purpose, source: [agents.csv], status: final, version: v01, date, entity: agent, language: es
   - tags: agent_id en minúsculas, "asesor", rol simplificado
   - summary: una línea con nombre, rol y zona de especialidad
   - agent_id

2. Cuerpo del documento:
   - H1: nombre completo
   - Subtítulo: rol · Meridiana Inmobiliaria
   - Sección Especialidad: tabla con zona geográfica, tipo de propiedad, idiomas, nivel (seniority)
   - Sección Contacto: email y teléfono
   - Footer: "Meridiana · Mérida · Yucatán"

3. Reglas de contenido:
   - NUNCA incluir commission_pct, manager_id ni datos internos de jerarquía
   - El rol debe presentarse de forma legible: "Director Comercial", "Asesor Senior", "Asesor", "Asesor Junior"
   - Si specialty_zone o specialty_property_type están vacíos (staff), omitir la sección Especialidad y solo mostrar el rol
   - No inventar logros, años de experiencia ni frases motivacionales

Genera únicamente el documento Markdown. Sin explicaciones adicionales.
```

---

## Notas de uso

- Los campos `commission_pct`, `manager_id` y `active` son internos y no deben aparecer
- Para roles de staff (marketing, operaciones, legal) omitir zona y tipo de propiedad
