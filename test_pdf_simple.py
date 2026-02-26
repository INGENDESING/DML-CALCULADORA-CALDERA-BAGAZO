"""
Test Simple - Botón PDF
========================
Script para probar la generación de PDF directamente.

DML INGENIEROS CONSULTORES S.A.S.
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'frontend'))

from components.report_generator import generate_pdf_report, is_pdf_generation_available
from balance import calculate_complete_balance, InputData

print('=' * 60)
print('  TEST PDF - DIRECTO')
print('=' * 60)
print()

# 1. Verificar disponibilidad
print('[1/4] Verificando librerias...')
if not is_pdf_generation_available():
    print('[ERROR] ReportLab no está disponible')
    print('   Ejecute: pip install reportlab')
    sys.exit(1)
print('[OK] ReportLab disponible')

# 2. Crear datos de prueba
print()
print('[2/4] Generando datos de prueba...')
input_data = InputData(
    m_stm=100, P_stm=106, T_stm=545, T_fw=270,
    pct_purge=2, efficiency=94,
    bagazo_humidity=48, bagazo_ash=10,
    altitude=1000, RH=75, T_amb=30, excess_air=20
)

results = calculate_complete_balance(input_data)

# Convertir a diccionario como lo hace el frontend
results_dict = {
    'ratio': float(results.ratio_stm_bagazo),
    'm_fw': float(results.feedwater.m_th), 'm_purge': float(results.blowdown.m_th),
    'm_stm': float(results.steam.m_th), 'm_bagazo': float(results.bagazo.m_th),
    'm_air': float(results.air.m_th), 'm_flue': float(results.flue_gas.m_th),
    'T_fw': results.feedwater.T_celsius, 'T_stm': results.steam.T_celsius,
    'T_purge': results.blowdown.T_celsius, 'T_flue': results.flue_gas.T_celsius,
    'P_stm': results.inputs.P_stm, 'T_amb': results.inputs.T_amb,
    'Q_fw': results.feedwater.energy_MW, 'Q_steam': results.steam.energy_MW,
    'Q_purge': results.blowdown.energy_MW, 'Q_fuel': results.Q_fuel_MW,
    'Q_abs': results.Q_abs_MW, 'losses': results.losses_MW,
}

inputs_dict = {
    'm_stm': input_data.m_stm, 'P_stm': input_data.P_stm, 'T_stm': input_data.T_stm,
    'T_fw': input_data.T_fw, 'pct_purge': input_data.pct_purge,
    'efficiency': input_data.efficiency, 'bagazo_humidity': input_data.bagazo_humidity,
    'bagazo_ash': input_data.bagazo_ash, 'altitude': input_data.altitude,
    'RH': input_data.RH, 'T_amb': input_data.T_amb, 'excess_air': input_data.excess_air,
}

print('[OK] Datos generados')
print(f'   Ratio: {results_dict["ratio"]:.3f} t/t')
print(f'   Q_abs: {results_dict["Q_abs"]:.2f} MW')

# 3. Generar PDF
print()
print('[3/4] Generando PDF...')
try:
    pdf_bytes = generate_pdf_report(results_dict, inputs_dict)
    if pdf_bytes:
        print(f'[OK] PDF generado: {len(pdf_bytes)} bytes')
    else:
        print('[ERROR] PDF vacío')
        sys.exit(1)
except Exception as e:
    print(f'[ERROR] Exception: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Guardar PDF
print()
print('[4/4] Guardando archivo...')
pdf_filename = 'test_reporte_caldera.pdf'
try:
    with open(pdf_filename, 'wb') as f:
        f.write(pdf_bytes)
    print(f'[OK] Archivo guardado: {pdf_filename}')
    print()
    print('=' * 60)
    print('  TEST EXITOSO')
    print(f'  Abra el archivo: {pdf_filename}')
    print('=' * 60)
except Exception as e:
    print(f'[ERROR] No se pudo guardar: {e}')
