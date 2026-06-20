# Taxonomía documental y de datos

## Propósito

Este archivo define las entidades principales del sistema Meridiana y su función dentro del sistema documental. Sirve como base para organizar documentos, reutilizar datos del CRM y mantener consistencia entre inventario, leads, propietarios y operación comercial. La taxonomía parte de la estructura del proyecto, del README del dataset y del tono de marca boutique de Meridiana. [file:2][file:3][file:1]

## Entidades principales

### 1. Propiedades

Representan el inventario comercial de Meridiana: casas, departamentos, townhouses, villas y terrenos. Esta entidad concentra la información más visible hacia clientes y prospectos, como ubicación, precio, metraje, tipo de propiedad y descripción comercial. A partir de esta entidad se producirán fichas, brochures, listings web y resúmenes comerciales. [file:3]

### 2. Agentes

Representan al equipo comercial y operativo de Meridiana. Incluyen perfiles, roles, especialidad geográfica, idioma, senioridad y jerarquía interna. Esta entidad alimentará documentos como perfiles de agente, directorios internos, asignaciones comerciales y materiales de presentación del equipo. [file:3]

### 3. Propietarios

Representan a las personas físicas, personas morales o fideicomisos dueños de los inmuebles. Esta entidad ayuda a entender quién autoriza la comercialización, cuáles son las condiciones de relación y qué nivel de comunicación se maneja. De aquí saldrán perfiles internos de propietario, notas de relación y documentos de seguimiento comercial. [file:3]

### 4. Leads

Representan prospectos, compradores o interesados en renta. Esta entidad captura origen del lead, presupuesto, zona de interés, tipo de propiedad buscada, horizonte de compra y nivel de calificación. Alimentará documentos como memorias de calificación, resúmenes de prospecto y seguimientos de atención comercial. [file:3]

### 5. Interacciones

Representan el historial de contacto entre agentes y leads, por ejemplo mensajes, llamadas, visitas, correos o videollamadas. Esta entidad es clave para reconstruir contexto comercial y continuidad de atención. Se usará para cronologías, bitácoras de contacto y resúmenes narrativos del proceso comercial. [file:3]

### 6. Visitas

Representan recorridos presenciales o virtuales a propiedades. Incluyen fecha, tipo de visita, nivel de interés, objeciones y necesidad de seguimiento. Esta entidad producirá resúmenes de visita, reportes de retroalimentación y notas de seguimiento después del recorrido. [file:3]

### 7. Ofertas

Representan propuestas formales o informales de compra o renta sobre una propiedad. Incluyen monto ofrecido, estatus de negociación, contraoferta, ventana de cierre y notas de negociación. Esta entidad servirá para memos de negociación, historiales de oferta y documentos de cierre comercial. [file:3]

### 8. Características de propiedad

Representan atributos desagregados de cada inmueble, como amenidades, seguridad, arquitectura, sustentabilidad, tecnología o elementos legales. Esta entidad complementa la descripción principal de la propiedad y ayuda a generar textos más precisos y comparables. Se usará para enriquecer fichas, listings, brochures y comparativos de inventario. [file:3]

## Relaciones entre entidades

Las propiedades están asignadas a un agente y vinculadas a un propietario. Los leads se asignan a agentes y se relacionan con interacciones, visitas y ofertas. Las interacciones conectan leads, agentes y, cuando aplica, una propiedad específica. Las visitas y ofertas conectan los tres núcleos del negocio: propiedad, interesado y asesor. Las características de propiedad dependen siempre de una propiedad concreta. [file:3]

## Tipos de documentos que producirá cada entidad

| Entidad | Documentos que generará |
|---|---|
| Propiedades | Ficha de propiedad, brochure, listing web, resumen comercial, comparativo interno. |
| Agentes | Perfil de agente, directorio del equipo, ficha de especialidad, presentación institucional. |
| Propietarios | Perfil de propietario, nota de relación, resumen de autorización, expediente interno. |
| Leads | Memo de calificación, perfil de prospecto, resumen de necesidades, plan de seguimiento. |
| Interacciones | Bitácora de contacto, cronología comercial, resumen narrativo de conversación. |
| Visitas | Resumen de visita, reporte de observaciones, seguimiento posterior, feedback comercial. |
| Ofertas | Memo de negociación, historial de oferta, contraoferta, estado de cierre. |
| Características de propiedad | Inventario de atributos, enriquecimiento de ficha, texto de amenities, comparativo técnico. |

## Criterio general de organización

La taxonomía de Meridiana debe partir de estas ocho entidades porque cubren el ciclo completo de operación inmobiliaria: inventario, equipo, propietarios, prospectos, contacto, visitas, ofertas y atributos. Con esta base, los documentos se pueden organizar de manera coherente para uso comercial, operativo e institucional sin perder consistencia entre el CRM y la documentación publicada. [file:3][file:2]
