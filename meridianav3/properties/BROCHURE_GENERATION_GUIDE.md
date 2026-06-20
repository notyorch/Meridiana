# Guía de Generación de Brochures (Instrucciones para IA)

Este documento define el proceso estandarizado para generar brochures comerciales de propiedades para Meridiana. Utilice estas instrucciones para mantener la consistencia visual y de datos en todo el catálogo.

## 1. Fuentes de Datos
- **Propiedades:** `meridianav1/datasets/raw/properties.csv`
- **Características:** `meridianav1/datasets/raw/property_features.csv`
- **Agentes:** `meridianav1/datasets/raw/agents.csv`
- **Template:** `meridianav1/templates/public/property-brochure.html`

## 2. Requisitos Previos
Cada propiedad debe tener su carpeta correspondiente en `meridianav1/properties/Pxxx/` y el archivo de imagen `render1.png` ya debe estar presente en dicha carpeta antes de la generación del HTML.

## 3. Reglas de Mapeo de Datos

### Portada (Página 1)
- **Título Principal:** Utilizar el campo `commercial_name`.
- **Subtítulo (Tagline):** Utilizar el campo `title`.
- **Badges:** Mostrar `listing_code`, `property_type` + `listing_type`, y `neighborhood` + `municipality`.
- **Precio:** Formatear como `$XX,XXX,XXX` (MXN).

### Ficha Técnica (Página 2)
- **Encabezado:** Repetir `commercial_name` y `listing_code`.
- **Estadísticas:** Mapear `bedrooms`, `bathrooms`, `construction_m2`, `lot_m2` y `parking_spaces`.
- **Descripción:**
  - Iniciar con el campo `title` en **negritas** (`<strong>`).
  - Seguir con dos saltos de línea (`<br /><br />`).
  - Incluir el campo `public_description` completo.
- **Características:** 
  - Consultar `property_features.csv`.
  - **FILTRO CRÍTICO:** Solo incluir aquellas donde `is_public` sea `sí`.
  - Formatear como una lista `<ul>` de elementos `<li>`.

### Información del Agente
- Localizar al agente en `agents.csv` usando el `agent_id` de la propiedad.
- **Campos:** `full_name`, `phone`, `email`.
- **Avatar:** Utilizar la inicial del primer nombre.

## 4. Estilo Visual y Formato
- **Relación de Aspecto:** 16:9 (Responsivo).
- **Acabado Premium:** El template incluye un gradiente lineal sobre la foto de portada (transparente a oscuro) para mejorar la legibilidad del texto blanco. No modificar estas clases de CSS.
- **Naming:** El archivo de salida debe llamarse siempre `property-brochure.html`.

## 5. Documentación de Control
Para cada brochure generado, crear un archivo `Pxxx.md` en la misma carpeta que documente:
1. El mapeo de campos realizado.
2. Cualquier dato que haya sido hardcodeado (ej. "Meridiana" como nombre de marca).
3. Fecha de generación.
