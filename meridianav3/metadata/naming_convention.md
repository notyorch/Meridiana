# Convención de nombres

## Propósito

Este documento define una forma simple y consistente de nombrar archivos, documentos y versiones dentro del sistema Meridiana. La convención busca ser fácil de aplicar por un equipo pequeño, evitar duplicados y permitir que cualquier persona identifique rápido el tipo de documento, la entidad y la versión. Se apoya en la estructura del proyecto, el esquema del dataset y el tono editorial sobrio de la marca. [file:2][file:3][file:1]

## Patrón general

### Formato recomendado

`[categoria]_[entidad]_[tema]_[yyyymmdd]_v[##].md`

### Significado de cada parte

- `categoria`: indica el tipo general de documento, por ejemplo `public`, `internal`, `restricted` o `template`.
- `entidad`: nombre corto de la entidad principal, por ejemplo `property`, `lead`, `owner`, `agent`, `viewing`, `offer`, `interaction`, `features`.
- `tema`: descriptor breve del contenido, en minúsculas y con guiones bajos si hace falta.
- `yyyymmdd`: fecha de creación o última actualización.
- `v[##]`: número de versión con dos dígitos, por ejemplo `v01`, `v02`, `v03`.

## Reglas de uso

- Usar solo minúsculas.
- No usar acentos, espacios ni caracteres especiales.
- Separar cada bloque con guion bajo.
- Mantener los temas cortos y descriptivos.
- No mezclar en el nombre información sensible que no deba verse a simple vista.
- Si el documento es plantilla, usar la categoría `template`.
- Si el documento está publicado para clientes, usar `public`.
- Si el documento es de uso interno, usar `internal`.

## Regla de versionado

### Versión principal

La primera versión de un documento es siempre `v01`.
Cada cambio relevante incrementa una unidad: `v02`, `v03`, `v04`.

### Cuándo subir versión

- Cambios de contenido sustancial.
- Ajustes de tono o estructura.
- Actualización de datos que altere el documento final.
- Correcciones posteriores a revisión.

### Cuándo no subir versión

- Correcciones menores de formato.
- Cambios de espacio, ortografía o maquetación sin impacto de contenido.
- Ediciones temporales no guardadas como versión final.

## Ejemplos concretos

### Documentos públicos

- `public_property_brochure_casa_chochol_20260614_v01.md`
- `public_agent_profile_maria_lopez_20260614_v01.md`
- `public_lead_faq_buyers_20260614_v01.md`

### Documentos internos

- `internal_lead_qualification_l039_20260614_v01.md`
- `internal_viewing_summary_p037_l039_20260614_v02.md`
- `internal_offer_notes_o012_20260614_v01.md`

### Plantillas

- `template_property_listing_longform_20260614_v01.md`
- `template_owner_profile_20260614_v01.md`
- `template_negotiation_notes_20260614_v01.md`

## Convención práctica para equipo pequeño

Para una operación pequeña, la regla más útil es que el nombre responda tres preguntas: qué es, para quién sirve y de cuándo es. Si el documento es fácil de localizar en una carpeta compartida, la convención está funcionando. Meridiana puede mantener el sistema simple con solo cuatro categorías base: `public`, `internal`, `restricted` y `template`. [file:2][file:3]

## Recomendación final

Cuando exista duda entre un nombre largo y uno corto, conviene preferir el corto mientras siga siendo inequívoco. La consistencia vale más que la granularidad excesiva. El objetivo es que el equipo pueda nombrar documentos rápido, sin perder orden ni legibilidad. [file:2][file:3]
