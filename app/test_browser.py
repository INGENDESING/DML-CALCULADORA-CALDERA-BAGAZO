"""
Script para probar la aplicación y capturar logs del navegador
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

# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
chrome_options.add_argument('--headless=False')  # Mostrar navegador
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')

# Iniciar WebDriver
print("Iniciando Chrome WebDriver...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Habilitar logging de consola
print("Navegando a la aplicación...")
driver.get("http://localhost:8050")

# Esperar a que la página cargue
time.sleep(5)

# Capturar logs de la consola
print("\n=== LOGS DE CONSOLA DEL NAVEGADOR ===")
logs = driver.get_log('browser')

if logs:
    for log in logs:
        level = log['level']
        message = log['message']
        source = log.get('source', 'unknown')
        timestamp = log.get('timestamp', 0)

        if level == 'SEVERE':
            print(f"[ERROR] {source}: {message}")
        elif level == 'WARNING':
            print(f"[WARN] {source}: {message}")
        elif level == 'INFO':
            print(f"[INFO] {source}: {message}")
else:
    print("No hay errores ni warnings en la consola.")

print(f"\nTotal de entradas de log: {len(logs)}")
errors = [l for l in logs if l['level'] == 'SEVERE']
warnings = [l for l in logs if l['level'] == 'WARNING']
print(f"Errores: {len(errors)}")
print(f"Warnings: {len(warnings)}")

# Verificar elementos de la página
print("\n=== VERIFICANDO ELEMENTOS DE LA PÁGINA ===")
try:
    # Verificar título
    title = driver.title
    print(f"Título: {title}")

    # Verificar elementos principales
    elements_to_check = [
        ("Input m_stm", "m_stm"),
        ("Input P_stm", "P_stm"),
        ("Botón Calcular", "btn-calculate"),
        ("Contenedor de resultados", "results-container"),
    ]

    for name, element_id in elements_to_check:
        try:
            element = driver.find_element(By.ID, element_id)
            print(f"[OK] {name}: encontrado")
        except:
            print(f"[MISSING] {name}: NO encontrado")

    # Verificar si hay mensajes de error visibles
    try:
        validation_msg = driver.find_element(By.ID, "validation-message")
        if validation_msg.is_displayed():
            print(f"[ALERT] Mensaje de validación visible: {validation_msg.text}")
        else:
            print("[OK] No hay mensajes de validación visibles")
    except:
        pass

except Exception as e:
    print(f"Error verificando elementos: {e}")

# Capturar screenshot
screenshot_path = "C:/Users/72-MS754/OneDrive/1.0 PROYECTOS DML/P2608 CALCULO CALDERA SOFTWARE/app/screenshot.png"
driver.save_screenshot(screenshot_path)
print(f"\nScreenshot guardado en: {screenshot_path}")

# Capturar HTML de la página
html_path = "C:/Users/72-MS754/OneDrive/1.0 PROYECTOS DML/P2608 CALCULO CALDERA SOFTWARE/app/page_source.html"
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(driver.page_source)
print(f"HTML fuente guardado en: {html_path}")

# Cerrar navegador
print("\nCerrando navegador...")
driver.quit()

print("\n=== RESUMEN ===")
if len(errors) == 0 and len(warnings) == 0:
    print("[SUCCESS] No se encontraron errores en la consola del navegador")
else:
    print(f"[INFO] Se encontraron {len(errors)} errores y {len(warnings)} warnings")
