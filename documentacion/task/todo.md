# Plan: Configurar Formateador de LaTeX

Este es el plan para solucionar el error "Please set your LaTeX formatter in `latex-workshop.formatting.latex`".

## Tareas

- [x] **1. Crear configuración de VS Code para el proyecto**
  - Crear la carpeta `.vscode` en la raíz del proyecto.
  - Crear el archivo `.vscode/settings.json`.
  - Agregar la configuración `"latex-workshop.formatting.latex": "latexindent"` (o el formateador preferido por defecto como `latexindent`) al archivo `settings.json`.

## Revisión
**Resumen de los cambios realizados:**
- Se añadió la configuración `"latex-workshop.formatting.latex": "latexindent"` para resolver el error del formateador de LaTeX y permitir el formateo del código usando `latexindent`.

- [x] **2. Ampliar columna 3 del encabezado conservando una sola línea en columna 5**
  - Se modificó `config/header.tex` para reubicar los anchos de las columnas de forma simétrica.
  - El grupo izquierdo (columnas 1 y 2) suma 4.5 cm (2.25 cm cada una).
  - El grupo derecho (columnas 4 y 5) suma 4.5 cm (1.6 cm y 2.9 cm respectivamente).
  - De esta forma el espacio central (columna 3) queda perfectamente simétrico y más amplio, mientras la columna 5 (`2.9cm`) tiene espacio suficiente para que su texto no ocupe más de una línea (evitando que crezca el alto de las filas).
  - Se ajustó el tamaño de los logos a `2.0cm` de ancho para el nuevo espacio disponible.

- [x] **3. Corregir Código de Proyecto en el Encabezado**
  - Se añadió la variable `\projectcode{P2807}` en `config/datos_proyecto.tex`.
  - Se actualizó también el `\documentcode` para utilizar `P2807-PR-MC-001`.
  - Se modificó la fila 6, columna 2 de `config/header.tex` cambiándolo de `\targetcompany` (que contenía "rio") a `\projectcode` (para mostrar "P2807" como exige el formato).

## Revisión
**Resumen de los cambios realizados:**
- Se creó la carpeta `.vscode` con el archivo `settings.json` para definir la configuración de formato de LaTeX.
- Se editó `config/header.tex` ajustando el entorno `tabularx` considerando el problema de salto de línea en la columna 5:
  - Columnas 1 y 2 de imagen: `p{2.25cm}` (imágenes ajustadas a `2.0cm`).
  - Columna 4 de etiquetas: `p{1.6cm}`.
  - Columna 5 de valores (fechas, nombres): `p{2.9cm}` (suficiente para que no haya salto de línea).
  - La columna 3 (`X`) fue ampliada en total y permanece simétricamente centrada dado que la suma de los anchos fijos a su izquierda (4.5 cm) es exactamente igual a la suma de los anchos a su derecha (4.5 cm).
- Se solucionó la desubicación del código de proyecto (P2807) en el reporte, creando una variable dedicada `\projectcode` y asignándola a la posición correcta (fila 6, columna 2) sin alterar el valor de la empresa destino ("rio").

## Tareas Nuevas: Renombrar Archivo y Depuración
- [x] **4. Renombrar archivo LaTeX principal**
  - Cambiar el nombre físico del archivo `P2608-PR-MC-001 REV0.tex` a `P2608-PR-MC-001.tex`.

- [x] **5. Reubicar Dependencias Usadas**
  - Mover los logos desde `formatolatex/logos/` hacia `assets/logos/`.
  - Actualizar el archivo `config/header.tex` para leer los logos desde `assets/logos/`.
  - Verificar que el documento principal compile tras estos cambios.

- [x] **6. Limpieza y Depuración del Directorio**
  - Eliminar la carpeta `formatolatex` que ya no es necesaria tras la migración.
  - Eliminar archivos PDF, log y auxiliares residuales de versiones previas (como `P2607-*`, `P2608-PR-MC-001 REV0.*`, y archivos `informe_caldera.*`).
  - Eliminar presentaciones de PowerPoint (ej: `100_t_h_Boiler_Thermal_Balance.pptx`), scripts redundantes (`mejorar_presentacion*.py`) y de logs (`indent.log`, `prompt1.txt`, `nul`).
  - Preguntarle al usuario si desea conservar la carpeta `scripts/` (la cual contiene el generador del diagrama `generate_diagrama_caldera.py`) y `GEMINI.md`. Tras la limpieza, solo perdurarán las carpetas (`.vscode`, `assets`, `config`, `emitido`, `references`, `sections`, `task`) y archivos directos de LaTeX.

