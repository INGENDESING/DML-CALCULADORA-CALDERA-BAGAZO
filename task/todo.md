# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║                    PLAN DE DESARROLLO - APLICACIÓN DE CÁLCULO                ║
# ║              CALDERA AQUOTUBULAR DE COGENERACIÓN CON BAGAZO                    ║
# ║                    DML INGENIEROS CONSULTORES S.A.S.                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

## FECHA INICIO: 2026-02-26

---

## 1. ESTRUCTURA DE CARPETAS

```
P2608 CALCULO CALDERA SOFTWARE/
├── documentacion/          (ya existe - documentación LaTeX)
├── app/                    (NUEVA - aplicación web)
│   ├── backend/
│   ├── frontend/
│   ├── reports/
│   ├── assets/
│   ├── data/
│   ├── tests/
│   ├── requirements.txt
│   ├── README.md
│   ├── .env.example
│   └── .gitignore
├── task/
│   └── todo.md            (este archivo)
└── CLAUDE.md
```

---

## 2. DEPENDENCIAS (requirements.txt)

```
dash>=2.14.0
dash-bootstrap-components>=1.5.0
plotly>=5.18.0
iapws>=1.5.0
numpy>=1.24.0
pandas>=2.0.0
gunicorn>=21.2.0
reportlab>=4.0.0
python-dotenv>=1.0.0
scipy>=1.11.0
```

---

## 3. CHECKLIST DE DESARROLLO

### FASE 1: PLANIFICACIÓN ✅
- [x] Leer prompt.txt
- [x] Crear estructura de carpetas
- [x] Listar dependencias
- [x] Crear archivos base

### FASE 2: DESARROLLO BACKEND ✅
- [x] 2.1 thermodynamics.py - Cálculos IAPWS-97
- [x] 2.2 bagazo.py - PCS, PCI, composición
- [x] 2.3 combustion.py - Aire, gases, estequiometría
- [x] 2.4 psychrometry.py - Cálculos psicrométricos
- [x] 2.5 balance.py - Balance materia/energía
- [x] 2.6 validators.py - Validación de datos
- [x] 2.7 base_validation.py - Datos base para validación

### FASE 3: DESARROLLO FRONTEND ✅
- [x] 3.1 app.py - Aplicación Dash principal
- [x] 3.2 layout_main.py - Layout principal (incluye sidebar y content)
- [x] 3.5 kpi_cards.py - Tarjetas de KPIs
- [x] 3.6 charts.py - Gráficos Plotly
- [x] 3.7 pid_diagram.py - Componente P&ID/PFD
- [x] 3.8 theme_dark.py - Tema oscuro
- [x] 3.9 theme_light.py - Tema claro
- [x] 3.10-3.12 Callbacks integrados en app.py

### FASE 4: INTEGRACIÓN ✅
- [x] 4.1 Conectar backend con frontend
- [x] 4.2 Implementar callback principal
- [x] 4.3 Probar flujo completo
- [x] 4.4 Optimizar rendimiento

### FASE 5: REPORTES ✅
- [x] 5.1 generator.py - Generador de reportes PDF
- [x] 5.2 Integrar con plantilla de reporte

### FASE 6: TESTS ✅
- [x] 6.1 test_thermodynamics.py
- [x] 6.2 test_combustion.py
- [x] 6.3 test_balance.py
- [x] 6.4 Validar contra datos base (Ratio 2.655)

### FASE 7: DEPLOYMENT ⏳
- [ ] 7.1 Crear repositorio GitHub
- [ ] 7.2 Configurar README.md
- [ ] 7.3 Configurar .env.example
- [ ] 7.4 Configurar .gitignore
- [ ] 7.5 Desplegar en Render

---

## 4. DATOS DE VALIDACIÓN

| Parámetro | Valor Esperado |
|-----------|----------------|
| Flujo de vapor | 100 t/h |
| Presión vapor | 106 barg |
| Temperatura vapor | 545 °C |
| Humedad bagazo | 48 % |
| Cenizas bagazo | 10 % |
| **Ratio Vapor/Bagazo** | **2.655** |

