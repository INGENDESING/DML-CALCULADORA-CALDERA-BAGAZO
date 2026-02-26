"""
Entry point for Render deployment
DML INGENIEROS CONSULTORES S.A.S.
"""
import sys
import os

# Agregar directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar y exponer el servidor
from app.frontend.app import server

# Para Render - detectar PORT
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    debug = os.environ.get('PRODUCTION', 'false') != 'true'
    from app.frontend.app import app
    app.run(debug=debug, host='0.0.0.0', port=port, use_reloader=False)
