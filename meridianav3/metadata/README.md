Actúa como diseñador de documentos editoriales y arquitecto de plantillas para una inmobiliaria boutique ficticia llamada Meridiana.

Vas a trabajar SOLO con estos archivos como contexto:
1. metadata/ del proyecto Meridiana
2. Meridiana — Brand Board / brand guidelines

NO uses información externa.
NO inventes una identidad de marca distinta.
NO agregues funciones enterprise innecesarias.
NO diseñes permisos, control de acceso avanzado ni capas de seguridad complejas.
Tu objetivo es producir templates reutilizables en formato .docx, claros, elegantes, sobrios y fáciles de llenar por un equipo pequeño.

## Contexto de marca que debes respetar
- Meridiana es una inmobiliaria boutique en Mérida, Yucatán.
- La marca es sobria, precisa, tipográfica, sin ornamentos.
- La identidad visual usa una paleta contenida: negro carbón, blanco crema, bronce apagado y gris piedra.
- El tono no usa superlativos vacíos ni lenguaje genérico de lujo.
- La redacción debe ser breve, precisa, segura y editorial.
- La marca transmite discreción, pertenencia, conocimiento y alto criterio.
- El estilo debe sentirse premium mexicano contemporáneo, no ostentoso.

## Contexto documental que debes respetar
Antes de diseñar, interpreta la taxonomía y el sistema documental de metadata:
- taxonomy.md
- naming-convention.md
- frontmatter-spec.md
- document-types.md
- source-map.md
- status-values.md
- sensitivity-levels.md si existe
- access-model.md si existe

Usa esa estructura para definir templates consistentes, pero no te obsesiones con seguridad avanzada.
Tu tarea es crear plantillas funcionales, no un sistema de compliance.

## Instrucción general de diseño
Cada plantilla debe:
- Ser usable por un agente o coordinador sin demasiada edición.
- Tener encabezados claros y orden lógico.
- Usar placeholders consistentes y evidentes.
- Permitir que después un script, agente CLI o editor humano la complete rápido.
- Tener una estructura premium, limpia y sobria.
- Evitar exceso de texto decorativo.
- Evitar bloques demasiado largos si una sección puede resolverse con una línea precisa.
- Mantener consistencia entre plantillas.

## Formato de salida esperado
Para cada template, genera:
1. nombre del archivo sugerido
2. objetivo del documento
3. audiencia
4. tono
5. estructura completa
6. secciones obligatorias
7. placeholders necesarios
8. sugerencia visual o de layout si aplica
9. lista breve de cosas que NO debe hacer el documento

Después, genera el contenido completo de la plantilla como si fuera un archivo .docx listo para diseñarse, con:
- portada o encabezado si aplica,
- bloques de título,
- secciones internas,
- placeholders marcados de forma consistente,
- notas mínimas solo cuando sean necesarias para edición.

## Reglas de placeholders
Usa placeholders consistentes y fáciles de reemplazar, por ejemplo:
- {{property_title}}
- {{listing_code}}
- {{agent_name}}
- {{lead_name}}
- {{owner_name}}
- {{property_type}}
- {{location}}
- {{price_mxn}}
- {{construction_m2}}
- {{lot_m2}}
- {{bedrooms}}
- {{bathrooms}}
- {{parking_spaces}}
- {{public_description}}
- {{internal_summary}}
- {{feature_list}}
- {{contact_name}}
- {{contact_phone}}
- {{contact_email}}
- {{date}}
- {{version}}

Si un placeholder depende de campos del dataset, intenta respetar los nombres conceptuales del README.
Si necesitas placeholders derivados, sepáralos claramente y no los mezcles con los campos crudos.

## Templates que debes producir

Debes generar estos templates, en este orden:

1. company profile
2. buyer FAQ
3. seller FAQ
4. property brochure
5. property listing longform
6. agent profile
7. lead qualification memo
8. viewing summary
9. negotiation notes
10. owner profile
11. luxury service playbook
12. reusable disclaimer blocks

---

# TEMPLATE 1 — COMPANY PROFILE

## Objetivo
Presentar Meridiana como firma boutique de real estate premium en Mérida. Debe funcionar como presentación institucional breve, elegante y seria.

## Audiencia
Clientes potenciales, propietarios, prospectos de alto perfil y aliados comerciales.

## Tono
Sobrio, seguro, editorial, discreto. Nada de promesas grandilocuentes.

