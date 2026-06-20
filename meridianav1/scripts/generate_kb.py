#!/usr/bin/env python3
"""Genera los documentos de knowledge_base desde los CSVs de Meridiana."""

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


# ─── helpers ────────────────────────────────────────────────────────────────

def tag_list(*args):
    return "\n" + "\n".join(f"  - {a}" for a in args if a)


# ════════════════════════════════════════════════════════════════════════════
# 1. PUBLIC — Fichas de propiedad
# ════════════════════════════════════════════════════════════════════════════

def gen_public_properties(properties, features, agents):
    feats_by_prop = {}
    for f in features:
        pid = f["property_id"]
        if pid not in feats_by_prop:
            feats_by_prop[pid] = []
        if f.get("is_public", "").lower() in ("sí", "si", "yes", "true"):
            feats_by_prop[pid].append(f)

    agent_map = {a["agent_id"]: a for a in agents}

    for p in properties:
        pid = p["property_id"]
        lc = p["listing_code"]
        status = p["status"]
        # Solo publicar propiedades activas o recién vendidas
        if status in ("borrador",):
            continue

        agt = agent_map.get(p["agent_id"], {})
        agt_name = agt.get("full_name", "Equipo Meridiana")
        agt_email = agt.get("email", "contacto@meridiana.mx")
        agt_phone = agt.get("phone", "")

        price_label = fmt_price(p["price_mxn"]) if p["listing_type"] == "venta" else f"${int(float(p['price_mxn'])):,} MXN/mes"

        prop_feats = feats_by_prop.get(pid, [])
        feat_lines = ""
        if prop_feats:
            cats = {}
            for f in prop_feats:
                c = f.get("category", "General")
                cats.setdefault(c, []).append(f["feature_name"])
            for cat, items in cats.items():
                feat_lines += f"\n**{cat}**\n"
                for item in items:
                    feat_lines += f"- {item}\n"

        maint = f"${int(float(p['maintenance_fee_mxn'])):,} MXN/mes" if p.get("maintenance_fee_mxn") and p["maintenance_fee_mxn"] != "0" else "No aplica"

        tags = [
            p["municipality"].lower().replace(" ", "_"),
            p["neighborhood"].lower().replace(" ", "_").replace("·", "").strip(),
            p["property_type"],
            p["listing_type"],
            p["luxury_tier"],
        ]
        tags = [t for t in tags if t]

        img_path     = f"../../properties/{pid}/render1.png"
        brochure_url = f"properties/{pid}/property-brochure.html"

        doc = f"""---
title: "{p['commercial_name']} — {p['title']}"
doc_type: property_brochure
category: public
audience: client
purpose: "Ficha comercial de propiedad para presentación a clientes y prospectos."
source:
  - properties.csv
  - property_features.csv
  - agents.csv
status: {"final" if status == "activa" else status}
version: v01
date: {TODAY}
entity: property
language: es
tags:{tag_list(*tags)}
summary: "{p['public_description'][:120]}..."
owner: equipo comercial
doc_id: kb-pub-{pid.lower()}
property_id: {pid}
listing_code: {lc}
listing_type: {p['listing_type']}
property_type: {p['property_type']}
neighborhood: "{p['neighborhood']}"
municipality: {p['municipality']}
price: "{price_label}"
luxury_tier: {p['luxury_tier']}
agent_id: {p['agent_id']}
brochure_url: "{brochure_url}"
render_image: "properties/{pid}/render1.png"
---

# {p['commercial_name']}
### {p['title']}

**{lc}** · {p['property_type'].capitalize()} en {p['listing_type']} · {p['neighborhood']}, {p['municipality']}

![Render principal]({img_path})

🔗 [Ver brochure completo]({brochure_url})

---

## Precio

**{price_label}**{"" if maint == "No aplica" else f"  ·  Mantenimiento: {maint}"}

---

## Características principales

| | |
|---|---|
| Recámaras | {p['bedrooms']} |
| Baños | {p['bathrooms']} |
| Construcción | {p['construction_m2']} m² |
| Terreno | {p['lot_m2']} m² |
| Estacionamientos | {p['parking_spaces']} |
| Año de construcción | {p['year_built'] or 'N/D'} |
| Amueblado | {p['furnished'].capitalize()} |
| Acepta mascotas | {p['pet_friendly'].capitalize()} |
| Comunidad privada | {p['gated_community'].capitalize()} |

---

## Descripción

{p['public_description']}

---
{"## Amenidades y características" + chr(10) + feat_lines if feat_lines else ""}
---

## Asesor responsable

**{agt_name}**
{agt_email}
{agt_phone}

---

*Meridiana · Mérida · Yucatán · meridiana.mx*
"""
        path = os.path.join(KB, "public", "properties", f"{pid}.md")
        write_doc(path, doc)

    print(f"  ✓ Fichas de propiedad generadas")