## Tareas Finales: Transmittal y Anexos
- [x] **7. Actualizar Transmittal (HTML)**
  - Cambiar colores a modo oscuro moderno (`#121212`, `#1e1e1e`).
  - Actualizar referencias del proyecto al nuevo estándar (`P2807` y el nombre "*Memoria descriptiva indicador Toneladas Vapor/Toneladas Bagazo*").

## Tareas Nuevas: Presentación Interactiva (HTML)
- [x] **9. Generar Presentación Interactiva HTML (Reveal.js)**
  - Cambiar estrategia de PPTX a HTML utilizando biblioteca de presentaciones (ej. Reveal.js) en un solo archivo `emitido/P2807-PR-DP-001_Presentacion.html`.
  - Crear un diseño 100% infográfico, altamente estético y en "modo oscuro".
  - Estructurar 10 diapositivas detalladas basadas en la memoria de cálculo:
    1. Título y Contexto Institucional
    2. Introducción al Caso Colombiano
    3. Parámetros de Diseño y Objetivo (100 t/h)
    4. Propiedades del Bagazo (Humedad, Cenizas, PCI)
    5. Propiedades Termodinámicas (IAPWS-97)
    6. Balance de Materia (Circuitos de agua)
    7. Balance de Energía (Calor absorbido y combustible)
    8. KPI Principal: Ratio Vapor/Bagazo (2.655)
    9. Conclusiones Técnicas
    10. Guía de Modelado en Aspen Plus

## Revisión Final de Depuración y Transmittal
**Resumen de los cambios realizados:**
- El archivo base LaTeX fue renombrado a `P2608-PR-MC-001.tex`.
- La carpeta `formatolatex` y su contenido fueron eliminados después de rescatar los logos corporativos a `assets/logos/`.
- Se purgó el directorio de todos los remanentes inútiles para el proyecto base de LaTeX (.pptx, logs viejos, scripts innecesarios y archivos de reportes superados).
- Se rediseñó por completo el archivo `emitido/Transmittal_HRosero.html` para cumplir con la estética actual de "modo oscuro", actualizando todos los códigos (`P2807`), las descripciones del reporte y los remitentes.
- Se generó exitosamente la presentación Premium Interactiva en HTML `emitido/P2807-PR-DP-001_Presentacion.html` de 10 diapositivas basada totalmente en los cálculos del informe.

---

## Nuevas Tareas: Reorganización del Dashboard (2026-03-02)

### Objetivo
Mejorar la usabilidad del dashboard con tres cambios puntuales:

### Tareas

- [ ] **T1. Mostrar min/max debajo de cada input numérico (panel izquierdo)**
  - Archivo: `app/frontend/layouts/layout_main.py`
  - Función: `create_input_number()`
  - Cambio: añadir `html.Small(f"Min: {min_val} | Max: {max_val}")` debajo del `dcc.Input`
  - Afecta solo a los inputs numéricos (VAPOR, BAGAZO, AIRE), no a los de texto

- [ ] **T2. Gráfica siempre visible en la parte superior del área de contenido**
  - Archivo: `app/frontend/layouts/layout_main.py` — `create_content_area()`
  - Añadir un bloque fijo con dos `dcc.Graph` (`id='chart-top-ash'` y `id='chart-top-eff'`) siempre renderizado, con o sin cálculo
  - Archivo: `app/frontend/app.py` — nuevo callback
  - El callback usa datos base por defecto (humedad=48%, ceniza=10%, eficiencia=94%) para renderizar las curvas desde el inicio; se actualiza con los resultados tras calcular

- [ ] **T3. KPI indicators debajo de la gráfica**
  - Archivo: `app/frontend/layouts/layout_main.py` — `create_content_area()`
  - Reordenar el bloque `results-container`: primero gráfica (T2), luego kpi-ratio-container, luego kpi-secondary-container, luego tabs y reporte
  - El bloque de gráfica superior (T2) va fuera del `results-container` para que sea independiente del estado de cálculo