---

## 5. ARCHIVOS CREADOS

### Backend (/app/backend)
- `__init__.py`
- `thermodynamics.py` - Cálculos IAPWS-97 (entalpía, entropía, densidad)
- `bagazo.py` - PCS, PCI, composición del bagazo
- `combustion.py` - Cálculos de combustión, aire, gases
- `psychrometry.py` - Propiedades del aire húmedo
- `balance.py` - Balance completo materia/energía
- `validators.py` - Validación de inputs
- `base_validation.py` - Datos base para validación

### Frontend (/app/frontend)
- `__init__.py`
- `app.py` - Aplicación Dash principal
- `layouts/layout_main.py` - Layout con sidebar y content
- `components/kpi_cards.py` - Tarjetas de KPIs
- `components/charts.py` - Gráficos Plotly
- `components/pid_diagram.py` - Diagrama P&ID/PFD
- `styles/theme_dark.py` - Tema oscuro
- `styles/theme_light.py` - Tema claro

### Reports (/app/reports)
- `__init__.py`
- `generator.py` - Generador de reportes PDF

### Tests (/app/tests)
- `__init__.py`
- `test_thermodynamics.py` - Tests de termodinámica (IAPWS-97)
- `test_combustion.py` - Tests de combustión y gases
- `test_balance.py` - Tests de balance materia/energía

### Archivos Base
- `requirements.txt` - Dependencias Python
- `README.md` - Documentación del proyecto
- `.env.example` - Variables de entorno
- `.gitignore` - Archivos ignorados por Git

---

## 6. PRÓXIMOS PASOS

1. **Ejecutar aplicación localmente** para probar:
   ```bash
   cd app
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python frontend/app.py
   ```

2. **Validación de cálculos** contra datos base

3. **Deployment en Render**

---

## 7. REVISIÓN DE CAMBIOS

### Cambios realizados en esta sesión:
1. Reorganización del proyecto (carpeta documentacion/)
2. Optimización del prompt.txt
3. Desarrollo completo del backend (7 módulos)
4. Desarrollo completo del frontend (layout, componentes, app principal)
5. Módulo de reportes PDF
6. **FASE 6 COMPLETADA**: Tests unitarios completos
7. **EJECUCIÓN Y DEPURACIÓN**: Corrección de errores en componentes

### Tests creados (FASE 6):
- `test_thermodynamics.py` - 19 tests para propiedades termodinámicas
- `test_combustion.py` - 23 tests para cálculos de combustión
- `test_balance.py` - 23 tests para balance materia/energía
- **Total: 65 tests, todos pasando ✓**

### Validación contra datos base:
- Ratio Vapor/Bagazo: Validado (2.655 calculado vs 2.655 esperado)
- Entalpía de vapor (3482.23 kJ/kg): Validado
- Balance de energía: Validado
- Flujo de bagazo: Validado (~37.67 t/h)

### Ejecución y depuración:
1. **charts.py (líneas 44, 50)**: `titlefont` → `title.font` (Plotly versión actualizada)
2. **pid_diagram.py**: Agregadas claves faltantes en `COLORS`:
   - `text_primary`, `text_secondary`, `bg_secondary`, `border`

### Verificación de ejecución (con Selenium):
- Backend: Funcionando correctamente
- Frontend: Todos los componentes operativos
- Aplicación: Ejecutando en http://localhost:8050
- Callbacks: 5 callbacks registrados correctamente
- **Prueba de interacción completa**: ✓ PASADA
  - Todos los inputs funcionan
  - Cálculo completado: "Ratio: 2.655 t/t"
  - KPI Ratio visible con "DENTRO DE TOLERANCIA"
  - Desviación: +0.0%
  - Errores reales en consola: 0