# ════════════════════════════════════════════════════════════════════════════
# 2. PUBLIC — Perfiles de agente
# ════════════════════════════════════════════════════════════════════════════

def gen_public_agents(agents):
    for a in agents:
        aid = a["agent_id"]
        name = a["full_name"]
        role = a["role"].title()
        zone = a["specialty_zone"] or "Oficina central"
        prop_types = a["specialty_property_type"] or "General"
        langs = a["languages"]
        seniority = a["seniority"].title()

        doc = f"""---
title: "Perfil de asesor: {name}"
doc_type: agent_profile
category: public
audience: client
purpose: "Presentar al asesor y sus especialidades para contacto por parte de clientes."
source:
  - agents.csv
status: final
version: v01
date: {TODAY}
entity: agent
language: es
tags:
  - {aid.lower()}
  - asesor
  - {"director" if "director" in role.lower() else "advisor"}
summary: "{name}, {role} en Meridiana especializado en {zone}."
owner: equipo comercial
doc_id: kb-pub-{aid.lower()}
agent_id: {aid}
---

# {name}

**{role}** · Meridiana Inmobiliaria

---

## Especialidad

| | |
|---|---|
| Zona geográfica | {zone} |
| Tipo de propiedad | {prop_types} |
| Idiomas | {langs} |
| Nivel | {seniority} |

---

## Contacto

- **Email:** {a['email']}
- **Teléfono:** {a['phone']}

---

*Meridiana · Mérida · Yucatán*
"""
        path = os.path.join(KB, "public", "agents", f"{aid}.md")
        write_doc(path, doc)

    print(f"  ✓ Perfiles públicos de agente generados ({len(agents)})")


# ════════════════════════════════════════════════════════════════════════════
# 3. PUBLIC — Company profile + FAQs
# ════════════════════════════════════════════════════════════════════════════

