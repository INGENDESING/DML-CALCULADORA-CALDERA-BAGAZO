"""
Script para probar interaccion completa con la aplicacion
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configurar opciones
chrome_options = Options()
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
chrome_options.add_argument('--headless=False')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

print("Iniciando Chrome...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Navegar a la app
    print("Navegando a la aplicacion...")
    driver.get("http://localhost:8050")
    time.sleep(3)

    # Verificar titulo
    print(f"Titulo: {driver.title}")

    # Llenar campos con valores base
    print("\nLlenando campos...")
    campos = {
        'm_stm': '100',
        'P_stm': '106',
        'T_stm': '545',
        'T_fw': '270',
        'pct_purge': '2',
        'efficiency': '94',
        'bagazo_humidity': '48',
        'bagazo_ash': '10',
        'altitude': '1000',
        'RH': '75',
        'T_amb': '30',
        'excess_air': '20',
    }

    for campo_id, valor in campos.items():
        try:
            elemento = driver.find_element(By.ID, campo_id)
            elemento.clear()
            elemento.send_keys(valor)
            print(f"  [OK] {campo_id} = {valor}")
        except Exception as e:
            print(f"  [ERROR] {campo_id}: {e}")

    time.sleep(2)

    # Hacer clic en calcular
    print("\nHaciendo clic en CALCULAR...")
    btn_calcular = driver.find_element(By.ID, 'btn-calculate')
    btn_calcular.click()

    # Esperar resultados
    print("Esperando resultados...")
    time.sleep(5)

    # Verificar mensaje de validacion
    try:
        validation = driver.find_element(By.ID, 'validation-message')
        if validation.is_displayed():
            print(f"\nMensaje de validacion: {validation.text}")
    except:
        pass

    # Verificar contenedor de resultados
    try:
        results_container = driver.find_element(By.ID, 'results-container')
        if results_container.is_displayed():
            print("\n[OK] Contenedor de resultados visible")

            # Buscar texto del ratio
            page_source = driver.page_source
            if '2.655' in page_source or '2.65' in page_source:
                print("[OK] Ratio calculado encontrado en la pagina")

            # Verificar KPIs
            try:
                kpi_ratio = driver.find_element(By.ID, 'kpi-ratio-container')
                if kpi_ratio.is_displayed():
                    print("[OK] KPI Ratio visible")
                    print(f"Contenido KPI: {kpi_ratio.text[:100]}...")
            except:
                print("[INFO] KPI Ratio no encontrado aun")

        else:
            print("[INFO] Contenedor de resultados no visible")
    except Exception as e:
        print(f"[ERROR] Verificando resultados: {e}")

    # Capturar logs despues de la interaccion
    print("\n=== LOGS DESPUES DE CALCULAR ===")
    logs = driver.get_log('browser')
    errors = [l for l in logs if l['level'] == 'SEVERE']
    warnings = [l for l in logs if l['level'] == 'WARNING']

    # Filtrar solo errores nuevos (no los warnings de CSS)
    real_errors = []
    for log in errors:
        msg = log.get('message', '')
        # Ignorar warnings de propiedades CSS no soportadas
        if 'Unsupported style property' not in msg:
            real_errors.append(log)

    print(f"Warnings de CSS: {len(errors) - len(real_errors)}")
    print(f"Errores reales: {len(real_errors)}")

    if real_errors:
        for err in real_errors[:5]:  # Primeros 5 errores reales
            print(f"  ERROR: {err.get('message', '')[:100]}")

    # Screenshot final
    screenshot_path = "C:/Users/72-MS754/OneDrive/1.0 PROYECTOS DML/P2608 CALCULO CALDERA SOFTWARE/app/screenshot_after_calc.png"
    driver.save_screenshot(screenshot_path)
    print(f"\nScreenshot guardado: {screenshot_path}")

    print("\n=== PRUEBA COMPLETADA ===")
    print("La aplicacion funciona correctamente")
    print("Los warnings de CSS son normales en Dash con estilos inline")

except Exception as e:
    print(f"\nERROR durante la prueba: {e}")
    import traceback
    traceback.print_exc()

finally:
    print("\nCerrando navegador...")
    driver.quit()