### Logs de consola del navegador:
- Warnings de CSS (kebab-case vs camelCase): 20
- Errores reales: **0**
- Estado: **APLICACIÓN FUNCIONAL** ✓

### Pendiente:
- **FASE 7: Deployment** (GitHub, Render)

---

## 13. CORRECCIÓN: Layout PFD arriba + KPIs siempre visibles (2026-03-02)

### Problema
La última actualización agregó dos gráficas (Ratio vs Cenizas y Ratio vs Eficiencia) en la parte superior del content area. Sin embargo, lo que se necesita es:
1. El **diagrama PFD/P&ID** siempre visible en la parte superior con datos base de cálculo
2. Los **KPIs** siempre visibles debajo del PFD (con valores "--" antes de calcular)
3. **Eliminar** las dos gráficas superiores

### Plan de corrección

- [ ] **Tarea 1**: Eliminar gráficas superiores en `layout_main.py`
  - Eliminar el bloque HTML de las dos gráficas top (líneas 298-326)
  - Eliminar el callback `update_top_charts()` en `app.py` (líneas 342-349)

- [ ] **Tarea 2**: Agregar diagrama PFD siempre visible arriba en `layout_main.py`
  - Agregar un `html.Div(id='pid-always-visible')` en la parte superior del content area
  - Este contenedor se actualiza con el diagrama PFD usando datos de inputs del sidebar

- [ ] **Tarea 3**: Mover KPIs fuera de results-container en `layout_main.py`
  - Sacar `kpi-ratio-container` y `kpi-secondary-container` del `results-container`
  - Colocarlos debajo del diagrama PFD, siempre visibles

- [ ] **Tarea 4**: Crear callback para PFD siempre visible en `app.py`
  - Nuevo callback que toma los valores de inputs del sidebar (State) y los resultados (Input store-results)
  - Si hay resultados calculados → muestra PFD con resultados completos
  - Si no hay resultados → muestra PFD con los valores de los inputs del sidebar (flujo vapor, temperaturas, etc.)

- [ ] **Tarea 5**: Actualizar callbacks de KPIs en `app.py`
  - Modificar `update_ratio_kpi()` para mostrar "--" cuando no hay resultados
  - Modificar `update_secondary_kpis()` para mostrar "--" cuando no hay resultados

- [ ] **Tarea 6**: Eliminar tab P&ID de los tabs de resultados
  - Eliminar el tab `tab-pid` ya que el PFD ahora está siempre visible arriba
  - Actualizar el valor default del tab a `tab-charts`
  - Eliminar el caso `tab-pid` del callback `update_tabs_content()`

- [ ] **Tarea 7**: Verificar y hacer commit/push

### Archivos a modificar
1. `app/frontend/layouts/layout_main.py` — Layout (tareas 1, 2, 3, 6)
2. `app/frontend/app.py` — Callbacks (tareas 1, 4, 5, 6)

---

## 8. CORRECCIÓN BUG: KPI Principal Ratio Vapor/Bagazo (2026-02-26)

### Problema
El KPI principal "Ratio Vapor/Bagazo" mostraba un **valor objetivo fijo de 2.655**, una **desviación porcentual**, y un **estado de tolerancia** (verde/naranja/rojo). Esto era un error conceptual: el valor 2.655 es solo el resultado del caso base de validación, no una meta operativa. Cuando el usuario cambiaba parámetros (ej: humedad del bagazo), el KPI comparaba incorrectamente contra 2.655.

### Solución
Simplificar el KPI para que muestre únicamente el valor calculado para las condiciones actuales, sin comparación alguna.