def gen_public_company():
    doc = """---
title: "Meridiana — Perfil corporativo"
doc_type: company_profile
category: public
audience: client
purpose: "Presentar a Meridiana como inmobiliaria premium de referencia en Yucatán."
source: []
status: final
version: v01
date: """ + TODAY + """
entity: company
language: es
tags:
  - meridiana
  - company
  - about
summary: "Meridiana es una inmobiliaria boutique especializada en propiedades premium en Yucatán."
owner: dirección
doc_id: kb-pub-company-profile
---

# Meridiana Inmobiliaria

**Propiedades premium en Yucatán**

---

## Quiénes somos

Meridiana es una inmobiliaria boutique con sede en Mérida, Yucatán, especializada en la comercialización de propiedades residenciales y comerciales de segmento premium y ultra. Operamos con un equipo de asesores certificados que combinan conocimiento profundo del mercado local con estándares de atención de clase internacional.

---

## Nuestra propuesta de valor

- **Inventario curado:** solo propiedades que cumplen con estándares de calidad, documentación y potencial.
- **Atención personalizada:** cada cliente tiene un asesor dedicado con seguimiento continuo.
- **Confidencialidad:** manejamos operaciones sensibles con total discreción.
- **Cobertura regional:** Mérida, zona metropolitana, municipios del interior y costa de Yucatán.
- **Experiencia internacional:** atendemos clientes en español, inglés, francés y alemán.

---

## Segmentos que atendemos

| Segmento | Descripción |
|---|---|
| Ultra | Propiedades $15M MXN en adelante, exclusividad absoluta |
| Premium | Propiedades $6M–$15M MXN, acabados y ubicación superiores |
| Entrada | Propiedades desde $1.5M MXN, primera adquisición o inversión |
| Renta corporativa | Residencias y villas para ejecutivos en asignación |
| Renta vacacional | Gestión de propiedades turísticas en Yucatán y costa |

---

## Equipo

Contamos con 15 colaboradores: asesores comerciales senior y junior, coordinación de marketing, operaciones y un área de legal y cumplimiento.

---

## Contacto

**Oficina principal:** Mérida, Yucatán, México
**Email:** contacto@meridiana.mx
**Web:** meridiana.mx

---

*Meridiana · Mérida · Yucatán*
"""
    path = os.path.join(KB, "public", "company", "company-profile.md")
    write_doc(path, doc)

    buyer_faq = """---
title: "Preguntas frecuentes — Compradores"
doc_type: faq
category: public
audience: client
purpose: "Resolver las dudas más comunes de compradores e inversionistas."
source: []
status: final
version: v01
date: """ + TODAY + """
entity: lead
language: es
tags:
  - faq
  - comprador
  - proceso
summary: "Guía de preguntas frecuentes para compradores de propiedades con Meridiana."
owner: equipo comercial
doc_id: kb-pub-faq-buyer
---

# Preguntas frecuentes para compradores

---

## ¿Cómo funciona el proceso de compra con Meridiana?

El proceso tiene cuatro etapas: (1) Calificación y búsqueda, donde conocemos tu perfil y necesidades; (2) Presentación de propiedades, con visitas coordinadas; (3) Oferta y negociación, donde te acompañamos en cada paso; (4) Cierre notarial, donde coordinamos con notaría y asesores legales.

---

## ¿Cuánto cuesta contratar a Meridiana?

Como comprador no pagas comisión directa. La comisión de venta es cubierta por el vendedor. Tu inversión es exclusivamente el valor de la propiedad y los gastos notariales correspondientes.

---

## ¿Puedo comprar si soy extranjero?

Sí. Los ciudadanos extranjeros pueden adquirir propiedades en México, incluyendo la zona federal. Para propiedades en zona restringida (50 km de costa o 100 km de frontera) se utiliza un fideicomiso bancario, que es un instrumento legal seguro y común. Nuestro equipo legal te guía en todo el proceso.

---

## ¿Qué gastos de cierre debo considerar?

Los gastos de escrituración típicos en Yucatán representan entre el 4% y el 7% del valor de la propiedad e incluyen: derechos notariales, impuesto de adquisición de inmuebles (ISAI), avalúo catastral y honorarios del notario.

---

## ¿Puedo comprar con crédito hipotecario?

Sí. Trabajamos con compradores que utilizan crédito bancario (BBVA, Santander, HSBC, Banorte), INFONAVIT, FOVISSSTE o combinaciones. Es importante tener la preaprobación bancaria antes de iniciar la búsqueda para acotar opciones a tu capacidad real.

---

## ¿Cuánto tiempo tarda un cierre?

Depende del tipo de operación. Una compra en contado puede cerrar en 30 a 45 días hábiles. Con crédito bancario, entre 60 y 90 días. Operaciones con fideicomiso para extranjeros pueden tomar hasta 120 días dependiendo del banco.

---

## ¿Qué documentos necesito?

Para iniciar: identificación oficial vigente, comprobante de domicilio y constancia de situación fiscal (RFC). Para el cierre notarial tu notario te indicará la lista completa según el tipo de operación.

---

*Meridiana · Mérida · Yucatán*
"""
    path = os.path.join(KB, "public", "faq", "faq-compradores.md")
    write_doc(path, buyer_faq)

    seller_faq = """---
title: "Preguntas frecuentes — Vendedores y arrendadores"
doc_type: faq
category: public
audience: owner
purpose: "Resolver las dudas más comunes de propietarios que desean vender o rentar."
source: []
status: final
version: v01
date: """ + TODAY + """
entity: owner
language: es
tags:
  - faq
  - vendedor
  - propietario
summary: "Guía de preguntas frecuentes para propietarios que trabajan con Meridiana."
owner: equipo comercial
doc_id: kb-pub-faq-seller
---

# Preguntas frecuentes para vendedores y arrendadores

---

## ¿Cómo determina Meridiana el precio de mi propiedad?

Realizamos un análisis comparativo de mercado (ACM) considerando propiedades similares vendidas recientemente en la misma zona, el estado físico de tu inmueble, características diferenciadoras y condiciones actuales del mercado. El objetivo es encontrar el precio óptimo que maximice tu beneficio sin alargar innecesariamente el tiempo en el mercado.

---

## ¿Cuál es la comisión de Meridiana?

La comisión varía según el tipo de operación, segmento y condiciones específicas de la propiedad. Tu asesor te la comunicará en la reunión inicial. Se paga únicamente al momento del cierre exitoso.

---

## ¿Qué incluye el servicio de Meridiana?

Fotografía profesional y recorridos virtuales, publicación en portales especializados y redes sociales, presentaciones a clientes calificados, coordinación de visitas, acompañamiento en negociación y gestión del proceso de cierre con notaría.

---

## ¿Cuánto tiempo tardará en venderse mi propiedad?

El tiempo promedio varía por segmento y zona. Propiedades bien valuadas en zonas de alta demanda suelen recibir ofertas en 15 a 30 días. Propiedades en segmentos ultra o zonas específicas pueden tomar 60 a 120 días. Te mantenemos informado con reportes de actividad.

---

## ¿Debo estar presente en las visitas?

No es necesario. Coordinamos las visitas con tu agenda y podemos mostrar la propiedad con tu autorización. Para propiedades con condiciones especiales de privacidad, diseñamos protocolos a tu medida.

---

## ¿Qué documentos necesito tener en orden?

Escritura de propiedad, predial al corriente, identificación oficial, constancia de no adeudo de servicios y, en caso de propiedades en condominio, último estado de cuenta de mantenimiento. Si la propiedad tiene régimen de fideicomiso, necesitaremos los documentos del fideicomiso.

---

*Meridiana · Mérida · Yucatán*
"""
    path = os.path.join(KB, "public", "faq", "faq-vendedores.md")
    write_doc(path, seller_faq)

    print("  ✓ Company profile y FAQs generados")


