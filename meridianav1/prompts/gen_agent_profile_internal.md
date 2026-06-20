---
title: "Prompt: Generar perfil interno de asesor"
doc_type: prompt
category: template
audience: internal_team
purpose: "Prompt canónico para generar perfiles internos de asesores con KPIs y cartera."
source:
  - agents.csv
  - properties.csv
  - offers.csv
status: final
version: v01
date: 2026-06-14
entity: agent
language: es
tags:
  - prompt
  - generacion
  - agent_profile_internal
  - internal
doc_id: prompt-gen-agent-profile-internal
output_category: internal
output_doc_type: agent_profile_internal
output_path: "knowledge_base/internal/playbooks/agent-internal-{agent_id}.md"
---

# Prompt: Generar perfil interno de asesor

## Propósito

Genera una ficha interna de asesor con datos operativos completos: comisión, manager, cartera de propiedades asignadas y métricas de actividad comercial. Uso exclusivo del equipo Meridiana.

---

## Variables de entrada

- `{agent_id}` — ej. `AGT-02`
- `{row_agent}` — fila de `agents.csv`
- `{row_manager}` — fila de `agents.csv` para el manager (si aplica)
- `{rows_properties}` — filas de `properties.csv` donde `agent_id` coincide
- `{rows_offers}` — filas de `offers.csv` donde `agent_id` coincide

---

## Prompt

```
Eres analista de operaciones de Meridiana. Genera una ficha interna de asesor en Markdown con frontmatter YAML. Este documento es de uso exclusivo del equipo directivo y no debe salir de la organización.

### Datos del asesor
{row_agent}

### Manager
{row_manager}

### Propiedades asignadas
{rows_properties}

### Ofertas gestionadas
{rows_offers}

### Instrucciones de formato

1. Frontmatter obligatorio:
   - title: "Perfil interno de asesor: {full_name} ({agent_id})"
   - doc_type: agent_profile_internal, category: internal, audience: internal_team
   - purpose, source: [agents.csv, properties.csv, offers.csv]
   - status: final, version, date, entity: agent, language: es
   - tags: agent_id, seniority, rol
   - summary: nombre, rol, seniority, comisión
   - agent_id

2. Cuerpo del documento:
   - Advertencia de uso interno al inicio
   - Sección Datos del asesor: tabla completa incluyendo email, teléfono, rol, nivel, manager, estado activo
   - Sección Especialidad comercial: zona, tipo de propiedad, idiomas, comisión
   - Sección Actividad en cartera: tabla de métricas (total propiedades asignadas, activas, ofertas gestionadas, cierres confirmados)
   - Lista de propiedades asignadas con property_id, commercial_name y status
   - Footer con fecha

3. Reglas de contenido:
   - Incluir commission_pct y manager_id (es documento interno)
   - Cierres confirmados = ofertas con status "aceptada" o "carta de intención firmada"
   - Si no tiene propiedades ni ofertas, indicarlo explícitamente
   - No inventar métricas de rendimiento ni porcentajes de conversión

Genera únicamente el documento Markdown. Sin explicaciones adicionales.
```

---

## Notas de uso

- Este prompt genera documentos de categoría `internal`, no `public`
- La comisión es información sensible: solo visible en perfiles internos
- Para staff sin cartera (marketing, operaciones, legal), las secciones de propiedades y ofertas mostrarán "No aplica"
