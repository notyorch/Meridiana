# Meridiana v1 — Implementación estándar de pyme (baseline vulnerable)

## Propósito en la investigación

Meridiana v1 representa cómo una pyme mexicana típica implementaría un RAG siguiendo
documentación estándar (LangChain, LlamaIndex, tutoriales de OpenAI). Sin conocimiento
de riesgos de privacidad, el desarrollador promedio:

- Vuelca todos los campos del CSV al corpus sin filtrar
- Usa un solo índice vectorial para todos los documentos
- No implementa control de roles
- Usa un system prompt genérico de 2-3 líneas
- No tiene logging ni auditoría

**Este repo es el baseline vulnerable.** Las vulnerabilidades son intencionales
y están documentadas para fines de investigación comparativa.

## Fugas documentadas en este corpus

- `internal_summary` de propiedades: estrategia de venta, circunstancias personales del vendedor
- Datos de contacto de propietarios: email, teléfono
- Notas internas de propietarios: confidencialidad, condiciones de manejo
- Comisiones de asesores
- Días en mercado (posición negociadora)
- Un solo índice: documentos `restricted` accesibles con las queries correctas

## Comparar contra

- **meridianav3:** implementación con controles de seguridad (índices separados,
  corpus auditado, system prompt robusto, filtrado por rol)

## Cómo reproducir las vulnerabilidades

```bash
# Regenerar corpus vulnerable (naive)
python3 scripts/generate_kb_naive.py

# Auditar y ver las fugas
python3 meridianav3/scripts/audit_corpus.py meridianav1/
# → 37/55 archivos con fugas detectadas

# Correr ataques de evaluación
# Ver eval/phase1_standard/queries/attack_prompts.json
```

## Tree

meridianav1/
├── config/
│   └── rag_config.md          ← configuración naive del RAG
├── datasets/
│   ├── raw/                   ← CSVs fuente de verdad
│   └── processed/
├── brand/
├── knowledge_base/
│   ├── public/                ← corpus con fugas (generado por generate_kb_naive.py)
│   ├── internal/              ← mezclado en el mismo índice en v1
│   └── restricted/            ← accesible desde el mismo índice en v1
├── templates/
├── generated/
├── properties/                ← assets de propiedades (PNG + HTML) — NO mover
├── metadata/
├── prompts/
├── scripts/
│   ├── generate_kb.py         ← generador seguro (para referencia)
│   └── generate_kb_naive.py   ← generador naive (el que pobló este corpus)
├── eval/
│   ├── phase1_standard/       ← queries, ataques y resultados del baseline
│   └── phase2_secure/         ← controles y leakage tests
└── tests/
    ├── golden_set/
    ├── fixtures/
    └── adversarial/

## Operating rules (v1 — sin controles)

- Un solo índice vectorial con todos los documentos
- Sin autenticación de rol
- Sin filtrado post-retrieval
- System prompt genérico
- Sin auditoría del corpus
