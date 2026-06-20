# Notebook 02 — Generation Playground

## Objetivo

Validar y diseñar el pipeline de generación sintética de contenido para Meridiana v1.

Este notebook tiene como finalidad transformar propiedades estructuradas en contenido narrativo listo para ser renderizado dentro de los templates documentales del proyecto.

El notebook debe enfocarse exclusivamente en generación de contenido.

No debe realizar ETL, limpieza de datos ni transformaciones estructurales complejas.

Toda la información consumida debe provenir del output validado del Notebook 01.

---

## Dependencias

### Entrada requerida

Generada por:

01_etl_playground.ipynb

Archivos esperados:

* property_master.parquet
* property_master.jsonl

---

## Alcance

### Entradas

Property Master consolidado.

Cada registro representa una propiedad completamente enriquecida y validada.

### Salidas

Contenido sintético estructurado para:

* property-brochure.html
* property-listing-longform.html

Opcionalmente:

* seo_snippets
* social_media_copy
* executive_summary
* property_highlights

---

## Fase 1 — Carga de datos

El notebook debe:

1. Leer property_master.
2. Validar estructura esperada.
3. Seleccionar una propiedad de prueba.
4. Construir contexto de generación.

El objetivo es trabajar inicialmente sobre un único registro para iterar rápidamente.

---

## Fase 2 — Diseño de prompts

Construir prompts reutilizables para generación inmobiliaria.

Los prompts deben aprovechar:

* datos estructurados
* ubicación
* precio
* atributos
* features
* amenidades
* contexto de marca

La generación debe enfocarse en beneficios y experiencia, no solamente en enumerar atributos.

Ejemplo:

Incorrecto:

"Casa con piscina y terraza."

Correcto:

"La piscina privada y las amplias áreas exteriores crean un entorno ideal para reuniones familiares y entretenimiento."

---

## Fase 3 — Definición del esquema de salida

La IA no debe generar HTML.

La IA debe generar únicamente contenido estructurado.

Ejemplo conceptual:

{
"headline": "",
"subheadline": "",
"executive_summary": "",
"property_highlights": [],
"longform_description": "",
"lifestyle_section": "",
"call_to_action": ""
}

Este esquema se convertirá en el contrato oficial entre generación y renderizado.

---

## Fase 4 — Generación de brochure

Generar contenido optimizado para property-brochure.html.

Objetivos:

* lectura rápida
* tono premium
* énfasis comercial
* mensajes claros
* alto impacto visual

Componentes sugeridos:

### Headline

Título comercial principal.

### Subheadline

Propuesta de valor resumida.

### Executive Summary

Descripción corta.

### Highlights

Lista de beneficios clave.

### Call To Action

Mensaje de cierre.

---

## Fase 5 — Generación de listing longform

Generar contenido optimizado para property-listing-longform.html.

Objetivos:

* profundidad descriptiva
* storytelling
* posicionamiento SEO
* contexto de estilo de vida

Componentes sugeridos:

### Introducción

Presentación de la propiedad.

### Lifestyle Narrative

Experiencia de vivir en la propiedad.

### Architectural Features

Elementos físicos relevantes.

### Location Context

Ventajas de la ubicación.

### Investment Perspective

Valor potencial para compradores o inversionistas.

### Closing Section

Cierre comercial.

---

## Fase 6 — Evaluación de calidad

Antes de escalar a todas las propiedades, validar:

### Consistencia

El texto debe reflejar correctamente los datos.

### Cobertura

Las features relevantes deben aparecer en el contenido.

### Hallucination Check

La IA no debe inventar:

* amenidades inexistentes
* ubicaciones inexistentes
* características no presentes en datasets

### Tono de marca

La narrativa debe alinearse con una inmobiliaria premium.

---

## Fase 7 — Batch Testing

Una vez validado el resultado para una propiedad:

Ejecutar sobre múltiples propiedades.

Objetivos:

* detectar repetición excesiva
* medir diversidad narrativa
* validar escalabilidad

Métricas sugeridas:

* longitud promedio
* similitud entre propiedades
* cobertura de features
* tiempo de generación

---

## Fase 8 — Persistencia

Guardar resultados estructurados.

Ejemplo:

generated_payloads/

├── property_001.json
├── property_002.json
└── property_003.json

Cada archivo debe contener exclusivamente contenido generado.

No debe almacenar HTML renderizado.

---

## Fase 9 — Preparación para renderizado

La salida de este notebook debe ser consumida posteriormente por un renderizador de templates.

Pipeline esperado:

Property Master
↓
LLM
↓
Generated Content JSON
↓
Template Renderer
↓
HTML Final

La generación y el renderizado deben permanecer desacoplados.

---

## Criterio de éxito

El notebook se considera exitoso cuando:

1. Puede generar contenido coherente para una propiedad.
2. El contenido refleja correctamente los datos estructurados.
3. No introduce información inexistente.
4. Produce salidas consistentes para brochure y listing.
5. El resultado puede insertarse directamente en los templates HTML sin intervención manual.
6. La misma arquitectura puede escalar de 1 a 38 propiedades sin modificaciones sustanciales.

La salida de este notebook se convierte en la capa oficial de generación sintética de Meridiana v1.
