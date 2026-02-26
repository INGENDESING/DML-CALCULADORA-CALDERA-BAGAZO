#!/usr/bin/env python
"""
Generador de PDF Standalone
============================
Genera reporte PDF desde datos ingresados manualmente.

DML INGENIEROS CONSULTORES S.A.S.

Uso:
    python generate_pdf_standalone.py
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'frontend'))

from balance import calculate_complete_balance, InputData
from components.report_generator import generate_pdf_report
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# DATOS DE ENTRADA (MODIFICAR SEGÚN NECESITE)
# ═══════════════════════════════════════════════════════════════════════════════

print('=' * 70)
print('  GENERADOR DE PDF - CALCULADORA DE CALDERA')
print('  DML INGENIEROS CONSULTORES S.A.S.')
print('=' * 70)
print()

# Datos de entrada (valores por defecto)
input_data = InputData(
    m_stm=100,          # t/h  - Flujo de vapor
    P_stm=106,          # barg - Presión de vapor
    T_stm=545,          # °C   - Temperatura vapor
    T_fw=270,           # °C   - Temperatura agua alimentación
    pct_purge=2,        # %    - Purga continua
    efficiency=94,      # %    - Eficiencia térmica
    bagazo_humidity=48, # %    - Humedad del bagazo
    bagazo_ash=10,      # %    - Cenizas del bagazo
    altitude=1000,      # msnm - Altitud
    RH=75,              # %    - Humedad relativa
    T_amb=30,           # °C   - Temperatura ambiente
    excess_air=20,      # %    - Exceso de aire
)

# ═══════════════════════════════════════════════════════════════════════════════
# EJECUTAR CÁLCULO
# ═══════════════════════════════════════════════════════════════════════════════

print('Ejecutando balance de materia y energía...')
results = calculate_complete_balance(input_data)

print(f'  Ratio Vapor/Bagazo: {results.ratio_stm_bagazo:.4f} t/t')
print(f'  Flujo bagazo: {results.bagazo.m_th:.2f} t/h')
print(f'  Q_abs: {results.Q_abs_MW:.2f} MW')
print()

# ═══════════════════════════════════════════════════════════════════════════════
# PREPARAR DATOS PARA PDF
# ═══════════════════════════════════════════════════════════════════════════════

# Convertir resultados a diccionario
results_dict = {
    'ratio': float(results.ratio_stm_bagazo),
    'm_fw': float(results.feedwater.m_th),
    'm_purge': float(results.blowdown.m_th),
    'm_stm': float(results.steam.m_th),
    'm_bagazo': float(results.bagazo.m_th),
    'm_air': float(results.air.m_th),
    'm_flue': float(results.flue_gas.m_th),
    'T_fw': results.feedwater.T_celsius,
    'T_stm': results.steam.T_celsius,
    'T_purge': results.blowdown.T_celsius,
    'T_flue': results.flue_gas.T_celsius,
    'P_stm': results.inputs.P_stm,
    'T_amb': results.inputs.T_amb,
    'Q_fw': results.feedwater.energy_MW,
    'Q_steam': results.steam.energy_MW,
    'Q_purge': results.blowdown.energy_MW,
    'Q_fuel': results.Q_fuel_MW,
    'Q_abs': results.Q_abs_MW,
    'losses': results.losses_MW,
    'h_steam': results.steam_props['h'],
}

inputs_dict = {
    'm_stm': input_data.m_stm,
    'P_stm': input_data.P_stm,
    'T_stm': input_data.T_stm,
    'T_fw': input_data.T_fw,
    'pct_purge': input_data.pct_purge,
    'efficiency': input_data.efficiency,
    'bagazo_humidity': input_data.bagazo_humidity,
    'bagazo_ash': input_data.bagazo_ash,
    'altitude': input_data.altitude,
    'RH': input_data.RH,
    'T_amb': input_data.T_amb,
    'excess_air': input_data.excess_air,
}

# ═══════════════════════════════════════════════════════════════════════════════
# GENERAR PDF
# ═══════════════════════════════════════════════════════════════════════════════

print('Generando PDF...')
pdf_bytes = generate_pdf_report(results_dict, inputs_dict)

if pdf_bytes:
    # Guardar PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f'reporte_caldera_{timestamp}.pdf'

    with open(pdf_filename, 'wb') as f:
        f.write(pdf_bytes)

    print(f'[OK] PDF guardado: {pdf_filename}')
    print(f'     Tamaño: {len(pdf_bytes)} bytes')
    print()
    print('=' * 70)

    # Abrir el archivo automáticamente
    import subprocess
    subprocess.Popen(['start', pdf_filename], shell=True)
    print('Abriendo PDF...')

else:
    print('[ERROR] No se pudo generar el PDF')

print()
print('Para generar otro reporte con diferentes datos, modifique')
print('los valores en la sección DATOS DE ENTRADA de este script.')
print('=' * 70)