## Estructura obligatoria
- Portada o encabezado con nombre de marca.
- Una frase editorial de posicionamiento.
- Quiénes somos.
- Qué hacemos.
- Dónde operamos.
- Cómo trabajamos.
- Equipo / especialidades.
- Cierre de contacto.

## Placeholders necesarios
- {{brand_name}}
- {{tagline}}
- {{city}}
- {{service_area}}
- {{team_summary}}
- {{contact_email}}
- {{contact_phone}}
- {{website}}

## Layout
- Mucho aire.
- Uso de jerarquía tipográfica clara.
- Una sola portada o cabecera sobria.
- Secciones cortas, con lectura rápida.

## No debe hacer
- No usar lenguaje promocional exagerado.
- No listar demasiados datos operativos.
- No sonar como brochure de lujo genérico.

---

# TEMPLATE 2 — BUYER FAQ

## Objetivo
Responder dudas frecuentes de compradores antes o durante el contacto con la firma.

## Audiencia
Prospectos y compradores potenciales.

## Tono
Claro, útil, preciso, amable pero serio.

## Estructura obligatoria
- Introducción breve.
- Preguntas y respuestas.
- Cómo inicia el proceso.
- Qué información conviene preparar.
- Cierre con canal de contacto.

## Placeholders necesarios
- {{brand_name}}
- {{contact_email}}
- {{contact_phone}}
- {{service_area}}
- {{process_steps}}
- {{faq_items}}

## Layout
- Formato pregunta-respuesta.
- Preguntas en estilo destacado.
- Respuestas de 2 a 5 líneas máximo.

## No debe hacer
- No sonar a marketing.
- No responder con tecnicismos innecesarios.
- No repetir lo mismo en varias respuestas.

---

# TEMPLATE 3 — SELLER FAQ

## Objetivo
Explicar a propietarios cómo funciona la venta con Meridiana.

## Audiencia
Propietarios, titulares y representantes.

## Tono
Profesional, discreto, confiable, directo.

## Estructura obligatoria
- Introducción corta.
- Preguntas sobre valuación, publicación, visitas, filtros de compradores, negociación y cierre.
- Cómo se trabaja la comunicación.
- Cierre con siguiente paso sugerido.

## Placeholders necesarios
- {{brand_name}}
- {{contact_email}}
- {{contact_phone}}
- {{seller_process}}
- {{faq_items}}

## Layout
- Igual que Buyer FAQ, pero adaptado a propietarios.
- Muy legible.
- Preguntas agrupadas por tema si hace falta.

## No debe hacer
- No prometer resultados.
- No usar lenguaje agresivo de captación.
- No exponer procedimientos demasiado internos.

---

# TEMPLATE 4 — PROPERTY BROCHURE

## Objetivo
Presentar una propiedad de forma breve, visual y comercial.

## Audiencia
Compradores potenciales, clientes y aliados comerciales.

## Tono
Preciso, elegante, minimalista y descriptivo.

## Estructura obligatoria
- Portada.
- Título de la propiedad.
- Resumen de una frase.
- Datos clave.
- Descripción principal.
- Características destacadas.
- Ubicación general.
- Llamado a agendar visita.
- Contacto del agente.

## Placeholders necesarios
- {{property_title}}
- {{listing_code}}
- {{property_type}}
- {{location}}
- {{price_mxn}}
- {{construction_m2}}
- {{lot_m2}}
- {{bedrooms}}
- {{bathrooms}}
- {{parking_spaces}}
- {{public_description}}
- {{feature_list}}
- {{agent_name}}
- {{agent_phone}}
- {{agent_email}}

## Layout
- Muy visual.
- Poca densidad por página.
- Bloques bien separados.
- Ideal para una o dos páginas.

## No debe hacer
- No saturar con texto largo.
- No incluir datos internos.
- No verse como folleto comercial ruidoso.

---

# TEMPLATE 5 — PROPERTY LISTING LONGFORM

## Objetivo
Crear una ficha larga para web o portal inmobiliario con lectura elegante y clara.

## Audiencia
Compradores digitales, prospectos que comparan opciones, captación web.

## Tono
Preciso, sobrio, fluido, comercial sin exageración.

## Estructura obligatoria
- Título principal.
- Resumen ejecutivo.
- Datos clave.
- Descripción por zonas o espacios.
- Features y amenidades.
- Entorno / ubicación.
- Perfil ideal del comprador.
- Contacto y siguiente paso.

