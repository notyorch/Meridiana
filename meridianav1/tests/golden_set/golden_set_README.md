---
title: "README — Golden Set de Meridiana RAG"
doc_type: readme
category: internal
audience: internal_team
purpose: "Instrucciones de uso del golden set para evaluación del RAG."
status: final
date: 2026-06-14
doc_id: tests-golden-set-readme
---

# Golden Set — Meridiana RAG

## Qué es

`golden_qa.json` contiene 10 pares Q&A validados manualmente que sirven como ground truth para evaluar el rendimiento del RAG en condiciones controladas. Son los casos más representativos del sistema: cubren los tres roles, tipos de consulta más frecuentes y situaciones críticas de privacidad.

---

## Cómo usar el golden set

### Evaluación manual

1. Para cada entrada en `golden_qa.json`, hacer la query al RAG con el rol especificado
2. Comparar la respuesta con `ground_truth_answer`
3. Verificar que todos los `required_fields` están presentes en la respuesta
4. Verificar que ningún `forbidden_fields` aparece en la respuesta
5. Registrar resultado: PASA / FALLA / PARCIAL

### Evaluación automática (LLM-as-judge)

```python
# Pseudocódigo para evaluación automática
for golden in golden_qa:
    response = rag.query(golden["query"], role=golden["role"])
    
    # Check required fields
    required_pass = all(field in response for field in golden["required_fields"])
    
    # Check forbidden fields
    forbidden_pass = not any(field in response for field in golden["forbidden_fields"])
    
    result = "PASA" if required_pass and forbidden_pass else "FALLA"
    log(golden["golden_id"], result, response)
```

---

## Distribución de casos

| Golden ID | Rol | Dificultad | Tipo |
|---|---|---|---|
| G001 | client | fácil | Precio exacto de propiedad |
| G002 | client | medio | Comparativa entre dos propiedades |
| G003 | client | medio | Filtrado por precio de renta |
| G004 | client | fácil | Perfil de agente por especialidad |
| G005 | client | fácil | FAQ: proceso de compra |
| G006 | client | medio | Característica específica (licencia) |
| G007 | agent | medio | Cartera de agente (internal) |
| G008 | agent | difícil | Cruce de visita + lead (internal) |
| G009 | director | difícil | Dos ofertas activas simultáneas (restricted) |
| G010 | client | medio | Cobertura geográfica fuera de Mérida |

---

## Métricas objetivo

| Métrica | Phase 1 baseline | Phase 2 seguro |
|---|---|---|
| Precision@1 (G001–G006, G010) | — | — |
| No-leakage rate (forbidden_fields) | — | — |
| Internal access control (G007–G008) | — | — |
| Restricted access control (G009) | — | — |

*Los valores se rellenan durante la evaluación.*

---

## Cuándo actualizar el golden set

- Cuando se agreguen nuevas propiedades al inventario
- Cuando cambie el status de una propiedad relevante (venta, retiro del mercado)
- Cuando se identifique un nuevo patrón de falla no cubierto por los casos actuales
- No más de una vez por sprint para mantener estabilidad del benchmark

---

*Tests · Meridiana · 2026-06-14*
