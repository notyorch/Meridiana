# Meridiana v3 — Implementación con controles de seguridad

## Propósito en la investigación

Meridiana v3 representa la implementación objetivo: lo que *debería* hacer una pyme
mexicana que maneja datos sensibles de clientes, propietarios y negociaciones en un RAG.

No es una implementación perfecta — es el piso mínimo razonable para una operación
inmobiliaria que cumple expectativas básicas de privacidad. Sigue siendo evaluable
para vulnerabilidades residuales.

## Controles implementados vs v1

| Control | v1 | v3 |
|---|---|---|
| Índices vectoriales | 1 único | 3 separados por nivel |
| Campos en corpus público | Todos (con fugas) | Auditados, sin datos sensibles |
| Autenticación de rol | No | Sesión autenticada |
| System prompt | 3 líneas genéricas | Robusto con anti-jailbreak |
| Filtro post-retrieval | No | Por categoría y rol |
| Sanitización de output | No | Patrones sensibles detectados |
| Auditoría del corpus | No | audit_corpus.py antes de indexar |
| Logging | No | Con SECURITY_EVENTs |

## Vulnerabilidades residuales (para investigación)

Incluso con estos controles, v3 puede ser vulnerable a:
- Inferencia estadística por consultas múltiples
- Membership inference
- Adversarial embeddings
- Model memorization del LLM base
- Timing attacks

Ver eval/phase2_secure/ para los casos de evaluación.

## Cómo verificar que el corpus es limpio

```bash
# Auditar v3 antes de indexar
python3 scripts/audit_corpus.py
# -> Corpus limpio — 55 archivos auditados, ninguna fuga detectada.

# Comparar contra v1 (debe mostrar fugas)
python3 scripts/audit_corpus.py ../meridianav1/
# -> 37/55 archivos con fugas
```

## Tree

meridianav3/
├── config/
│   └── rag_config.md          <- configuración segura del RAG con controles
├── datasets/
│   ├── raw/                   <- mismos CSVs que v1 (fuente de verdad compartida)
│   └── processed/
├── brand/
├── knowledge_base/
│   ├── public/                <- corpus auditado (sin fugas)
│   ├── internal/              <- índice separado, accesible para agentes
│   └── restricted/            <- índice separado, accesible solo para director
├── templates/
├── generated/
├── properties/                <- assets de propiedades (PNG + HTML) — NO mover
├── metadata/
├── prompts/
├── scripts/
│   ├── generate_kb.py         <- generador seguro (excluye campos sensibles)
│   └── audit_corpus.py        <- auditor pre-indexación
├── eval/
│   ├── phase1_standard/       <- queries y ataques compartidos con v1
│   └── phase2_secure/         <- controles, leakage tests y vulnerabilidades residuales
└── tests/
    ├── golden_set/
    ├── fixtures/
    └── adversarial/

## Operating rules (v3 — con controles)

- Tres índices vectoriales separados por nivel de acceso
- Rol verificado desde sesión autenticada, no del mensaje del usuario
- Corpus auditado antes de indexar con audit_corpus.py
- System prompt con cláusulas anti-jailbreak y anti-override de rol
- Filtrado post-retrieval por categoría vs rol de sesión
- Sanitización de output con detección de patrones sensibles
- Logging completo de interacciones y SECURITY_EVENTs
