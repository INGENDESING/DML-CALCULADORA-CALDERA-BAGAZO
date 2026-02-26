#!/usr/bin/env python
"""
Test Selenium - Aplicación Completa
====================================
Script para probar la aplicación con Selenium.

DML INGENIEROS CONSULTORES S.A.S.
"""

import subprocess
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configurar paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'frontend'))

def test_app():
    """Ejecuta pruebas de la aplicación."""

    print('=' * 60)
    print('  TEST DE APLICACIÓN - CALCULADORA DE CALDERA')
    print('  DML INGENIEROS CONSULTORES S.A.S.')
    print('=' * 60)
    print()

    # Iniciar servidor
    print('[1/4] Iniciando servidor...')
    server_proc = subprocess.Popen(
        [sys.executable, 'run_app.py'],
        cwd=os.path.dirname(__file__),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Esperar a que el servidor inicie
    print('[2/4] Esperando que el servidor esté listo...')
    time.sleep(8)

    try:
        # Configurar Chrome
        print('[3/4] Iniciando navegador...')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(30)

        # Navegar a la aplicación
        print('       Abriendo http://127.0.0.1:8050')
        driver.get('http://127.0.0.1:8050')

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'btn-calculate')))

        print('[INFO] Pagina cargada correctamente')

        # Verificar elementos principales
        elements_to_check = [
            ('btn-calculate', 'Boton Calcular'),
            ('m_stm', 'Input Flujo Vapor'),
            ('P_stm', 'Input Presion Vapor'),
            ('initial-message', 'Mensaje Inicial'),
        ]

        for elem_id, description in elements_to_check:
            try:
                elem = driver.find_element(By.ID, elem_id)
                print(f'[OK] {description} encontrado')
            except:
                print(f'[ERROR] {description} NO encontrado')

        # Ingresar valores y calcular
        print()
        print('[4/4] Ejecutando calculo...')

        # Ingresar valores
        driver.find_element(By.ID, 'm_stm').clear()
        driver.find_element(By.ID, 'm_stm').send_keys('100')

        driver.find_element(By.ID, 'P_stm').clear()
        driver.find_element(By.ID, 'P_stm').send_keys('106')

        driver.find_element(By.ID, 'T_stm').clear()
        driver.find_element(By.ID, 'T_stm').send_keys('545')

        driver.find_element(By.ID, 'T_fw').clear()
        driver.find_element(By.ID, 'T_fw').send_keys('270')

        driver.find_element(By.ID, 'pct_purge').clear()
        driver.find_element(By.ID, 'pct_purge').send_keys('2')

        driver.find_element(By.ID, 'efficiency').clear()
        driver.find_element(By.ID, 'efficiency').send_keys('94')

        driver.find_element(By.ID, 'bagazo_humidity').clear()
        driver.find_element(By.ID, 'bagazo_humidity').send_keys('48')

        driver.find_element(By.ID, 'bagazo_ash').clear()
        driver.find_element(By.ID, 'bagazo_ash').send_keys('10')

        driver.find_element(By.ID, 'altitude').clear()
        driver.find_element(By.ID, 'altitude').send_keys('1000')

        driver.find_element(By.ID, 'RH').clear()
        driver.find_element(By.ID, 'RH').send_keys('75')

        driver.find_element(By.ID, 'T_amb').clear()
        driver.find_element(By.ID, 'T_amb').send_keys('30')

        driver.find_element(By.ID, 'excess_air').clear()
        driver.find_element(By.ID, 'excess_air').send_keys('20')

        # Hacer clic en CALCULAR
        calculate_btn = driver.find_element(By.ID, 'btn-calculate')
        calculate_btn.click()

        # Esperar resultados
        time.sleep(5)

        # Verificar resultados
        try:
            # Buscar el contenedor de resultados
            results_container = driver.find_element(By.ID, 'results-container')

            if results_container.is_displayed():
                print('[OK] Contenedor de resultados visible')
            else:
                print('[WARN] Contenedor de resultados no visible')

            # Verificar mensaje de validación
            try:
                validation_msg = driver.find_element(By.ID, 'validation-message')
                if validation_msg.is_displayed():
                    msg_text = validation_msg.text
                    print(f'[INFO] Mensaje validacion: {msg_text[:100]}')
            except:
                pass

            # Tomar screenshot
            screenshot_path = os.path.join(os.path.dirname(__file__), 'screenshot_test.png')
            driver.save_screenshot(screenshot_path)
            print(f'[INFO] Screenshot guardado en: {screenshot_path}')

        except Exception as e:
            print(f'[ERROR] No se pudieron verificar los resultados: {e}')

        # Verificar logs de consola
        print()
        print('[INFO] Logs de consola del navegador:')
        logs = driver.get_log('browser')
        if logs:
            for log in logs[-10:]:  # Últimos 10 logs
                level = log['level']
                msg = log['message'][:100]
                print(f'  [{level}] {msg}')
        else:
            print('  (No hay errores/warnings en consola)')

        print()
        print('=' * 60)
        print('  TEST FINALIZADO')
        print('=' * 60)

        driver.quit()

    except Exception as e:
        print(f'[ERROR] Exception during test: {e}')
        import traceback
        traceback.print_exc()

    finally:
        # Detener servidor
        print()
        print('[INFO] Deteniendo servidor...')
        server_proc.terminate()
        time.sleep(2)
        if server_proc.poll() is None:
            server_proc.kill()
        print('[OK] Servidor detenido')

if __name__ == '__main__':
    test_app()
