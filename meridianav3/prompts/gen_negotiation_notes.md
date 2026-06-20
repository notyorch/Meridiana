---
title: "Prompt: Generar memo de negociación"
doc_type: prompt
category: template
audience: internal_team
purpose: "Prompt canónico para generar memos de negociación confidenciales desde offers.csv."
source:
  - offers.csv
  - properties.csv
  - leads.csv
status: final
version: v01
date: 2026-06-14
entity: offer
language: es
tags:
  - prompt
  - generacion
  - negotiation_notes
  - restricted
doc_id: prompt-gen-negotiation-notes
output_category: restricted
output_doc_type: negotiation_notes
output_path: "knowledge_base/restricted/deals/{offer_id}.md"
---

# Prompt: Generar memo de negociación

## Propósito

Genera un memo confidencial de negociación para uso exclusivo de dirección y del agente asignado. Consolida estado de la oferta, montos, contraoferta, ventana de cierre y estrategia de negociación interna.

---

## Variables de entrada

- `{offer_id}` — ej. `O001`
- `{row_offer}` — fila de `offers.csv`
- `{row_property}` — fila de `properties.csv` correspondiente
- `{row_lead}` — fila de `leads.csv` correspondiente

---

## Estados de oferta y su significado

| Estado CSV | Descripción operativa |
|---|---|
| `aceptada` | Propietario aceptó. Proceso notarial en marcha. |
| `rechazada` | Propietario rechazó. Sin contraoferta activa. |
| `contraoferta activa` | Propietario respondió con contraoferta. Lead deliberando. |
| `en negociación` | Intercambio activo de posiciones. Sin acuerdo todavía. |
| `en revisión legal` | Oferta en análisis legal antes de aceptar o rechazar. |
| `carta de intención firmada` | Compromiso formal previo al contrato. |
| `retirada por lead` | El prospecto se retiró de la oferta. |
| `pendiente visita` | Oferta indicativa antes de visita confirmada. |

---

## Prompt

```
Eres director comercial de Meridiana. Genera un memo de negociación confidencial en Markdown con frontmatter YAML. Este documento es de acceso restringido: solo el agente asignado y dirección.

### Datos de la oferta
{row_offer}

### Propiedad
{row_property}

### Prospecto
{row_lead}

### Instrucciones de formato

1. Frontmatter obligatorio:
   - title: "Memo de negociación {offer_id}: {property_id} — {lead_id}"
   - doc_type: negotiation_notes, category: restricted, audience: director
   - purpose, source: [offers.csv, properties.csv, leads.csv]
   - status: final, version, date, entity: offer, language: es
   - tags: offer_id, property_id, lead_id, agent_id, offer_status (con guiones bajos)
   - summary: offer_id · propiedad con lead · estado · monto ofertado
   - offer_id, property_id, lead_id, agent_id, offer_status (entrecomillado)

2. Cuerpo del documento:
   - Advertencia de RESTRINGIDO al inicio
   - Sección Estado de la oferta: tabla con estado actual, fecha, monto ofertado, contraoferta, ventana de cierre en días, tipo de financiamiento, enganche/depósito
   - Sección Notas de negociación: notes_internal con advertencia de confidencialidad
   - Footer con fecha

3. Reglas de contenido:
   - El monto se formatea como "${amount:,} MXN"
   - Si el monto es 0 (carta de intención), indicar "N/A — Carta de intención"
   - Si no hay contraoferta (valor 0), indicar "Sin contraoferta"
   - El gap entre oferta y contraoferta se calcula y se menciona en las notas si ambos valores existen
   - NUNCA suavizar ni resumir las notas internas: transcribir literalmente
   - Las circunstancias personales del vendedor (divorcio, urgencia, etc.) mencionadas en notes_internal son información de uso estrictamente interno

Genera únicamente el documento Markdown. Sin explicaciones adicionales.
```

---

## Notas de uso

- Este prompt genera documentos de categoría `restricted` — el más sensible del sistema
- Las notas de negociación pueden contener información personal del vendedor: manejo estrictamente confidencial
- Cualquier operación con criptomonedas, moneda extranjera o condiciones inusuales debe estar anotada en el memo y marcada para revisión de AGT-15 (legal y cumplimiento)
- El output nunca debe indexarse en el corpus público del RAG
