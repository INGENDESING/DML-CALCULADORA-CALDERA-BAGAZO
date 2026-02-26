# MANUAL DE USUARIO
# Calculadora de Caldera Acuotubular
## DML INGENIEROS CONSULTORES S.A.S.

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Requisitos del Sistema](#2-requisitos-del-sistema)
3. [Instalación](#3-instalación)
4. [Inicio de la Aplicación](#4-inicio-de-la-aplicación)
5. [Descripción de la Interfaz](#5-descripción-de-la-interfaz)
6. [Guía de Uso Paso a Paso](#6-guía-de-uso-paso-a-paso)
7. [Descripción de Campos de Entrada](#7-descripción-de-campos-de-entrada)
8. [Interpretación de Resultados](#8-interpretación-de-resultados)
9. [Generación de Reportes](#9-generación-de-reportes)
10. [Solución de Problemas](#10-solución-de-problemas)

---

## 1. Introducción

La **Calculadora de Caldera Acuotubular** es una herramienta de ingeniería diseñada para realizar balances de materia y energía en calderas acuotubulares que utilizan bagazo como combustible.

### Características Principales

- Cálculo de balance de materia y energía según normas ASME
- Implementación de formulaciones IAPWS-97 para propiedades del agua/vapor
- Cálculo de ratio vapor/bagazo
- Análisis de combustión con exceso de aire
- Visualización de diagramas de proceso (P&ID)
- Gráficos de análisis paramétrico
- Generación de reportes en PDF
- Interfaz intuitiva con tema oscuro

---

## 2. Requisitos del Sistema

### Requisitos Mínimos

- **Sistema Operacional:** Windows 10+, macOS 10.14+, o Linux
- **Python:** 3.9 o superior
- **Navegador:** Chrome, Firefox, Edge, o Safari (versión reciente)
- **Memoria RAM:** 4 GB mínimo (8 GB recomendado)
- **Espacio en Disco:** 500 MB

### Dependencias de Python

```
dash>=2.18.0
dash-bootstrap-components>=1.6.0
plotly>=6.0.0
iapws>=1.5.0
reportlab>=4.2.0
```

---

## 3. Instalación

### 3.1 Instalar Python

1. Descargue Python desde [python.org](https://www.python.org/downloads/)
2. Ejecute el instalador
3. **IMPORTANTE:** Marque la opción "Add Python to PATH"

### 3.2 Instalar Dependencias

Abra una terminal o símbolo del sistema y ejecute:

```bash
cd "C:\ruta\a\la\carpeta\del\proyecto"
pip install -r requirements.txt
```

---

## 4. Inicio de la Aplicación

### 4.1 Modo Desarrollo (recomendado para pruebas)

```bash
python run.py
```

La aplicación estará disponible en: **http://127.0.0.1:8050**

### 4.2 Modo Producción

```bash
python run.py --prod
```

### 4.3 Configurar Host y Puerto

```bash
python run.py --host 0.0.0.0 --port 8080
```

---

## 5. Descripción de la Interfaz

### Layout General

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: Logo | Título | Botón Modo | Botón About           │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│   SIDEBAR    │         ÁREA DE CONTENIDO                    │
│   (Entradas) │         (Resultados)                         │
│              │                                              │
│  - Proyecto  │  - KPIs Principales                          │
│  - Vapor     │  - Gráficos                                  │
│  - Bagazo    │  - Tabs de Análisis                          │
│  - Aire      │  - Botón Generar Reporte                     │
│              │                                              │
│  [CALCULAR]  │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

### Componentes de la Interfaz

| Componente | Descripción |
|------------|-------------|
| **Header** | Barra superior con logo, título y controles |
| **Sidebar** | Panel izquierdo para ingreso de datos |
| **KPIs** | Indicadores clave de desempeño |
| **Tabs** | Pestañas con diferentes vistas de análisis |
| **Modal PDF** | Ventana emergente para visualizar reportes |

---

## 6. Guía de Uso Paso a Paso

### Paso 1: Iniciar la Aplicación

1. Abra una terminal
2. Navegue a la carpeta del proyecto
3. Ejecute: `python run.py`
4. Abra su navegador en http://127.0.0.1:8050

### Paso 2: Ingresar Datos del Proyecto

En el panel izquierdo, complete los campos:

**PROYECTO:**
- **Código Proyecto:** Identificador del proyecto (ej: P2807)
- **Código Documento:** Código del documento (ej: P2807-PR-MC-001)
- **Analista:** Nombre del analista
- **Fecha:** Fecha del cálculo (se llena automáticamente)

### Paso 3: Ingresar Datos de Vapor

Complete los parámetros del vapor:

| Campo | Descripción | Rango Típico |
|-------|-------------|--------------|
| Flujo de vapor | Caudal de vapor producido | 10 - 200 t/h |
| Presión de vapor | Presión de vapor a la salida | 40 - 150 barg |
| Temperatura vapor | Temperatura del vapor sobrecalentado | 400 - 600 °C |
| Temp. agua alim. | Temperatura del agua de alimentación | 150 - 300 °C |
| Purga continua | Porcentaje de purga de fondo | 0.5 - 5 % |
| Eficiencia térmica | Eficiencia esperada de la caldera | 50 - 95 % |

### Paso 4: Ingresar Datos de Bagazo

Complete los parámetros del combustible:

| Campo | Descripción | Rango Típico |
|-------|-------------|--------------|
| Humedad | Contenido de agua del bagazo | 40 - 60 % |
| Cenizas | Contenido de cenizas del bagazo | 1 - 15 % |

### Paso 5: Ingresar Datos de Aire

Complete los parámetros ambientales:

| Campo | Descripción | Rango Típico |
|-------|-------------|--------------|
| Altitud | Altitud sobre el nivel del mar | 0 - 3000 msnm |
| Humedad relativa | Humedad relativa ambiente | 30 - 95 % |
| Temp. ambiente | Temperatura ambiente | 15 - 40 °C |
| Exceso de aire | Exceso de aire para combustión | 10 - 50 % |

### Paso 6: Ejecutar Cálculo

1. Revise que todos los datos estén correctos
2. Haga clic en el botón **CALCULAR**
3. Espere unos segundos mientras se procesa
4. Los resultados aparecerán en el panel derecho

### Paso 7: Analizar Resultados

Los resultados incluyen:

**KPI Principal:**
- **Ratio Vapor/Bagazo:** Indica la cantidad de vapor producido por tonelada de bagazo

**KPIs Secundarios:**
- Flujo de Bagazo (t/h)
- Flujo de Agua de alimentación (t/h)
- Calor Absorbido (MW)
- Calor del Combustible (MW)

### Paso 8: Explorar las Pestañas de Análisis

**Diagrama P&ID/PFD:**
- Visualización esquemática del proceso
- Muestra flujos másicos y temperaturas

**Gráficos de Análisis:**
- Ratio vs Cenizas
- Ratio vs Eficiencia
- Composición de Gases de Combustión

**Tabla de Resultados:**
- Resumen tabular de todos los valores calculados

**Balance Energético:**
- Diagrama Sankey del flujo de energía

### Paso 9: Generar Reporte PDF

1. Haga clic en el botón **GENERAR REPORTE PDF**
2. Se abrirá una ventana emergente con el reporte
3. Use el botón de descarga del navegador para guardar el PDF
4. Cierre la ventana con el botón **Cerrar**

---

## 7. Descripción de Campos de Entrada

### 7.1 Datos del Proyecto

| Campo | Unidad | Descripción | Valor por Defecto |
|-------|--------|-------------|-------------------|
| Código Proyecto | - | Identificador único del proyecto | P2807 |
| Código Documento | - | Código del documento de cálculo | P2807-PR-MC-001 |
| Analista | - | Nombre del ingeniero responsable | - |
| Fecha | - | Fecha de realización del cálculo | Fecha actual |

### 7.2 Datos de Vapor

| Campo | Unidad | Descripción | Valor por Defecto |
|-------|--------|-------------|-------------------|
| Flujo de vapor | t/h | Caudal másico de vapor producido | 100 |
| Presión de vapor | barg | Presión del vapor a la salida | 106 |
| Temperatura vapor | °C | Temperatura del vapor sobrecalentado | 545 |
| Temp. agua alim. | °C | Temperatura del agua de alimentación | 270 |
| Purga continua | % | Porcentaje de purga de fondo | 2 |
| Eficiencia térmica | % | Eficiencia de la caldera | 94 |

### 7.3 Datos de Bagazo

| Campo | Unidad | Descripción | Valor por Defecto |
|-------|--------|-------------|-------------------|
| Humedad | % | Humedad sobre base húmeda | 48 |
| Cenizas | % | Contenido de cenizas | 10 |

### 7.4 Datos de Aire

| Campo | Unidad | Descripción | Valor por Defecto |
|-------|--------|-------------|-------------------|
| Altitud | msnm | Altitud sobre nivel del mar | 1000 |
| Humedad relativa | % | Humedad relativa ambiente | 75 |
| Temp. ambiente | °C | Temperatura seca del ambiente | 30 |
| Exceso de aire | % | Exceso de aire sobre el estequiométrico | 20 |

---

## 8. Interpretación de Resultados

### 8.1 Ratio Vapor/Bagazo

El ratio vapor/bagazo es el **KPI principal** e indica la eficiencia de la caldera:

| Valor | Interpretación |
|-------|----------------|
| < 2.0 | Bajo rendimiento |
| 2.0 - 2.4 | Rango normal |
| 2.4 - 2.7 | Buen rendimiento |
| > 2.7 | Excelente rendimiento |

**Valor objetivo:** 2.655 t/t (bajo condiciones de referencia)

### 8.2 Flujos Másicos

| Flujo | Descripción |
|-------|-------------|
| m_stm | Flujo de vapor producido |
| m_fw | Flujo de agua de alimentación |
| m_bagazo | Flujo de bagazo consumido |
| m_air | Flujo de aire de combustión |
| m_flue | Flujo de gases de combustión |

### 8.3 Balance de Energía

| Término | Descripción |
|---------|-------------|
| Q_fw | Energía del agua de alimentación |
| Q_steam | Energía del vapor producido |
| Q_fuel | Energía del combustible |
| Q_abs | Calor absorbido por el agua |
| losses | Pérdidas térmicas |

---

## 9. Generación de Reportes

### 9.1 Contenido del Reporte PDF

El reporte incluye:

1. **Portada** con logo y datos del proyecto
2. **Datos de Entrada** tabulados
3. **Resultados del Balance:**
   - Balance de materia
   - Balance de energía
   - Flujo de gases de combustión
4. **Eficiencia y Ratios** calculados
5. **Diagramas** (si están disponibles)

### 9.2 Guardar el Reporte

1. Haga clic en **GENERAR REPORTE PDF**
2. En la ventana emergente, use el navegador para:
   - **Chrome:** Menú → Imprimir → Destino: Guardar como PDF
   - **Firefox:** Menú → Imprimir → Destino: Guardar como PDF
   - **Edge:** Menú → Imprimir → Guardar como PDF

---

## 10. Solución de Problemas

### Problema: La aplicación no inicia

**Solución:**
1. Verifique que Python esté instalado: `python --version`
2. Verifique las dependencias: `pip list`
3. Reinstale dependencias: `pip install -r requirements.txt`

### Problema: Error al calcular

**Solución:**
1. Verifique que todos los campos tengan valores válidos
2. Revise los rangos permitidos para cada campo
3. Los valores fuera de rango mostrarán un mensaje de error

### Problema: El PDF no se genera

**Solución:**
1. Verifique que el cálculo se haya ejecutado correctamente
2. Espere a que aparezca el modal con el PDF
3. Si el PDF no carga, recargue la página y calcule nuevamente

### Problema: Los gráficos no se muestran

**Solución:**
1. Actualice el navegador a la última versión
2. Verifique que JavaScript esté habilitado
3. Limpie la caché del navegador

---

## Contacto

**DML INGENIEROS CONSULTORES S.A.S.**

Para soporte técnico o consultas:
- Email: info@dmlingenieros.com
- Tel: +57 XXX XXX XXXX

---

*Documento v1.0 - Febrero 2026*
