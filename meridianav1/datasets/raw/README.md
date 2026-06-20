# Meridiana — Dataset de CRM Inmobiliario

## Qué es Meridiana

Meridiana es una inmobiliaria boutique con sede en Mérida, Yucatán. Opera en el segmento de clase media alta y alto poder adquisitivo. No es una agencia de volumen. Es una firma de relaciones: pocos agentes, propiedades seleccionadas, clientes discretos.

Su cartera cubre la ciudad de Mérida y su zona metropolitana inmediata, incluyendo el corredor norte (Altabrisa, Montejo, Temozón Norte, Yucatán Country Club), el centro histórico, municipios cercanos (Conkal, Cholul, Progreso, Valladolid) y propiedades especiales como haciendas restauradas y terrenos con vocación turística.

El equipo tiene 15 personas: un director, tres senior advisors, cuatro advisors, cuatro junior advisors y tres personas de soporte (marketing, operaciones y legal). Cuatro agentes activos cubren la cartera de propiedades en este dataset.

La identidad de marca es negra, tipográfica y sin ornamentos. No usa superlativos. Describe con precisión. Trato discreto con clientes de alto perfil.

---

## Propósito del dataset

Este dataset fue diseñado para construir y probar sistemas de recuperación de información (RAG), pipelines de CRM, análisis de ventas, modelos de scoring y dashboards sobre datos inmobiliarios reales en Yucatán. Todos los datos son sintéticos pero semánticamente consistentes: nombres, colonias, precios, narrativas y relaciones entre tablas reflejan el comportamiento real del mercado premium de Mérida.

Los campos `notes_internal`, `internal_summary`, `feedback_summary` y `summary` contienen texto narrativo denso diseñado específicamente para retrieval semántico.

---

## Resumen de datasets

| Archivo | Filas | Columnas | Entidad principal |
|---|---|---|---|
| `properties.csv` | 38 | 30 | Inventario de propiedades |
| `agents.csv` | 15 | 12 | Equipo Meridiana |
| `owners.csv` | 38 | 12 | Propietarios |
| `leads.csv` | 40 | 19 | Prospectos y compradores |
| `interactions.csv` | 65 | 13 | Historial de contacto |
| `viewings.csv` | 35 | 11 | Visitas a propiedades |
| `offers.csv` | 20 | 12 | Ofertas y negociaciones |
| `property_features.csv` | 149 | 5 | Características premium desnormalizadas |

---

## Esquema y llaves

### `properties.csv`
**Llave primaria:** `property_id`
**Llaves foráneas:** `agent_id → agents.agent_id`, `owner_id → owners.owner_id`

| Columna | Tipo | Descripción |
|---|---|---|
| `property_id` | string PK | Identificador único de la propiedad (P001–P038) |
| `listing_code` | string | Código público de listado (ej. MER-2024-001) |
| `title` | string | Título de la ficha para portales y fichas |
| `property_type` | enum | `casa`, `depto`, `townhouse`, `terreno`, `villa` |
| `listing_type` | enum | `venta`, `renta` |
| `status` | enum | `activa`, `apartada`, `vendida`, `rentada`, `borrador` |
| `price_mxn` | integer | Precio en pesos mexicanos |
| `maintenance_fee_mxn` | integer | Cuota mensual de mantenimiento (0 si no aplica) |
| `bedrooms` | integer | Número de recámaras |
| `bathrooms` | float | Número de baños (0.5 = medio baño) |
| `parking_spaces` | integer | Cajones de estacionamiento |
| `construction_m2` | integer | Metros cuadrados de construcción |
| `lot_m2` | integer | Metros cuadrados de terreno (0 en deptos) |
| `year_built` | integer | Año de construcción (0 en terrenos) |
| `furnished` | enum | `sí`, `no` |
| `pet_friendly` | enum | `sí`, `no` |
| `address_line` | string | Dirección completa incluyendo colonia |
| `neighborhood` | string | Colonia |
| `municipality` | string | Municipio |
| `state` | string | Estado (siempre Yucatán) |
| `postal_code` | string | Código postal de 5 dígitos |
| `latitude` | float | Coordenada geográfica |
| `longitude` | float | Coordenada geográfica |
| `gated_community` | enum | `sí`, `no` (privada o fraccionamiento cerrado) |
| `luxury_tier` | enum | `ultra`, `premium`, `entrada` |
| `days_on_market` | integer | Días activa en cartera (0 si vendida o rentada) |
| `agent_id` | string FK | Agente responsable de la propiedad |
| `owner_id` | string FK | Propietario de la propiedad |
| `public_description` | text | Descripción para portales y fichas públicas |
| `internal_summary` | text | Notas internas del agente. Contiene contexto sensible no publicable |

