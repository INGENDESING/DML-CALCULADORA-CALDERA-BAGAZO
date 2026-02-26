# Calculadora de Caldera Acuotubular

**DML INGENIEROS CONSULTORES S.A.S.**

Aplicación web para el cálculo de balance de materia y energía en calderas acuotubulares que utilizan bagazo como combustible.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-2.18%2B-orange)](https://dash.plot.ly/)
[![License](https://img.shields.io/badge/License-Proprietary-red)](LICENSE)

---

## Características

- ✅ **Balance de materia** según normas ASME
- ✅ **Balance de energía** con cálculos termodinámicos IAPWS-97
- ✅ **Cálculo de ratio vapor/bagazo** - KPI principal
- ✅ **Análisis de combustión** con exceso de aire variable
- ✅ **Diagramas de proceso** (P&ID/PFD) interactivos
- ✅ **Gráficos paramétricos** de análisis
- ✅ **Generación de reportes PDF**
- ✅ **Interfaz moderna** con tema oscuro

---

## Capturas de Pantalla

### Interfaz Principal
![Interfaz Principal](docs/screenshots/main_interface.png)

### Resultados y KPIs
![Resultados](docs/screenshots/results.png)

### Gráficos de Análisis
![Gráficos](docs/screenshots/charts.png)

---

## Requisitos

- **Python:** 3.9 o superior
- **Navegador:** Chrome, Firefox, Edge, o Safari
- **Memoria:** 4 GB RAM mínimo (8 GB recomendado)

---

## Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/dml-ingenieros/calculadora-caldera.git
cd calculadora-caldera

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
python run.py
```

La aplicación estará disponible en: **http://127.0.0.1:8050**

---

## Uso

### Modo Desarrollo
```bash
python run.py
```

### Modo Producción
```bash
python run.py --prod
```

### Configurar Host y Puerto
```bash
python run.py --host 0.0.0.0 --port 8080
```

---

## Documentación

- 📖 [Manual de Usuario](MANUAL_USUARIO.md) - Guía completa de uso
- 🚀 [Guía de Deployment](DEPLOYMENT.md) - Instrucciones de instalación

---

## Estructura del Proyecto

```
calculadora-caldera/
├── app/
│   ├── backend/              # Módulos de cálculo
│   │   ├── thermodynamics.py # Propiedades IAPWS-97
│   │   ├── combustion.py     # Cálculos de combustión
│   │   ├── balance.py        # Balance materia/energía
│   │   ├── validators.py     # Validación de inputs
│   │   └── tests/            # Tests unitarios
│   └── frontend/             # Interfaz Dash
│       ├── app.py            # Aplicación principal
│       ├── components/       # Componentes UI
│       ├── layouts/          # Layouts
│       └── styles/           # Estilos
├── docs/                     # Documentación adicional
├── requirements.txt          # Dependencias
├── run.py                    # Script de ejecución
├── MANIFESTO.md
├── MANUAL_USUARIO.md
├── DEPLOYMENT.md
└── README.md
```

---

## Tests

Ejecutar suite de tests:

```bash
python -m pytest app/tests/ -v
```

**Resultados actuales:** 65/65 tests PASSED

---

## Tecnologías

| Tecnología | Uso |
|------------|-----|
| **Python** | Lenguaje principal |
| **Dash** | Framework web |
| **Plotly** | Gráficos interactivos |
| **IAPWS** | Propiedades del agua/vapor |
| **ReportLab** | Generación de PDF |
| **NumPy** | Cálculos numéricos |

---

## Autores

**Jonathan Arboleda Genes** - Ingeniero Mecánico
**Herminsul Rosero** - Ingeniero Mecánico

**DML INGENIEROS CONSULTORES S.A.S.**

---

## Licencia

Este proyecto es propiedad intelectual de **DML INGENIEROS CONSULTORES S.A.S.**

© 2026 DML INGENIEROS CONSULTORES S.A.S. Todos los derechos reservados.

---

## Soporte

Para soporte técnico contacte a:
- Email: info@dmlingenieros.com
- Tel: +57 XXX XXX XXXX

---

**Versión:** 1.0.0
**Última actualización:** Febrero 2026
