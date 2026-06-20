#!/usr/bin/env python3
"""
Auditoría de corpus — Meridiana v3.

Verifica que ningún documento en knowledge_base/public/ contiene
campos o patrones sensibles que no deberían estar expuestos.

Ejecutar antes de indexar:
    python3 scripts/audit_corpus.py

Exit code 0 = corpus limpio.
Exit code 1 = se encontraron fugas — NO indexar hasta resolver.
"""

import os
import re
import sys

if len(sys.argv) > 1:
    BASE = os.path.abspath(sys.argv[1])
else:
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_KB = os.path.join(BASE, "knowledge_base", "public")

# Patrones de texto que nunca deben aparecer en docs públicos
FORBIDDEN_PATTERNS = [
    # Campos internos de properties.csv
    (r"proceso de divorcio", "internal_summary: circunstancia personal del vendedor"),
    (r"manejo con extrema discreción", "internal_summary: instrucción interna"),
    (r"urgido|ha bajado precio", "internal_summary: urgencia del vendedor"),
    (r"precio con margen real", "internal_summary: precio mínimo real"),
    (r"permuta parcial", "internal_summary: condición de negociación"),
    (r"USDT|criptomoneda", "internal_summary: método de pago no estándar"),
    (r"due diligence", "internal_summary: proceso legal interno"),
    (r"fideicomiso familiar con tres herederos", "internal_summary: estructura legal interna"),
    (r"Vendedor motivado|Vendedor urgido", "internal_summary: perfil del vendedor"),
    # Datos de propietarios
    (r"@protonmail\.com|@icloud\.com", "contacto privado del propietario"),
    (r"OWN-\d{3}", "owner_id expuesto"),
    (r"confidencialidad.*alta|muy alta", "nivel de confidencialidad del propietario"),
    (r"apoderado.*legal|representante.*legal", "dato de representación legal del propietario"),
    # Datos de agentes
    (r"commission_pct|Comisión: \d", "comisión del agente"),
    (r"manager_id", "jerarquía interna de agentes"),
    # Datos de negociación
    (r"oferta.*\$\d+,\d{3},\d{3}", "monto de oferta activa"),
    (r"contraoferta", "información de negociación"),
    # Scores internos
    (r"qualification_score|score.*\d{2}/100", "score de calificación interno"),
    # Días en mercado (posición negociadora)
    (r"Días en mercado", "dato de posición negociadora"),
]

# Campos de frontmatter que no deben estar en docs públicos
FORBIDDEN_FRONTMATTER_KEYS = [
    "internal_summary",
    "notes_internal",
    "qualification_score",
    "commission_pct",
    "manager_id",
    "owner_id",
    "days_on_market",
    "confidentiality_level",
]


def audit_file(filepath):
    issues = []
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # Check forbidden patterns in content
    for pattern, description in FORBIDDEN_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"PATRÓN PROHIBIDO [{description}]: '{pattern}'")

    # Check forbidden frontmatter keys
    in_frontmatter = False
    for line in content.split("\n"):
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            for key in FORBIDDEN_FRONTMATTER_KEYS:
                if line.strip().startswith(f"{key}:"):
                    issues.append(f"CAMPO PROHIBIDO EN FRONTMATTER: '{key}'")

    return issues


def main():
    total_files = 0
    total_issues = 0
    files_with_issues = []

    print(f"Auditando corpus público: {PUBLIC_KB}\n")

    for root, dirs, files in os.walk(PUBLIC_KB):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            total_files += 1
            issues = audit_file(fpath)
            if issues:
                rel = os.path.relpath(fpath, BASE)
                files_with_issues.append((rel, issues))
                total_issues += len(issues)

    # Report
    if files_with_issues:
        print(f"❌ CORPUS CON FUGAS — {len(files_with_issues)} archivos con problemas:\n")
        for fpath, issues in files_with_issues:
            print(f"  📄 {fpath}")
            for issue in issues:
                print(f"     ⚠️  {issue}")
            print()
        print(f"Total: {total_issues} problemas en {len(files_with_issues)}/{total_files} archivos.")
        print("\nNO indexar este corpus hasta resolver las fugas.")
        print("Regenerar con scripts/generate_kb.py (versión segura, no naive).")
        sys.exit(1)
    else:
        print(f"✅ Corpus limpio — {total_files} archivos auditados, ninguna fuga detectada.")
        print("El corpus está listo para indexar.")
        sys.exit(0)


if __name__ == "__main__":
    main()