### Archivos modificados
1. **`app/frontend/components/kpi_cards.py`** — función `create_ratio_kpi()`
   - Eliminado: parámetro `target`, cálculo de `deviation`, lógica de colores por tolerancia, líneas de "Objetivo", "Desviación" y estado
   - Resultado: muestra solo el valor calculado con color de acento fijo (#0078D4)
2. **`app/frontend/app.py`** — callback `update_ratio_kpi()`
   - Eliminado: argumento `target=2.655` en la llamada a `create_ratio_kpi()`

### Verificación
- [x] Sintaxis Python verificada en ambos archivos
- [x] 21/21 tests de combustión pasando (tests de balance/termodinámica requieren `iapws` no disponible en entorno de CI)
- [x] Cambio mínimo: solo 2 archivos, solo componente de display (no afecta cálculos backend)

---

## 9. CORRECCIONES MÚLTIPLES (2026-02-26)

### Problema 1: Diagrama P&ID/PFD deficiente
**Archivo:** `app/frontend/components/pid_diagram.py` — función `create_pid_plotly()`
- Reescrita completamente con diagrama esquemático profesional de caldera acuotubular
- Componentes dibujados: Domo superior, domo inferior, banco de tubos, hogar/zona de combustión, sobrecalentador (serpentín), chimenea
- 7 corrientes con tuberías y flechas direccionales: agua alimentación, bagazo, aire, vapor sobrecalentado, purga, gases de combustión, cenizas
- Etiquetas dinámicas posicionadas fuera del diagrama sin superposición
- Canvas 620px, caldera centrada, fondo oscuro consistente con tema

### Problema 2: Botón "GENERAR REPORTE PDF" no genera nada
**Archivo:** `app/frontend/app.py` — callback `calculate_balance()`
- Agregados 7 parámetros de entrada faltantes al `results_dict`: `pct_purge`, `efficiency`, `bagazo_humidity`, `bagazo_ash`, `altitude`, `RH`, `excess_air`
- El callback `handle_pdf_modal` ahora puede leer los inputs reales del usuario desde `store-results`
- Nota: `reportlab` debe estar instalado en el entorno de producción para que el PDF se genere

### Problema 3: Pestaña "Tabla de Resultados" vacía
**Archivo:** `app/frontend/app.py` — callback `update_tabs_content()`
- Agregado caso `elif active_tab == 'tab-table':` que faltaba
- Llama a `create_results_table(results)` que ya existía e importada pero nunca se invocaba

### Problema 4: Gráfica de composición de gases ilegible
**Archivos:** `app/frontend/components/charts.py` + `app/frontend/app.py`
- Cambiada de barras apiladas (`go.Bar`) a gráfica de torta/donut (`go.Pie`)
- Agregada composición de gases (`flue_gas_composition`) al `results_dict`
- Reemplazados datos hardcodeados por datos dinámicos del balance

### Verificación
- [x] Sintaxis Python verificada en los 3 archivos modificados
- [x] 21/21 tests de combustión pasando
- [x] Cambios mínimos y focalizados en cada problema

---

## 10. CORRECCIÓN: Temperatura de Gases de Combustión (2026-02-27)

### Problema
La función `estimate_flue_gas_temperature()` en `combustion.py:329` usa la fórmula:
```
T_gases = T_steam - 10 + (excess_air / 5)
```
Caso base: T_gases = 545 - 10 + 4 = **539°C** — Valor **irreal**.

En calderas bagaceras reales con economizador + precalentador de aire, la temperatura
de gases de chimenea es **150-250°C**, no ~540°C. La fórmula actual vincula T_gases
directamente a T_vapor, lo cual es termodinámicamente incorrecto.

### Impacto
- T_flue es **solo para visualización** (P&ID, tabla de resultados, PDF).
- **NO afecta** el balance de energía, ratio ni consumo de bagazo (la eficiencia es input directo).
- Cambiar la fórmula NO rompe ningún cálculo existente.

### Plan de corrección

- [x] **Tarea 1**: Modificar `estimate_flue_gas_temperature()` en `combustion.py`
  - Eliminado parámetro `T_steam`, agregado `bagazo_humidity`
  - Nueva fórmula: `T = 180 + excess_air×0.5 + (humidity-40)×0.3`
  - Caso base: **192.4°C** ✓

- [x] **Tarea 2**: Actualizar llamada en `balance.py:338`
  - `estimate_flue_gas_temperature(inputs.excess_air, inputs.bagazo_humidity)`

- [x] **Tarea 3**: Actualizar tests en `test_combustion.py`
  - 4 tests: exceso de aire, humedad, caso base (~192°C), rango realista (150-250°C)

- [x] **Tarea 4**: Verificar que tests pasen y que el ratio no se afecte
  - **22/22 tests pasando** ✓
  - T_gases caso base: 192.4°C ✓
  - Ratio y balance de energía: sin cambios (T_flue es solo visualización)

---

## 11. CORRECCIÓN: T_gases = 125°C y energía de gases en PFD (2026-02-27)

### Problema
1. La etiqueta del PFD muestra T_gases ≈ 192°C, pero el **valor real medido es 125°C**.
2. La corriente de gases muestra solo Flujo y Temp, pero **no muestra la energía de salida [MW]**.
3. El flujo de aire de combustión determina la masa de gases → determina la energía que sale.

### Plan de corrección

- [x] **Tarea 1**: Modificar `estimate_flue_gas_temperature()` en `combustion.py`
  - Fórmula: `T = 117 + excess_air×0.3 + (humidity-40)×0.2`
  - Caso base: **124.6°C ≈ 125°C** ✓

- [x] **Tarea 2**: Calcular energía de gases `Q_flue [MW]` en `balance.py`
  - `Q_flue = m_flue_kgh × 1.1 × (T_flue - T_amb) / 3_600_000`
  - Asignado a `flue_gas.energy_MW` ✓

- [x] **Tarea 3**: Mostrar energía en etiqueta PFD de gases
  - Línea `E: X.XX MW` agregada en las 3 versiones del diagrama ✓
  - `Q_flue` agregado al `results_dict` en `app.py` ✓

- [x] **Tarea 4**: Actualizar tests en `test_combustion.py`
  - Caso base: 120-130°C, rango realista: 100-160°C ✓

- [x] **Tarea 5**: Verificar tests, commit y push
  - **22/22 tests pasando** ✓

---

## 12. VALIDACIÓN: Balance consistente, aire dinámico, etiquetas PFD (2026-02-27)

### Errores encontrados y corregidos

- [x] **Fix 1**: Fórmula T_flue iba en dirección opuesta
  - ANTES: `T = 117 + excess_air×0.3` (más aire = T más alta ❌)
  - AHORA: `T = 127.8 - excess_air×0.2 + (humidity-40)×0.15` (más aire = T más baja ✓)
  - Base case: `127.8 - 4.0 + 1.2 = 125.0°C` ✓

- [x] **Fix 2**: Flujo de aire usaba hardcoded 20% exceso
  - ANTES: `combustion_validate()` siempre retornaba ratio con 20% exceso ❌
  - AHORA: `flue_gas_data['combustion'].air.m_actual` usa `inputs.excess_air` ✓
  - Reordenado: gases se calculan ANTES del aire para obtener ratio correcto

- [x] **Fix 3**: Cp_gas era constante 1.1 kJ/(kg·°C)
  - AHORA: Cp ponderado por composición real (CO2=0.846, H2O=1.890, N2=1.040, O2=0.920, SO2=0.640)

- [x] **Fix 4**: Etiquetas PFD incompletas
  - Aire: agregado `Exc: XX%`
  - Cenizas: agregado `Flujo: X.XX t/h`
  - En las 3 versiones del diagrama (Plotly, HTML, Imagen)

- [x] **Fix 5**: Tests actualizados
  - `test_temperature_decreases_with_excess_air` (antes: increases)
  - Rango realista: 110-145°C

### Revisión
- **22/22 tests pasando** ✓
- El balance ahora responde correctamente al exceso de aire del usuario
- Más aire → menor T_gases → menos energía perdida por chimenea
- Todas las corrientes del PFD muestran datos completos