**Distribución:** 17 casas · 11 deptos · 4 villas · 3 townhouses · 3 terrenos. Tiers: 12 ultra · 8 premium · 18 entrada.

---

### `agents.csv`
**Llave primaria:** `agent_id`
**Autoreferencia:** `manager_id → agents.agent_id` (AGT-01 apunta a sí mismo como nodo raíz)

| Columna | Tipo | Descripción |
|---|---|---|
| `agent_id` | string PK | Identificador del agente (AGT-01 a AGT-15) |
| `full_name` | string | Nombre completo |
| `email` | string | Correo corporativo en @meridiana.mx |
| `phone` | string | Teléfono con lada internacional |
| `role` | enum | `director`, `senior advisor`, `advisor`, `junior advisor`, `marketing coordinator`, `operations manager`, `legal & compliance` |
| `seniority` | enum | `senior`, `mid`, `junior`, `staff` |
| `specialty_zone` | string | Zonas de especialización geográfica (múltiples separadas por ·) |
| `specialty_property_type` | string | Tipos de propiedad de especialización |
| `languages` | string | Idiomas hablados |
| `commission_pct` | float | Porcentaje de comisión sobre precio de venta (0.0 para staff) |
| `manager_id` | string FK | Agente superior en la jerarquía |
| `active` | enum | `sí`, `no` |

**Jerarquía:** AGT-01 (director) → AGT-02, AGT-03, AGT-07, AGT-08, AGT-13 (seniors/mid) → juniors. Staff reporta directo al director. AGT-15 es legal y compliance.

---

### `owners.csv`
**Llave primaria:** `owner_id`
**Referenciada por:** `properties.owner_id`

| Columna | Tipo | Descripción |
|---|---|---|
| `owner_id` | string PK | Identificador del propietario (OWN-010 a OWN-038) |
| `owner_type` | enum | `persona física`, `persona moral`, `fideicomiso` |
| `owner_name` | string | Nombre o razón social |
| `contact_email` | string | Correo de contacto (vacío si toda comunicación es vía apoderado) |
| `contact_phone` | string | Teléfono de contacto |
| `preferred_contact_channel` | enum | `email`, `whatsapp`, `llamada` |
| `residency_country` | string | País de residencia fiscal |
| `legal_representative` | string | Nombre y correo del apoderado legal si aplica |
| `confidentiality_level` | enum | `baja`, `media`, `alta`, `muy alta` |
| `allow_public_photos` | enum | `sí`, `no` — si la propiedad puede aparecer en portales con fotos |
| `allow_open_house` | enum | `sí`, `no` — si se permiten visitas abiertas sin previa calificación |
| `notes_internal` | text | Contexto de la relación con el propietario. Uso exclusivo del equipo |

**Casos especiales:** 3 fideicomisos (F-1998, F-2008, F-2019), 5 personas morales. 4 propietarios con `allow_public_photos = no`. 5 con confidencialidad `muy alta`. Comunicación vía apoderado obligatoria en 5 casos.

---

### `leads.csv`
**Llave primaria:** `lead_id`
**Llaves foráneas:** `assigned_agent_id → agents.agent_id`

