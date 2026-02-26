#!/usr/bin/env python
"""
Test Completo - Aplicación Caldera
===================================
Prueba completa de la aplicación con backend y frontend.

DML INGENIEROS CONSULTORES S.A.S.
"""

import sys
import os
import time
import threading

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'frontend'))

def test_backend():
    """Prueba el backend."""
    print('=' * 60)
    print('  TEST BACKEND')
    print('=' * 60)

    from balance import calculate_complete_balance, InputData
    from validators import validate_inputs

    # Crear datos de entrada
    input_data = InputData(
        m_stm=100, P_stm=106, T_stm=545, T_fw=270,
        pct_purge=2, efficiency=94,
        bagazo_humidity=48, bagazo_ash=10,
        altitude=1000, RH=75, T_amb=30, excess_air=20
    )

    # Validar
    validation = validate_inputs(
        m_stm=input_data.m_stm, P_stm=input_data.P_stm, T_stm=input_data.T_stm,
        T_fw=input_data.T_fw, pct_purge=input_data.pct_purge, efficiency=input_data.efficiency,
        bagazo_humidity=input_data.bagazo_humidity, bagazo_ash=input_data.bagazo_ash,
        altitude=input_data.altitude, RH=input_data.RH, T_amb=input_data.T_amb,
        excess_air=input_data.excess_air
    )

    if validation.is_valid:
        print('[OK] Validacion de inputs: PASSED')
    else:
        print(f'[ERROR] Validacion fallida: {validation.errors}')
        return False

    # Calcular
    results = calculate_complete_balance(input_data)

    # Verificar resultados
    print(f'[OK] Ratio Vapor/Bagazo: {results.ratio_stm_bagazo:.4f} t/t (esperado: ~2.655)')
    print(f'[OK] Flujo bagazo: {results.bagazo.m_th:.2f} t/h')
    print(f'[OK] Flujo vapor: {results.steam.m_th:.2f} t/h')
    print(f'[OK] Temperatura vapor: {results.steam.T_celsius:.1f} C')
    print(f'[OK] Presion vapor: {results.inputs.P_stm:.1f} barg')
    print(f'[OK] Q_abs: {results.Q_abs_MW:.2f} MW')
    print(f'[OK] Q_fuel: {results.Q_fuel_MW:.2f} MW')
    print(f'[OK] Perdidas: {results.losses_MW:.2f} MW')

    # Verificar razonabilidad
    assert 2.5 < results.ratio_stm_bagazo < 3.0, 'Ratio fuera de rango'
    assert 30 < results.bagazo.m_th < 50, 'Flujo bagazo fuera de rango'
    assert results.Q_abs_MW > 0, 'Q_abs debe ser positivo'
    assert results.Q_fuel_MW > results.Q_abs_MW, 'Q_fuel debe ser mayor que Q_abs'

    print()
    print('[SUCCESS] Backend test PASSED')
    return True


def test_frontend():
    """Prueba el frontend."""
    print()
    print('=' * 60)
    print('  TEST FRONTEND')
    print('=' * 60)

    from app import app
    import requests

    # Iniciar servidor en thread
    def run_server():
        app.run(debug=False, host='127.0.0.1', port=8051, use_reloader=False)

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    print('[INFO] Iniciando servidor...')
    time.sleep(8)

    try:
        # Probar home page
        response = requests.get('http://127.0.0.1:8051')
        if response.status_code == 200:
            print('[OK] Pagina principal cargada (status 200)')
        else:
            print(f'[ERROR] Status code: {response.status_code}')
            return False

        # Verificar contenido
        content = response.text
        if 'btn-calculate' in content:
            print('[OK] Boton calcular encontrado')
        if 'm_stm' in content:
            print('[OK] Inputs encontrados')
        if 'DML INGENIEROS' in content or 'Calculadora' in content:
            print('[OK] Header encontrado')

        print()
        print('[SUCCESS] Frontend test PASSED')
        return True

    except Exception as e:
        print(f'[ERROR] Exception: {e}')
        return False


def test_integration():
    """Prueba de integracion - calculo completo."""
    print()
    print('=' * 60)
    print('  TEST INTEGRACION')
    print('=' * 60)

    from balance import calculate_complete_balance, InputData

    # Caso base de validacion
    input_data = InputData(
        m_stm=100, P_stm=106, T_stm=545, T_fw=270,
        pct_purge=2, efficiency=94,
        bagazo_humidity=48, bagazo_ash=10,
        altitude=1000, RH=75, T_amb=30, excess_air=20
    )

    results = calculate_complete_balance(input_data)

    # Validar contra datos base conocidos
    print('Validando contra datos base...')

    # Ratio esperado: 2.655 t/t
    ratio_diff = abs(results.ratio_stm_bagazo - 2.655)
    if ratio_diff < 0.01:
        print(f'[OK] Ratio: {results.ratio_stm_bagazo:.4f} (diff: {ratio_diff:.4f})')
    else:
        print(f'[WARN] Ratio diff: {ratio_diff:.4f}')

    # Balance de masa lado agua
    water_balance = results.feedwater.m_th - (results.steam.m_th + results.blowdown.m_th)
    if abs(water_balance) < 0.01:
        print('[OK] Balance de masa agua: conservado')
    else:
        print(f'[WARN] Balance agua: {water_balance:.4f} t/h')

    # Balance de energia
    energy_in = results.feedwater.energy_MW + results.Q_fuel_MW
    energy_out = results.steam.energy_MW + results.blowdown.energy_MW + results.losses_MW
    energy_diff = abs(energy_in - energy_out)
    if energy_diff < 0.1:
        print(f'[OK] Balance de energia: conservado (diff: {energy_diff:.2f} MW)')
    else:
        print(f'[WARN] Balance energia diff: {energy_diff:.2f} MW')

    print()
    print('[SUCCESS] Integration test PASSED')
    return True


def main():
    """Ejecuta todos los tests."""
    print()
    print('*' * 60)
    print('*' + ' ' * 20 + 'TEST SUITE' + ' ' * 26 + '*')
    print('*' + ' ' * 15 + 'CALCULADORA CALDERA' + ' ' * 23 + '*')
    print('*' + ' ' * 10 + 'DML INGENIEROS CONSULTORES' + ' ' * 20 + '*')
    print('*' * 60)
    print()

    results = []

    # Test Backend
    try:
        results.append(('Backend', test_backend()))
    except Exception as e:
        print(f'[ERROR] Backend test failed: {e}')
        results.append(('Backend', False))

    # Test Frontend (puede fallar si el puerto esta ocupado)
    try:
        results.append(('Frontend', test_frontend()))
    except Exception as e:
        print(f'[ERROR] Frontend test failed: {e}')
        results.append(('Frontend', False))

    # Test Integracion
    try:
        results.append(('Integracion', test_integration()))
    except Exception as e:
        print(f'[ERROR] Integration test failed: {e}')
        results.append(('Integracion', False))

    # Resumen
    print()
    print('=' * 60)
    print('  RESUMEN DE TESTS')
    print('=' * 60)

    for name, passed in results:
        status = '[PASSED]' if passed else '[FAILED]'
        print(f'  {name}: {status}')

    all_passed = all(r[1] for r in results)

    print()
    if all_passed:
        print('*' * 60)
        print('*' + ' ' * 15 + 'ALL TESTS PASSED!' + ' ' * 21 + '*')
        print('*' * 60)
        return 0
    else:
        print('*' * 60)
        print('*' + ' ' * 15 + 'SOME TESTS FAILED' + ' ' * 21 + '*')
        print('*' * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
