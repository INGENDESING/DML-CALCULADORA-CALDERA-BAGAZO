# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║          CALCULADORA DE CALDERA AQUOTUBULAR DE COGENERACIÓN                   ║
# ║                    DML INGENIEROS CONSULTORES S.A.S.                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

## Descripción

Aplicación web interactiva para el balance de materia y energía de calderas
acuotubulares de cogeneración alimentadas con bagazo de caña de azúcar.

## Características

- Cálculo termodinámico con IAPWS-97
- Balance de materia y energía completo
- Diagrama P&ID/PFD interactivo
- Gráficos dinámicos con Plotly
- Generación de reportes PDF
- Modo oscuro/claro

## Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución Local

```bash
# Copiar variables de entorno
copy .env.example .env

# Ejecutar aplicación
python app/frontend/app.py
```

Abrir navegador en: http://localhost:8050

## Autores

- **Jonathan Arboleda Genes**, MSc. Chemical Engineering
- **Herminsul Rosero**, MSc. Process Engineering

## Propiedad Intelectual

© 2026 DML INGENIEROS CONSULTORES S.A.S.
Cali - Colombia
Tel: 661 24 08
Email: administrativo@dmlsas.com.co

## Licencia

Todos los derechos reservados.
