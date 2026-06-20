#!/usr/bin/env python3
"""
Genera knowledge_base/internal/interactions/ desde interactions.csv.
Un documento por lead con todo su historial de contacto agrupado cronológicamente.
"""

import csv
import os
from collections import defaultdict
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
RAW  = os.path.join(BASE, "..", "datasets/raw")
KB   = os.path.join(BASE, "..", "knowledge_base")
TODAY = date.today().isoformat()

CHANNEL_LABEL = {
    "instagram": "Instagram DM",
    "whatsapp": "WhatsApp",
    "email": "Email",
    "llamada": "Llamada telefónica",
    "visita presencial": "Visita presencial",
    "videollamada": "Videollamada",
    "referido": "Contacto por referido",
    "portal inmobiliario": "Portal inmobiliario",
    "feria inmobiliaria": "Feria inmobiliaria",
    "sitio web meridiana": "Sitio web Meridiana",
}

DIRECTION_LABEL = {
    "entrante": "Entrada",
    "saliente": "Salida",
}

SENTIMENT_EMOJI = {
    "muy positivo": "🟢",
    "positivo": "🔵",
    "neutral": "⚪",
    "negativo": "🔴",
}


def read_csv(name):
    path = os.path.join(RAW, name)
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_doc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def gen_interaction_histories():
    interactions = read_csv("interactions.csv")
    leads        = read_csv("leads.csv")
    agents       = read_csv("agents.csv")

    lead_map  = {l["lead_id"]: l for l in leads}
    agent_map = {a["agent_id"]: a for a in agents}

    # Agrupar por lead
    by_lead = defaultdict(list)
    for row in interactions:
        by_lead[row["lead_id"]].append(row)

    # Ordenar cada grupo cronológicamente
    for lid in by_lead:
        by_lead[lid].sort(key=lambda r: r["interaction_datetime"])

    out_dir = os.path.join(KB, "internal", "interactions")
    count = 0

    for lid, rows in sorted(by_lead.items()):
        lead = lead_map.get(lid, {})
        lead_name  = lead.get("full_name", lid)
        score      = lead.get("qualification_score", "—")
        stage      = lead.get("lead_status", "—")
        b_min      = lead.get("budget_min_mxn", "")
        b_max      = lead.get("budget_max_mxn", "")
        try:
            budget_fmt = f"${int(float(b_min)):,} – ${int(float(b_max)):,} MXN"
        except (ValueError, TypeError):
            budget_fmt = "—"

        # Agentes involucrados (únicos, en orden de aparición)
        seen_agents = []
        for r in rows:
            agt_id = r["agent_id"]
            if agt_id and agt_id not in seen_agents:
                seen_agents.append(agt_id)
        agt_names = ", ".join(
            agent_map[a]["full_name"] for a in seen_agents if a in agent_map
        ) or "—"

        # Propiedades mencionadas (únicas)
        props = sorted({r["property_id"] for r in rows if r["property_id"]})
        props_str = ", ".join(props) if props else "—"

        # Última acción pendiente
        last = rows[-1]
        next_action     = last.get("next_action", "—")
        next_action_due = last.get("next_action_due", "—")

        # Tabla de interacciones
        lines = []
        for r in rows:
            iid       = r["interaction_id"]
            dt        = r["interaction_datetime"][:10]
            channel   = CHANNEL_LABEL.get(r["channel"], r["channel"])
            direction = DIRECTION_LABEL.get(r["direction"], r["direction"])
            sentiment = r.get("sentiment", "")
            emoji     = SENTIMENT_EMOJI.get(sentiment, "⚪")
            intent    = r.get("intent", "—")
            prop_ref  = r["property_id"] if r["property_id"] else "—"
            summary   = r["summary"]
            lines.append(
                f"### {iid} — {dt}  |  {channel} ({direction})  {emoji}\n"
                f"**Propiedad:** {prop_ref}  |  **Intención:** {intent}  |  **Sentimiento:** {sentiment}\n\n"
                f"{summary}\n\n"
                f"**Próxima acción:** {r.get('next_action', '—')}  "
                f"(due: {r.get('next_action_due', '—')})\n"
            )

        interactions_block = "\n---\n\n".join(lines)

        doc = f"""---
doc_id: HIST-{lid}
doc_type: interaction_history
access_level: internal
lead_id: {lid}
lead_name: {lead_name}
agents: {agt_names}
properties_referenced: {props_str}
total_interactions: {len(rows)}
qualification_score: {score}
stage: {stage}
budget: {budget_fmt}
next_action: {next_action}
next_action_due: {next_action_due}
generated: {TODAY}
---

# Historial de contacto — {lead_name} ({lid})

**Score de calificación:** {score}  |  **Etapa:** {stage}  |  **Presupuesto:** {budget_fmt}
**Agente(s):** {agt_names}
**Propiedades referenciadas:** {props_str}
**Total de interacciones:** {len(rows)}

---

## Interacciones

{interactions_block}

---

## Próxima acción pendiente

**{next_action}**
Fecha límite: {next_action_due}
"""

        path = os.path.join(out_dir, f"{lid}-historial.md")
        write_doc(path, doc)
        count += 1

    print(f"  ✓ {count} historiales de contacto generados en knowledge_base/internal/interactions/")
    return count


if __name__ == "__main__":
    print("Generando historiales de contacto...")
    gen_interaction_histories()
    print("Listo.")
