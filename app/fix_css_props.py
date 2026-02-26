"""
Script para corregir propiedades CSS de kebab-case a camelCase en estilos inline
"""
import re
import os

# Mapeo de propiedades CSS de kebab-case a camelCase
CSS_PROPS = {
    'font-size': 'fontSize',
    'font-weight': 'fontWeight',
    'margin-top': 'marginTop',
    'margin-bottom': 'marginBottom',
    'margin-left': 'marginLeft',
    'margin-right': 'marginRight',
    'padding-top': 'paddingTop',
    'padding-bottom': 'paddingBottom',
    'padding-left': 'paddingLeft',
    'padding-right': 'paddingRight',
    'border-radius': 'borderRadius',
    'border-top': 'borderTop',
    'border-bottom': 'borderBottom',
    'border-left': 'borderLeft',
    'border-right': 'borderRight',
    'background-color': 'backgroundColor',
    'text-align': 'textAlign',
    'text-transform': 'textTransform',
    'align-items': 'alignItems',
    'justify-content': 'justifyContent',
    'flex-direction': 'flexDirection',
    'box-shadow': 'boxShadow',
    'overflow-y': 'overflowY',
    'overflow-x': 'overflowX',
    'min-width': 'minWidth',
    'max-width': 'maxWidth',
    'line-height': 'lineHeight',
    'letter-spacing': 'letterSpacing',
    'white-space': 'whiteSpace',
    'border-color': 'borderColor',
    'border-width': 'borderWidth',
    'border-style': 'borderStyle',
    'z-index': 'zIndex',
}

def fix_css_in_string(text):
    """Reemplaza propiedades CSS kebab-case por camelCase en estilos inline"""
    # Buscar patrones como 'font-size': '12px' o "font-size": "12px"
    for kebab, camel in CSS_PROPS.items():
        # Patrón para encontrar la propiedad en diferentes formatos de string
        # Buscar: 'kebab': o "kebab":
        pattern = rf"['\"]{re.escape(kebab)}['\"]:"

        def replace_func(match):
            quote = match.group(0)[0]  # Obtener la comilla usada (' o ")
            return f"{quote}{camel}:{quote}"

        text = re.sub(pattern, replace_func, text)

    return text

def process_file(filepath):
    """Procesa un archivo Python y corrige los estilos CSS"""
    print(f"Procesando: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Contar cambios antes
    original_content = content

    # Aplicar correcciones
    content = fix_css_in_string(content)

    # Verificar si hubo cambios
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        # Contar cuántas propiedades se corrigieron
        changes = []
        for kebab in CSS_PROPS:
            if kebab in original_content and f"'{CSS_PROPS[kebab]}':" in content:
                changes.append(f"  {kebab} -> {CSS_PROPS[kebab]}")

        print(f"  Cambios aplicados: {len(changes)}")
        for change in changes[:5]:  # Mostrar primeros 5
            print(change)
        if len(changes) > 5:
            print(f"  ... y {len(changes) - 5} más cambios")
        return True
    else:
        print("  Sin cambios necesarios")
        return False

# Archivos a procesar
archivos = [
    r'C:\Users\72-MS754\OneDrive\1.0 PROYECTOS DML\P2608 CALCULO CALDERA SOFTWARE\app\frontend\app.py',
    r'C:\Users\72-MS754\OneDrive\1.0 PROYECTOS DML\P2608 CALCULO CALDERA SOFTWARE\app\frontend\components\pid_diagram.py',
    r'C:\Users\72-MS754\OneDrive\1.0 PROYECTOS DML\P2608 CALCULO CALDERA SOFTWARE\app\frontend\layouts\layout_main.py',
    r'C:\Users\72-MS754\OneDrive\1.0 PROYECTOS DML\P2608 CALCULO CALDERA SOFTWARE\app\frontend\components\kpi_cards.py',
    r'C:\Users\72-MS754\OneDrive\1.0 PROYECTOS DML\P2608 CALCULO CALDERA SOFTWARE\app\frontend\styles\theme_light.py',
    r'C:\Users\72-MS754\OneDrive\1.0 PROYECTOS DML\P2608 CALCULO CALDERA SOFTWARE\app\frontend\styles\theme_dark.py',
]

print("=== CORRIGIENDO PROPIEDADES CSS KEBAB-CASE -> CAMELCASE ===\n")

cambios_totales = 0
for archivo in archivos:
    if os.path.exists(archivo):
        if process_file(archivo):
            cambios_totales += 1
            print()
    else:
        print(f"Archivo no encontrado: {archivo}\n")

print(f"\n=== RESUMEN ===")
print(f"Archivos modificados: {cambios_totales} de {len(archivos)}")
print("Correccion completada")