| Columna | Tipo | Descripción |
|---|---|---|
| `lead_id` | string PK | Identificador del prospecto (L001–L040) |
| `full_name` | string | Nombre completo del prospecto |
| `email` | string | Correo electrónico |
| `phone` | string | Teléfono con lada internacional |
| `lead_source` | enum | `instagram`, `referido agente`, `referido cliente`, `portal inmobiliario`, `sitio web meridiana`, `feria inmobiliaria` |
| `lead_status` | enum | `nuevo`, `en contacto`, `calificado`, `descartado` |
| `budget_min_mxn` | integer | Presupuesto mínimo en pesos (o renta mínima mensual) |
| `budget_max_mxn` | integer | Presupuesto máximo |
| `financing_type` | enum | `contado`, `crédito bancario`, `crédito institucional`, `renta mensual`, `por definir` |
| `desired_municipality` | string | Municipio o municipios de interés |
| `desired_neighborhoods` | string | Colonias de interés separadas por · |
| `property_type_interest` | string | Tipos de propiedad de interés |
| `bedrooms_min` | integer | Mínimo de recámaras requerido |
| `purchase_timeline` | string | `inmediato`, `0-3 meses`, `3-6 meses`, `6-12 meses`, `más de 12 meses`, `por definir` |
| `investment_profile` | string | Intención: uso propio, inversión, renta vacacional, retiro, corporativo, etc. |
| `assigned_agent_id` | string FK | Agente asignado al prospecto |
| `qualification_score` | integer | Score de calificación de 0 a 100 |
| `notes_public` | text | Resumen de preferencias para el expediente compartido con el equipo |
| `notes_internal` | text | Contexto sensible para el agente asignado: urgencia real, dinámica familiar, alertas |

**Distribución:** 20 calificados · 13 en contacto · 6 nuevos · 1 descartado. 9 leads internacionales (Francia, Alemania, Suecia, Holanda, EE.UU.). Score promedio 70.3, mínimo 22, máximo 94.

---

### `interactions.csv`
**Llave primaria:** `interaction_id`
**Llaves foráneas:** `lead_id → leads.lead_id`, `agent_id → agents.agent_id`, `property_id → properties.property_id` (nullable)

| Columna | Tipo | Descripción |
|---|---|---|
| `interaction_id` | string PK | Identificador de la interacción (I001–I065) |
| `lead_id` | string FK | Prospecto involucrado |
| `agent_id` | string FK | Agente que registra o gestiona |
| `property_id` | string FK nullable | Propiedad discutida (vacío en contactos iniciales) |
| `channel` | enum | `instagram`, `whatsapp`, `llamada`, `email`, `visita presencial`, `videollamada`, `referido`, `portal inmobiliario`, `sitio web meridiana`, `feria inmobiliaria` |
| `direction` | enum | `entrante`, `saliente` |
| `interaction_datetime` | datetime | Fecha y hora ISO 8601 |
| `summary` | text | Resumen narrativo de la interacción. Campo principal para RAG |
| `sentiment` | enum | `muy positivo`, `positivo`, `neutral`, `negativo` |
| `intent` | enum | `exploración`, `calificación`, `intención de compra`, `intención de renta`, `negociación`, `due diligence`, `reflexión`, `decisión`, `urgente`, `exploración legal`, `agenda visita` |
| `next_action` | text | Acción concreta a realizar después de esta interacción |
| `next_action_due` | date | Fecha límite para la siguiente acción |
| `visibility` | enum | `equipo` (visible para todos), `privado` (solo AGT-01 y director) |

**Notas de diseño:** 65 interacciones cubren 27 leads. 9 interacciones marcadas como `privado` corresponden a los tres casos más sensibles: divorcio activo, director regional corporativo y lead de mayor valor con tour ejecutivo. El campo `summary` es el insumo principal para sistemas RAG porque contiene lenguaje natural denso sobre actitud del cliente, detalles de visita y señales de compra.

