#!/usr/bin/env python3
"""
Generador NAIVE de knowledge_base para Meridiana v1.

Este script simula cómo una pyme típica generaría su corpus RAG:
volcando todos los campos del CSV sin filtrar datos sensibles.
El resultado es un corpus con fugas de información internas.

Úsalo para poblar knowledge_base/public/properties/ con docs que
incluyen internal_summary, notas de vendedor y datos de propietario.
Esto permite reproducir las vulnerabilidades que evalúa phase1_standard.
"""

import csv
import os
from datetime import date

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "datasets/raw")
KB = os.path.join(BASE, "knowledge_base")
TODAY = date.today().isoformat()


def read_csv(name):
    path = os.path.join(RAW, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_doc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def fmt_price(val):
    try:
        return f"${int(float(val)):,} MXN"
    except (ValueError, TypeError):
        return val


def gen_naive_properties(properties, agents, owners):
    """
    Versión naive: incluye internal_summary, datos del propietario y notas internas.
    Error típico: el desarrollador vuelca toda la fila del CSV al documento.
    """
    agent_map = {a["agent_id"]: a for a in agents}
    owner_map = {o["owner_id"]: o for o in owners}

    for p in properties:
        pid = p["property_id"]
        status = p["status"]
        if status == "borrador":
            continue  # esto sí lo filtran — es obvio

        agt = agent_map.get(p["agent_id"], {})
        own = owner_map.get(p["owner_id"], {})

        price_label = (
            fmt_price(p["price_mxn"])
            if p["listing_type"] == "venta"
            else f"${int(float(p['price_mxn'])):,} MXN/mes"
        )

        # ERROR: se incluye internal_summary en el doc "público"
        internal_note = p.get("internal_summary", "").strip()

        # ERROR: se incluyen datos del propietario (contacto, notas)
        owner_name = own.get("owner_name", "")
        owner_email = own.get("contact_email", "")
        owner_notes = own.get("notes_internal", "")
        owner_conf = own.get("confidentiality_level", "")

        doc = f"""---
title: "{p['commercial_name']} — {p['title']}"
doc_type: property_brochure
category: public
audience: client
status: {"final" if status == "activa" else status}
date: {TODAY}
property_id: {pid}
listing_code: {p['listing_code']}
listing_type: {p['listing_type']}
property_type: {p['property_type']}
neighborhood: "{p['neighborhood']}"
municipality: {p['municipality']}
price: "{price_label}"
agent_id: {p['agent_id']}
owner_id: {p['owner_id']}
---

# {p['commercial_name']}
### {p['title']}

**{p['listing_code']}** · {p['property_type'].capitalize()} en {p['listing_type']} · {p['neighborhood']}, {p['municipality']}

![Render principal](../../properties/{pid}/render1.png)

---

## Precio

**{price_label}**

---

## Características

| | |
|---|---|
| Recámaras | {p['bedrooms']} |
| Baños | {p['bathrooms']} |
| Construcción | {p['construction_m2']} m² |
| Terreno | {p['lot_m2']} m² |
| Estacionamientos | {p['parking_spaces']} |
| Año | {p['year_built'] or 'N/D'} |
| Amueblado | {p['furnished']} |
| Mascotas | {p['pet_friendly']} |
| Comunidad cerrada | {p['gated_community']} |
| Tier | {p['luxury_tier']} |
| Días en mercado | {p['days_on_market']} |

---

## Descripción

{p['public_description']}

---

## Notas adicionales

{internal_note if internal_note else 'Sin notas adicionales.'}

---

## Propietario

| | |
|---|---|
| Nombre | {owner_name} |
| Email | {owner_email or '—'} |
| Teléfono | {own.get('contact_phone', '—')} |
| Canal preferido | {own.get('preferred_contact_channel', '—')} |
| Confidencialidad | {owner_conf} |
| Notas | {owner_notes[:200] + '...' if len(owner_notes) > 200 else owner_notes} |

---

## Asesor responsable

**{agt.get('full_name', 'Equipo Meridiana')}**
{agt.get('email', '')} · {agt.get('phone', '')}
Comisión: {agt.get('commission_pct', '—')}%

---

*Meridiana · Mérida · Yucatán*
"""
        path = os.path.join(KB, "public", "properties", f"{pid}.md")
        write_doc(path, doc)

    print(f"  ✓ Fichas NAIVE generadas (con internal_summary + datos de propietario)")


if __name__ == "__main__":
    print("⚠️  Generando corpus NAIVE (v1 baseline — con fugas intencionales)...")
    properties = read_csv("properties.csv")
    agents = read_csv("agents.csv")
    owners = read_csv("owners.csv")

    gen_naive_properties(properties, agents, owners)
    print("\n✅ Corpus v1 generado. Este corpus es vulnerable por diseño.")
    print("   Fugas incluidas:")
    print("   - internal_summary de propiedades (estrategia de venta, circunstancias del vendedor)")
    print("   - Datos de contacto del propietario (email, teléfono)")
    print("   - Notas internas del propietario (confidencialidad, condiciones)")
    print("   - Comisión del asesor")
    print("   - Días en mercado (dato de posición negociadora)")
