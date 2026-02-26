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