# ════════════════════════════════════════════════════════════════════════════
# 4. INTERNAL — Memos de calificación de leads
# ════════════════════════════════════════════════════════════════════════════

def gen_internal_leads(leads):
    score_label = {
        range(0, 40): "bajo",
        range(40, 60): "medio-bajo",
        range(60, 75): "medio",
        range(75, 88): "alto",
        range(88, 101): "muy alto",
    }

    def get_label(score):
        try:
            s = int(score)
        except (ValueError, TypeError):
            return "N/D"
        for r, label in score_label.items():
            if s in r:
                return label
        return "N/D"

    for lead in leads:
        lid = lead["lead_id"]
        name = lead["full_name"]
        status = lead["lead_status"]
        score = lead["qualification_score"]
        agt = lead["assigned_agent_id"]

        budget_min = fmt_price(lead["budget_min_mxn"])
        budget_max = fmt_price(lead["budget_max_mxn"])

        tags = [
            lid.lower(),
            lead["property_type_interest"].split("·")[0].strip().replace(" ", "_"),
            status.replace(" ", "_"),
            lead["investment_profile"].replace(" ", "_").replace("+", "mas"),
        ]

        doc = f"""---
title: "Memo de calificación: {name} ({lid})"
doc_type: lead_qualification_memo
category: internal
audience: agent
purpose: "Resumen operativo del prospecto para uso exclusivo del equipo comercial."
source:
  - leads.csv
status: final
version: v01
date: {TODAY}
entity: lead
language: es
tags:{tag_list(*tags)}
summary: "{name} — {status.title()} — Score {score}/100 ({get_label(score)})"
owner: {agt}
doc_id: kb-int-{lid.lower()}
lead_id: {lid}
assigned_agent: {agt}
qualification_score: {score}
---

# Memo de calificación — {name}

**{lid}** · Agente asignado: {agt}

---

## Perfil del prospecto

| Campo | Valor |
|---|---|
| Nombre | {name} |
| Email | {lead['email']} |
| Teléfono | {lead['phone']} |
| Origen | {lead['lead_source'].title()} |
| Estado | **{status.title()}** |
| Score de calificación | **{score}/100** ({get_label(score)}) |

---

## Criterios de búsqueda

| Campo | Valor |
|---|---|
| Presupuesto | {budget_min} — {budget_max} |
| Financiamiento | {lead['financing_type'].title()} |
| Municipio deseado | {lead['desired_municipality']} |
| Zonas de interés | {lead['desired_neighborhoods']} |
| Tipo de propiedad | {lead['property_type_interest']} |
| Recámaras mínimas | {lead['bedrooms_min']} |
| Horizonte de compra | {lead['purchase_timeline']} |
| Perfil de inversión | {lead['investment_profile']} |

---

## Notas del prospecto (públicas)

{lead['notes_public'] or 'Sin notas públicas.'}

---

## Notas internas del equipo

> **Uso exclusivo del equipo Meridiana. No compartir con el prospecto.**

{lead['notes_internal'] or 'Sin notas internas.'}

---

*Documento interno · Meridiana · {TODAY}*
"""
        path = os.path.join(KB, "internal", "leads", f"{lid}.md")
        write_doc(path, doc)

    print(f"  ✓ Memos de leads generados ({len(leads)})")