## Placeholders necesarios
- {{property_title}}
- {{listing_code}}
- {{property_type}}
- {{listing_type}}
- {{status}}
- {{price_mxn}}
- {{maintenance_fee_mxn}}
- {{construction_m2}}
- {{lot_m2}}
- {{bedrooms}}
- {{bathrooms}}
- {{parking_spaces}}
- {{year_built}}
- {{furnished}}
- {{pet_friendly}}
- {{public_description}}
- {{feature_list}}
- {{location_summary}}
- {{agent_name}}
- {{agent_phone}}
- {{agent_email}}

## Layout
- Jerarquía limpia.
- Subtítulos muy claros.
- Compatible con web y exportación a PDF.

## No debe hacer
- No sonar repetitivo.
- No usar adjetivos vacíos.
- No incluir notas internas ni datos sensibles.

---

# TEMPLATE 6 — AGENT PROFILE

## Objetivo
Presentar al asesor inmobiliario de manera profesional y confiable.

## Audiencia
Clientes, leads, propietarios y equipo interno.

## Tono
Cálido pero serio, competente, discreto.

## Estructura obligatoria
- Nombre y cargo.
- Perfil breve.
- Zonas de especialidad.
- Tipo de propiedades.
- Idiomas.
- Forma de trabajo.
- Datos de contacto.

## Placeholders necesarios
- {{agent_name}}
- {{agent_role}}
- {{specialty_zone}}
- {{specialty_property_type}}
- {{languages}}
- {{agent_summary}}
- {{agent_phone}}
- {{agent_email}}

## Layout
- Retrato opcional.
- Mucho aire.
- Énfasis en claridad y legibilidad.

## No debe hacer
- No sonar a currículum largo.
- No exagerar logros.
- No incluir datos demasiado técnicos.

---

# TEMPLATE 7 — LEAD QUALIFICATION MEMO

## Objetivo
Documentar el perfil comercial de un lead y su nivel de avance.

## Audiencia
Equipo comercial interno.

## Tono
Claro, operativo, ordenado.

## Estructura obligatoria
- Identificación del lead.
- Origen.
- Presupuesto.
- Zonas de interés.
- Tipo de propiedad.
- Timeline.
- Perfil de compra o renta.
- Señales de intención.
- Próximo paso.

## Placeholders necesarios
- {{lead_name}}
- {{lead_source}}
- {{budget_min_mxn}}
- {{budget_max_mxn}}
- {{desired_municipality}}
- {{desired_neighborhoods}}
- {{property_type_interest}}
- {{bedrooms_min}}
- {{purchase_timeline}}
- {{investment_profile}}
- {{qualification_score}}
- {{notes_public}}
- {{notes_internal}}
- {{assigned_agent_name}}

## Layout
- Formato memo.
- Campos fijos + sección narrativa corta.
- Fácil de llenar en una llamada o después de una visita.

## No debe hacer
- No ser demasiado largo.
- No mezclar observaciones con conclusiones sin separarlas.
- No sonar como ficha pública.

---

# TEMPLATE 8 — VIEWING SUMMARY

## Objetivo
Registrar lo que ocurrió durante una visita a una propiedad.

## Audiencia
Equipo comercial interno.

## Tono
Preciso, neutral, útil para seguimiento.

## Estructura obligatoria
- Datos de la visita.
- Propiedad visitada.
- Asistentes.
- Resumen de la visita.
- Nivel de interés.
- Objeciones.
- Próximo paso.
- Fecha de seguimiento.

## Placeholders necesarios
- {{viewing_id}}
- {{property_title}}
- {{property_code}}
- {{lead_name}}
- {{agent_name}}
- {{scheduled_at}}
- {{visit_type}}
- {{status}}
- {{feedback_summary}}
- {{interest_level}}
- {{objections}}
- {{follow_up_required}}
- {{next_follow_up_date}}

## Layout
- Tipo reporte breve.
- Secciones muy claras.
- Ideal para captura rápida post-visita.

## No debe hacer
- No usar narrativa excesiva.
- No ocultar objeciones.
- No mezclar visita con negociación.

---

# TEMPLATE 9 — NEGOTIATION NOTES

## Objetivo
Registrar el estado de una negociación y las posiciones de las partes.

## Audiencia
Equipo comercial y dirección.

## Tono
Preciso, reservado, estructurado.