---

### `viewings.csv`
**Llave primaria:** `viewing_id`
**Llaves foráneas:** `property_id → properties.property_id`, `lead_id → leads.lead_id`, `agent_id → agents.agent_id`

| Columna | Tipo | Descripción |
|---|---|---|
| `viewing_id` | string PK | Identificador de la visita (V001–V035) |
| `property_id` | string FK | Propiedad visitada |
| `lead_id` | string FK | Prospecto que visitó |
| `agent_id` | string FK | Agente que coordinó la visita |
| `scheduled_at` | datetime | Fecha y hora programada o realizada |
| `visit_type` | enum | `presencial`, `videollamada` |
| `status` | enum | `realizada`, `programada`, `cancelada` |
| `feedback_summary` | text | Descripción narrativa de lo que ocurrió en la visita |
| `interest_level` | enum | `muy alto`, `alto`, `medio`, `bajo`, `pendiente`, `sin calificación` |
| `objections` | text | Objeciones o dudas planteadas por el prospecto durante la visita |
| `follow_up_required` | enum | `sí`, `no` |

**Distribución:** 20 realizadas · 10 programadas · 5 canceladas. P037 es la propiedad con más visitas (4). L039 es el lead con más visitas acumuladas (4). 31 de 35 visitas requieren follow-up. Las 5 canceladas tienen razón documentada.

---

### `offers.csv`
**Llave primaria:** `offer_id`
**Llaves foráneas:** `property_id → properties.property_id`, `lead_id → leads.lead_id`, `agent_id → agents.agent_id`

| Columna | Tipo | Descripción |
|---|---|---|
| `offer_id` | string PK | Identificador de la oferta (O001–O020) |
| `property_id` | string FK | Propiedad sobre la que se hace la oferta |
| `lead_id` | string FK | Prospecto que hace la oferta |
| `agent_id` | string FK | Agente que gestiona la negociación |
| `offer_amount_mxn` | integer | Monto ofertado en pesos (0 para cartas de intención de renta) |
| `offer_date` | date | Fecha de la oferta |
| `offer_status` | enum | `en negociación`, `contraoferta activa`, `aceptada`, `rechazada`, `en revisión legal`, `carta de intención firmada`, `pendiente visita`, `retirada por lead` |
| `counteroffer_amount_mxn` | integer | Monto de la contraoferta del vendedor (0 si no hay) |
| `closing_window_days` | integer | Días pactados para cierre (0 si rechazada o retirada) |
| `financing_type` | enum | `contado`, `crédito bancario`, `renta mensual` |
| `deposit_pct` | integer | Porcentaje de enganche acordado |
| `notes_internal` | text | Contexto de la negociación: posición real de cada parte, alertas, instrucciones al agente |

**Análisis de gaps:** descuento promedio negociado es del 7% sobre precio de lista. El gap más pequeño es 400K (2.8%) en P031. El más grande es 2.5M (7.8%) en P003, oferta que fue rechazada. Cinco propiedades tienen ofertas múltiples simultáneas (P007 con dos compradores compitiendo sin saberlo es el caso más delicado).

---

### `property_features.csv`
**Llave primaria compuesta:** `property_id + feature_name`
**Llave foránea:** `property_id → properties.property_id`

| Columna | Tipo | Descripción |
|---|---|---|
| `property_id` | string FK | Propiedad a la que pertenece la característica |
| `feature_name` | string | Nombre corto de la característica (ej. `cenote privado`, `cocina Gaggenau`) |
| `feature_category` | string | Categoría semántica de la feature (28 categorías distintas) |
| `feature_value` | text | Descripción detallada de la característica para retrieval |
| `is_public` | enum | `sí` — aparece en portales · `no` — uso interno únicamente |

**Cobertura:** 149 features para 38 propiedades (38/38). Promedio de 3.9 features por propiedad. Las ultra tienen entre 6 y 7 features cada una. Las de entrada tienen entre 2 y 4.