# ════════════════════════════════════════════════════════════════════════════
# 5. INTERNAL — Resúmenes de visitas
# ════════════════════════════════════════════════════════════════════════════

def gen_internal_viewings(viewings):
    for v in viewings:
        vid = v["viewing_id"]
        pid = v["property_id"]
        lid = v["lead_id"]
        aid = v["agent_id"]
        status = v["status"]
        visit_type = v["visit_type"].title()
        scheduled = v["scheduled_at"]
        interest = v["interest_level"] or "N/D"
        feedback = v["feedback_summary"] or "Sin feedback registrado."
        objections = v["objections"] or "Sin objeciones registradas."
        follow_up = v["follow_up_required"]

        tags = [vid.lower(), pid.lower(), lid.lower(), aid.lower(), status.replace(" ", "_")]

        doc = f"""---
title: "Resumen de visita {vid}: {pid} · {lid}"
doc_type: viewing_summary
category: internal
audience: agent
purpose: "Registro del resultado de la visita para seguimiento comercial."
source:
  - viewings.csv
status: final
version: v01
date: {TODAY}
entity: viewing
language: es
tags:{tag_list(*tags)}
summary: "Visita {vid} — {pid} con {lid} — Estado: {status.title()} — Interés: {interest}"
owner: {aid}
doc_id: kb-int-{vid.lower()}
viewing_id: {vid}
property_id: {pid}
lead_id: {lid}
agent_id: {aid}
visit_status: {status}
interest_level: {interest}
follow_up_required: {follow_up}
---

# Resumen de visita — {vid}

**Propiedad:** {pid} · **Prospecto:** {lid} · **Agente:** {aid}

---

## Datos de la visita

| Campo | Valor |
|---|---|
| Fecha programada | {scheduled} |
| Tipo | {visit_type} |
| Estado | **{status.title()}** |
| Nivel de interés | **{interest.title()}** |
| Requiere seguimiento | {follow_up.title()} |

---

## Feedback del recorrido

{feedback}

---

## Objeciones identificadas

{objections}

---

*Documento interno · Meridiana · {TODAY}*
"""
        path = os.path.join(KB, "internal", "viewings", f"{vid}.md")
        write_doc(path, doc)

    print(f"  ✓ Resúmenes de visitas generados ({len(viewings)})")


# ════════════════════════════════════════════════════════════════════════════
# 6. INTERNAL — Perfiles de propietarios (nivel medio)
#    RESTRICTED — Propietarios con confidencialidad alta/muy alta
# ════════════════════════════════════════════════════════════════════════════

def gen_owners(owners):
    internal_count = 0
    restricted_count = 0

    for o in owners:
        oid = o["owner_id"]
        name = o["owner_name"]
        conf = o["confidentiality_level"]
        otype = o["owner_type"]
        country = o["residency_country"]
        channel = o["preferred_contact_channel"]
        rep = o["legal_representative"] or "—"
        notes = o["notes_internal"] or "Sin notas."

        is_restricted = conf in ("alta", "muy alta")
        category = "restricted" if is_restricted else "internal"
        audience = "director" if is_restricted else "agent"

        tags = [oid.lower(), conf.replace(" ", "_"), otype.replace(" ", "_")]

        doc = f"""---
title: "Perfil de propietario: {name} ({oid})"
doc_type: owner_profile
category: {category}
audience: {audience}
purpose: "Ficha interna del propietario para coordinación comercial y de atención."
source:
  - owners.csv
status: final
version: v01
date: {TODAY}
entity: owner
language: es
tags:{tag_list(*tags)}
summary: "{name} — {otype.title()} — Confidencialidad: {conf}"
owner: direccion
doc_id: kb-{category[:3]}-{oid.lower()}
owner_id: {oid}
confidentiality_level: {conf}
---

# Perfil de propietario — {name}

**{oid}** · {otype.title()}

{'> ⚠️ **RESTRINGIDO** — Este documento contiene información de alta confidencialidad. Uso exclusivo de dirección.' if is_restricted else '> *Uso interno del equipo Meridiana. No compartir con prospectos.*'}

---

## Datos de contacto

| Campo | Valor |
|---|---|
| Tipo | {otype.title()} |
| Email | {o['contact_email'] or '—'} |
| Teléfono | {o['contact_phone'] or '—'} |
| Canal preferido | {channel.title()} |
| País de residencia | {country} |
| Representante legal | {rep} |

---

## Condiciones y preferencias

| Campo | Valor |
|---|---|
| Nivel de confidencialidad | **{conf.upper()}** |
| Permite fotos públicas | {o['allow_public_photos'].title()} |
| Permite open house | {o['allow_open_house'].title()} |

---

## Notas internas

> **Uso exclusivo del equipo Meridiana.**

{notes}

---

*Documento {'restringido' if is_restricted else 'interno'} · Meridiana · {TODAY}*
"""
        if is_restricted:
            path = os.path.join(KB, "restricted", "owners", f"{oid}.md")
            restricted_count += 1
        else:
            path = os.path.join(KB, "internal", "owners", f"{oid}.md")
            internal_count += 1

        write_doc(path, doc)

    print(f"  ✓ Perfiles de propietarios generados — {internal_count} internos, {restricted_count} restringidos")


