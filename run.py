#!/usr/bin/env python
"""
Calculadora de Caldera Acuotubular
====================================
Script principal de ejecución.

DML INGENIEROS CONSULTORES S.A.S.
Autores: Jonathan Arboleda Genes, Herminsul Rosero

Uso:
    python run.py              # Modo desarrollo
    python run.py --prod       # Modo producción
    python run.py --host 0.0.0.0 --port 8080
"""

import sys
import os

# Agregar ruta del proyecto al path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Agregar ruta del backend
backend_path = os.path.join(project_root, 'app', 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Agregar ruta del frontend
frontend_path = os.path.join(project_root, 'app', 'frontend')
if frontend_path not in sys.path:
    sys.path.insert(0, frontend_path)


def parse_arguments():
    """Parsea argumentos de línea de comandos y variables de entorno."""
    args = {
        'host': '127.0.0.1',
        'port': 8050,
        'debug': True,
        'dev_tools_hot_reload': False,
        'dev_tools_prune_errors': True
    }

    # Render y otras plataformas definen PORT como variable de entorno
    if 'PORT' in os.environ:
        args['port'] = int(os.environ['PORT'])
        args['host'] = '0.0.0.0'  # Necesario para Render
        args['debug'] = False     # Siempre producción en la nube

    # Modo producción desde variable de entorno
    if os.environ.get('PRODUCTION') == 'true':
        args['debug'] = False

    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == '--prod':
            args['debug'] = False
        elif arg == '--host' and i + 1 < len(sys.argv):
            args['host'] = sys.argv[i + 1]
        elif arg == '--port' and i + 1 < len(sys.argv):
            args['port'] = int(sys.argv[i + 1])
        elif arg == '--help' or arg == '-h':
            print(__doc__)
            sys.exit(0)

    return args


def main():
    """Función principal."""
    print("=" * 60)
    print("  CALCULADORA DE CALDERA ACUOTUBULAR")
    print("  DML INGENIEROS CONSULTORES S.A.S.")
    print("=" * 60)
    print()

    # Parsear argumentos
    args = parse_arguments()

    # Importar aplicación
    try:
        from app.frontend.app import app
        print("[OK] Aplicación importada correctamente")
    except ImportError as e:
        print(f"[ERROR] No se pudo importar la aplicación: {e}")
        print("\nAsegúrese de instalar las dependencias:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    # Mostrar configuración
    mode = "DESARROLLO" if args['debug'] else "PRODUCCIÓN"
    print(f"\nModo: {mode}")
    print(f"Host: {args['host']}")
    print(f"Puerto: {args['port']}")
    print()
    print("-" * 60)
    print("Abra el navegador en:")
    print(f"  http://{args['host']}:{args['port']}")
    print("-" * 60)
    print()

    # Iniciar servidor
    try:
        app.run(
            host=args['host'],
            port=args['port'],
            debug=args['debug'],
            dev_tools_hot_reload=args['dev_tools_hot_reload'],
            dev_tools_prune_errors=args['dev_tools_prune_errors'],
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n\nServidor detenido por el usuario.")
    except Exception as e:
        print(f"\n[ERROR] Error al iniciar el servidor: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