**Features privadas (9):** cuartos de pánico (P003, P019), cuartos de servicio en cantidad (P003, P019), fachada restringida por INAH (P004), biodigestor (P011, P033), licencia de hospedaje (P013), contrato corporativo activo (P035) y expediente cerrado de propiedad vendida (P014).

**Categorías principales:** amenidad exterior · distribución · exterior · cocina · amenidad edificio · interior premium · seguridad · infraestructura · arquitectura histórica · sustentabilidad · tecnología · habilitación legal.

---

## Diagrama de relaciones

```
agents ──────────────────────────────────┐
  │ agent_id                             │ manager_id (self-ref)
  │                                      │
  ├──→ properties.agent_id               │
  ├──→ leads.assigned_agent_id           │
  ├──→ interactions.agent_id             │
  ├──→ viewings.agent_id                 │
  └──→ offers.agent_id                   │
                                         │
owners                                   │
  └──→ properties.owner_id              ─┘

properties ──────────────────────────────┐
  │ property_id                          │
  │                                      │
  ├──→ interactions.property_id          │
  ├──→ viewings.property_id              │
  ├──→ offers.property_id                │
  └──→ property_features.property_id    ─┘

leads
  │ lead_id
  │
  ├──→ interactions.lead_id
  ├──→ viewings.lead_id
  └──→ offers.lead_id
```

---

## Campos para RAG — guía de uso

Los siguientes campos contienen lenguaje natural denso y son los más útiles para embedding y retrieval semántico:

| Dataset | Campo | Contenido semántico |
|---|---|---|
| `properties` | `public_description` | Descripción comercial de la propiedad |
| `properties` | `internal_summary` | Contexto privado del agente sobre el propietario y la operación |
| `owners` | `notes_internal` | Dinámica de la relación con el propietario |
| `leads` | `notes_public` | Preferencias declaradas del prospecto |
| `leads` | `notes_internal` | Señales reales de urgencia motivación y dinámica de decisión |
| `interactions` | `summary` | Narrativa de cada contacto: lo más rico semánticamente |
| `viewings` | `feedback_summary` | Reacción del prospecto durante la visita |
| `viewings` | `objections` | Objeciones específicas del prospecto |
| `offers` | `notes_internal` | Posición real de cada parte en la negociación |
| `property_features` | `feature_value` | Descripción detallada de cada característica |

---

## Control de acceso por visibilidad

Varios campos y registros están marcados con restricción de visibilidad. Un sistema que implemente control de roles debe respetar lo siguiente:

- `interactions.visibility = privado` → solo AGT-01 (director) y el agente asignado al lead
- `owners.confidentiality_level = muy alta` → solo el agente responsable y dirección
- `owners.allow_public_photos = no` → bloquear en cualquier pipeline de publicación automática
- `property_features.is_public = no` → no incluir en fichas de portales ni materiales públicos
- `properties.internal_summary` → nunca exponer en respuestas públicas o a usuarios sin autenticación
- `offers.notes_internal` → solo para el agente asignado y dirección

---

## Notas sobre los datos

Todos los registros son sintéticos. Los nombres de personas son combinaciones verosímiles de apellidos yucatecos (Peón, Cámara, Barbachano, Manzanilla, Dzul, Pech, Canul, Bolio, Rejón, Ancona) sin apuntar a personas públicas identificables. Los precios reflejan rangos reales del mercado premium de Mérida en 2024. Las coordenadas geográficas son aproximaciones plausibles dentro de las colonias mencionadas y no corresponden a direcciones reales.

Los campos `notes_internal` contienen situaciones delicadas que aparecerían en un CRM real: divorcios en proceso, fideicomisos con herederos en conflicto, compradores con intención de pago en criptomonedas, propietarios con apego emocional, y errores de coordinación interna. Están ahí para que el sistema que consuma estos datos pueda ser probado en escenarios complejos y no solo en casos simples.