# ════════════════════════════════════════════════════════════════════════════
# 7. RESTRICTED — Memos de negociación (ofertas)
# ════════════════════════════════════════════════════════════════════════════

def gen_restricted_offers(offers):
    status_labels = {
        "aceptada": "Aceptada",
        "rechazada": "Rechazada",
        "contraoferta activa": "Contraoferta activa",
        "en negociación": "En negociación",
        "en revisión legal": "En revisión legal",
        "carta de intención firmada": "Carta de intención firmada",
        "retirada por lead": "Retirada por prospecto",
        "pendiente visita": "Pendiente de visita",
    }

    for o in offers:
        oid = o["offer_id"]
        pid = o["property_id"]
        lid = o["lead_id"]
        aid = o["agent_id"]
        amount = fmt_price(o["offer_amount_mxn"]) if o["offer_amount_mxn"] and o["offer_amount_mxn"] != "0" else "N/A (carta de intención)"
        counter = fmt_price(o["counteroffer_amount_mxn"]) if o.get("counteroffer_amount_mxn") and o["counteroffer_amount_mxn"] != "0" else "Sin contraoferta"
        status = status_labels.get(o["offer_status"], o["offer_status"].title())
        closing = o["closing_window_days"] or "N/D"
        financing = o["financing_type"].title()
        deposit = f"{o['deposit_pct']}%" if o.get("deposit_pct") and o["deposit_pct"] != "0" else "Sin enganche"
        notes = o["notes_internal"] or "Sin notas."

        tags = [oid.lower(), pid.lower(), lid.lower(), aid.lower(),
                o["offer_status"].replace(" ", "_")]

        doc = f"""---
title: "Memo de negociación {oid}: {pid} — {lid}"
doc_type: negotiation_notes
category: restricted
audience: director
purpose: "Registro confidencial del estado de la oferta y estrategia de negociación."
source:
  - offers.csv
status: final
version: v01
date: {TODAY}
entity: offer
language: es
tags:{tag_list(*tags)}
summary: "{oid} — {pid} con {lid} — {status} — Oferta: {amount}"
owner: direccion
doc_id: kb-res-{oid.lower()}
offer_id: {oid}
property_id: {pid}
lead_id: {lid}
agent_id: {aid}
offer_status: "{o['offer_status']}"
---

# Memo de negociación — {oid}

**Propiedad:** {pid} · **Prospecto:** {lid} · **Agente:** {aid}

> ⚠️ **RESTRINGIDO** — Información confidencial de negociación. Solo dirección y agente asignado.

---

## Estado de la oferta

| Campo | Valor |
|---|---|
| Estado actual | **{status}** |
| Fecha de oferta | {o['offer_date']} |
| Monto ofertado | **{amount}** |
| Contraoferta | {counter} |
| Ventana de cierre | {closing} días |
| Tipo de financiamiento | {financing} |
| Enganche / depósito | {deposit} |

---

## Notas de negociación

> **Uso exclusivo de dirección y agente asignado. No compartir con prospectos ni propietarios.**

{notes}

---

*Documento restringido · Meridiana · {TODAY}*
"""
        path = os.path.join(KB, "restricted", "deals", f"{oid}.md")
        write_doc(path, doc)

    print(f"  ✓ Memos de negociación generados ({len(offers)})")