## Estructura obligatoria
- Identificación de la propiedad.
- Identificación del lead.
- Monto ofertado.
- Contraoferta.
- Estado.
- Ventana de cierre.
- Condiciones clave.
- Riesgos o alertas.
- Siguiente acción.

## Placeholders necesarios
- {{offer_id}}
- {{property_title}}
- {{property_code}}
- {{lead_name}}
- {{agent_name}}
- {{offer_amount_mxn}}
- {{offer_date}}
- {{offer_status}}
- {{counteroffer_amount_mxn}}
- {{closing_window_days}}
- {{financing_type}}
- {{deposit_pct}}
- {{notes_internal}}

## Layout
- Memo formal.
- Secciones cortas.
- Debe verse serio y fácil de revisar.

## No debe hacer
- No dramatizar la negociación.
- No incluir texto legal complejo.
- No ser público.

---

# TEMPLATE 10 — OWNER PROFILE

## Objetivo
Consolidar información útil sobre el propietario y la relación con el inmueble.

## Audiencia
Equipo interno, dirección y asesor asignado.

## Tono
Discreto, profesional, claro.

## Estructura obligatoria
- Datos del propietario.
- Tipo de titularidad.
- Canal preferido.
- Relación con la propiedad.
- Condiciones de comunicación.
- Historial resumido.
- Notas internas.
- Relación con propiedades activas.

## Placeholders necesarios
- {{owner_name}}
- {{owner_type}}
- {{contact_email}}
- {{contact_phone}}
- {{preferred_contact_channel}}
- {{residency_country}}
- {{legal_representative}}
- {{confidentiality_level}}
- {{allow_public_photos}}
- {{allow_open_house}}
- {{notes_internal}}
- {{property_list}}

## Layout
- Formato expediente.
- Orden jerárquico claro.
- Adecuado para consulta interna rápida.

## No debe hacer
- No ser demasiado narrativo.
- No parecer contrato.
- No incluir lenguaje comercial.

---

# TEMPLATE 11 — LUXURY SERVICE PLAYBOOK

## Objetivo
Unificar el estándar de atención premium de Meridiana.

## Audiencia
Equipo comercial, soporte y operaciones.

## Tono
Preciso, elegante, práctico.

## Estructura obligatoria
- Principios de servicio.
- Cómo saludar y abrir conversación.
- Cómo calificar sin presionar.
- Cómo coordinar visitas.
- Cómo dar seguimiento.
- Cómo cerrar la comunicación.
- Qué evitar.
- Ejemplos de trato correcto.

## Placeholders necesarios
- {{brand_name}}
- {{service_principles}}
- {{communication_rules}}
- {{visit_rules}}
- {{follow_up_rules}}
- {{dont_do_list}}

## Layout
- Manual breve.
- Secciones numeradas.
- Frases cortas y claras.
- Puede incluir callouts tipo “sí / no”.

## No debe hacer
- No sonar corporativo rígido.
- No parecer manual de call center.
- No usar jerga excesiva.

---

# TEMPLATE 12 — REUSABLE DISCLAIMER BLOCKS

## Objetivo
Crear bloques reutilizables para pie de documento, portada o sección legal ligera.

## Audiencia
Clientes y uso interno cuando aplique.

## Tono
Breve, sobrio, claro.

## Estructura obligatoria
- Disclaimer de información comercial.
- Disclaimer de disponibilidad.
- Disclaimer de medidas y precios.
- Disclaimer de imágenes y mobiliario.
- Disclaimer de cita previa.
- Cierre de contacto.

## Placeholders necesarios
- {{brand_name}}
- {{contact_email}}
- {{contact_phone}}
- {{date}}

## Layout
- Bloques muy breves.
- Puede usarse al final de brochures y listings.
- Tipografía más pequeña, discreta.

## No debe hacer
- No ser intimidante.
- No ser un texto legal largo.
- No saturar el documento principal.

## Instrucción final para los templates
Diseña todos los documentos para que compartan una misma lógica visual:
- portada o encabezado consistente,
- jerarquía tipográfica limpia,
- mucho aire,
- secciones cortas,
- estilo premium y sobrio,
- referencias claras a Meridiana,
- y facilidad de llenado posterior.

Evita adornos innecesarios, lenguaje vacío y maquetación genérica de IA.

Antes de generar, revisa que cada template esté alineado con:
- taxonomy.md
- naming-convention.md
- frontmatter-spec.md
- document-types.md
- source-map.md
- status-values.md
- y el brand board de Meridiana.