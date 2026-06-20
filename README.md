# Meridiana

Archivos de una inmobiliaria ficticia usados como corpus para dos deployments de RAG, en el contexto de investigación de AI Safety.

Meridiana es una empresa inmobiliaria simulada con 38 propiedades, datos de propietarios, notas internas, comisiones y documentación operativa. Esos archivos se despliegan en dos configuraciones de RAG con distintos niveles de control, permitiendo estudiar fugas de información y comportamiento de seguridad en sistemas de IA.

---

## Deployments

### meridianav1 — RAG sin controles

Deployment naive: corpus sin auditar volcado en un solo índice vectorial, sin autenticación de rol ni system prompt defensivo. Reproduce lo que haría un desarrollador siguiendo tutoriales estándar (LangChain, LlamaIndex) sin considerar privacidad.

### meridianav3 — RAG con controles

Deployment con piso mínimo de seguridad: tres índices separados por nivel de acceso, corpus auditado, autenticación de rol en sesión, system prompt robusto y logging de eventos de seguridad.

| Control | v1 | v3 |
|---|---|---|
| Índices vectoriales | 1 único | 3 separados por nivel |
| Corpus | Sin auditar (con datos sensibles) | Auditado |
| Autenticación de rol | No | Sesión autenticada |
| System prompt | Genérico | Anti-jailbreak |
| Filtro post-retrieval | No | Por rol |
| Logging | No | Con `SECURITY_EVENT`s |

---

## Estructura

```
Meridiana/
├── meridianav1/          # Archivos de la empresa + deployment sin controles
│   ├── datasets/         # CSVs fuente
│   ├── knowledge_base/   # Corpus generado (public / internal / restricted)
│   ├── prompts/
│   ├── config/
│   └── eval/             # Queries, ataques y resultados
├── meridianav3/          # Mismos archivos + deployment con controles
│   ├── datasets/
│   ├── knowledge_base/
│   ├── prompts/
│   ├── config/
│   └── eval/
├── notebooks/            # Pipeline de ETL y generación del corpus
├── scripts/              # ETL y generación sintética de contenido
└── outputs/
```

---

## Pipeline de generación del corpus

```
CSVs fuente (datasets/raw/)
    ↓  etl.py
property_master.parquet / .jsonl
    ↓  generate.py
Contenido sintético (JSON)
    ↓  Template renderer
Archivos del knowledge_base (HTML, MD)
```

---

## Comandos útiles

```bash
# Auditar corpus v1 (muestra fugas)
python3 meridianav3/scripts/audit_corpus.py meridianav1/

# Auditar corpus v3 (debe estar limpio)
python3 meridianav3/scripts/audit_corpus.py

# Regenerar corpus naive (v1)
python3 meridianav1/scripts/generate_kb_naive.py

# Regenerar corpus seguro (v3)
python3 meridianav3/scripts/generate_kb.py
```

---

## Licencia

MIT — ver [LICENSE](LICENSE).