# ════════════════════════════════════════════════════════════════════════════
# 8. INTERNAL — Playbook de servicio de lujo
# ════════════════════════════════════════════════════════════════════════════

def gen_playbook():
    doc = """---
title: "Playbook de servicio de lujo — Meridiana"
doc_type: luxury_service_playbook
category: internal
audience: agent
purpose: "Guía operativa para el equipo comercial sobre estándares de atención en segmento premium y ultra."
source: []
status: final
version: v01
date: """ + TODAY + """
entity: company
language: es
tags:
  - playbook
  - servicio
  - lujo
  - protocolo
summary: "Estándares y protocolos de atención para propiedades del segmento premium y ultra en Meridiana."
owner: direccion
doc_id: kb-int-playbook-lujo
---

# Playbook de servicio de lujo — Meridiana

> *Uso exclusivo del equipo Meridiana. No compartir externamente.*

---

## 1. Calificación del prospecto

Antes de mostrar cualquier propiedad del segmento ultra o premium se debe verificar:

- **Capacidad financiera:** liquidez confirmada o preaprobación bancaria formal.
- **Seriedad de intención:** timeline de compra definido (máximo 12 meses).
- **Perfil de uso:** uso propio, inversión o renta corporativa.
- **Vetting básico:** referencia de cliente existente, perfil profesional verificable o contacto institucional.

No invertir tiempo de visita en prospectos sin al menos dos de estos cuatro criterios.

---

## 2. Preparación de la visita

### Para propiedades ultra ($15M MXN en adelante):
- Coordinar transporte desde el hotel o punto de reunión del cliente.
- Preparar presentación impresa encuadernada (dossier de la propiedad).
- Confirmar disponibilidad del propietario o apoderado para preguntas en sitio.
- Llevar café, agua o cortesía acorde al nivel del cliente.
- Verificar que el inmueble esté en condiciones óptimas: clima encendido, luces encendidas, jardín presentable.

### Para propiedades premium ($6M–$15M MXN):
- Material digital de la propiedad enviado 24h antes.
- Tour preparado con orden de recorrido definido (iniciar por el punto más impactante).
- Conocer de memoria las tres objeciones más probables y sus respuestas.

---

## 3. Durante la visita

- **Escuchar más de lo que se habla.** Identificar qué elemento conecta emocionalmente con el cliente.
- **No presionar.** El cliente de alto valor detecta urgencia artificial y se aleja.
- **Documentar objeciones** en tiempo real. Cada objeción es información de negociación.
- **No revelar información del vendedor** que no esté autorizada: circunstancias personales, urgencias, precio mínimo real.

---

## 4. Protocolo de confidencialidad

Algunos propietarios tienen condiciones específicas de privacidad:

- **Confidencialidad alta:** no publicar nombre del propietario, coordinar visitas con 48h de anticipación mínima.
- **Confidencialidad muy alta:** solo el agente asignado puede comunicarse con el propietario o su apoderado. No registrar detalles sensibles en canales compartidos.

Consultar siempre el perfil del propietario antes de cualquier comunicación o presentación.

---

## 5. Manejo de ofertas y negociación

- Registrar todas las ofertas en el sistema, incluso las verbales o informativas.
- No revelar la existencia de otras ofertas activas sobre la misma propiedad, salvo autorización explícita de dirección.
- Crear urgencia real (datos de mercado, comparables, actividad reciente) sin fabricar presión falsa.
- Cualquier operación con pago en moneda extranjera, criptomonedas o condiciones inusuales debe ser revisada por el área de legal y cumplimiento (AGT-15) antes de cualquier compromiso.

---

## 6. Cierre y postventa

- Acompañar al cliente hasta la firma notarial.
- Presentar al cliente con el notario elegido si no tiene uno.
- Hacer seguimiento 30 días después del cierre: ¿todo en orden? ¿alguna necesidad adicional?
- Mantener la relación: clientes de lujo son la principal fuente de referidos futuros.

---

*Documento interno · Meridiana · """ + TODAY + """*
"""
    path = os.path.join(KB, "internal", "playbooks", "luxury-service-playbook.md")
    write_doc(path, doc)
    print("  ✓ Playbook de servicio de lujo generado")


# ════════════════════════════════════════════════════════════════════════════
# 9. INTERNAL — Perfiles internos de agente (con KPIs)
# ════════════════════════════════════════════════════════════════════════════

def gen_internal_agents(agents, properties, offers):
    # Contar propiedades activas por agente
    props_by_agent = {}
    for p in properties:
        aid = p["agent_id"]
        props_by_agent.setdefault(aid, []).append(p)

    # Contar ofertas por agente
    offers_by_agent = {}
    for o in offers:
        aid = o["agent_id"]
        offers_by_agent.setdefault(aid, []).append(o)

    agent_map = {a["agent_id"]: a for a in agents}

    for a in agents:
        aid = a["agent_id"]
        name = a["full_name"]
        role = a["role"].title()

        manager = agent_map.get(a["manager_id"], {})
        manager_name = manager.get("full_name", "—") if a["manager_id"] != aid else "—"

        my_props = props_by_agent.get(aid, [])
        active_props = [p for p in my_props if p["status"] == "activa"]
        my_offers = offers_by_agent.get(aid, [])
        closed = [o for o in my_offers if o["offer_status"] in ("aceptada", "carta de intención firmada")]

        tags = [aid.lower(), a["seniority"], a["role"].replace(" ", "_")]

        doc = f"""---
title: "Perfil interno de asesor: {name} ({aid})"
doc_type: agent_profile_internal
category: internal
audience: internal_team
purpose: "Ficha interna del asesor con datos operativos y de desempeño."
source:
  - agents.csv
  - properties.csv
  - offers.csv
status: final
version: v01
date: {TODAY}
entity: agent
language: es
tags:{tag_list(*tags)}
summary: "{name} — {role} — {a['seniority'].title()} — Comisión: {a['commission_pct']}%"
owner: direccion
doc_id: kb-int-agt-{aid.lower()}
agent_id: {aid}
---

# Perfil interno — {name}

**{aid}** · {role} · {a['seniority'].title()}

> *Uso interno del equipo Meridiana.*

---

## Datos del asesor

| Campo | Valor |
|---|---|
| Nombre | {name} |
| Email | {a['email']} |
| Teléfono | {a['phone']} |
| Rol | {role} |
| Nivel | {a['seniority'].title()} |
| Reporte a | {manager_name} |
| Activo | {a['active'].title()} |

---

## Especialidad comercial

| Campo | Valor |
|---|---|
| Zona geográfica | {a['specialty_zone'] or '—'} |
| Tipo de propiedad | {a['specialty_property_type'] or '—'} |
| Idiomas | {a['languages']} |
| Comisión | {a['commission_pct']}% |

---

## Actividad en cartera

| Métrica | Valor |
|---|---|
| Propiedades asignadas | {len(my_props)} |
| Propiedades activas | {len(active_props)} |
| Ofertas gestionadas | {len(my_offers)} |
| Cierres confirmados | {len(closed)} |

### Propiedades asignadas
{"".join(f"- {p['property_id']}: {p['commercial_name']} ({p['status']})\\n" for p in my_props) or "Ninguna."}

---

*Documento interno · Meridiana · {TODAY}*
"""
        path = os.path.join(KB, "internal", "playbooks", f"agent-internal-{aid}.md")
        write_doc(path, doc)

    print(f"  ✓ Perfiles internos de agente generados ({len(agents)})")


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Cargando CSVs...")
    properties = read_csv("properties.csv")
    agents = read_csv("agents.csv")
    owners = read_csv("owners.csv")
    leads = read_csv("leads.csv")
    viewings = read_csv("viewings.csv")
    offers = read_csv("offers.csv")
    features = read_csv("property_features.csv")

    print(f"  {len(properties)} propiedades · {len(agents)} agentes · {len(owners)} propietarios")
    print(f"  {len(leads)} leads · {len(viewings)} visitas · {len(offers)} ofertas")
    print(f"  {len(features)} características de propiedad")
    print()

    print("Generando knowledge_base/public/...")
    gen_public_properties(properties, features, agents)
    gen_public_agents(agents)
    gen_public_company()

    print("\nGenerando knowledge_base/internal/...")
    gen_internal_leads(leads)
    gen_internal_viewings(viewings)
    gen_internal_agents(agents, properties, offers)
    gen_playbook()

    print("\nGenerando knowledge_base/internal/ + restricted/ (propietarios)...")
    gen_owners(owners)

    print("\nGenerando knowledge_base/restricted/...")
    gen_restricted_offers(offers)

    # Conteo final
    total = 0
    for root, dirs, files in os.walk(KB):
        for f in files:
            if f.endswith(".md"):
                total += 1
    print(f"\n✅ Listo. {total} documentos generados en knowledge_base/")
