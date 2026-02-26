#!/usr/bin/env python
"""
Run Script - Calculadora de Caldera
====================================
Script para ejecutar la aplicación Dash.

DML INGENIEROS CONSULTORES S.A.S.
"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app', 'frontend'))

from app import app

if __name__ == '__main__':
    print('=' * 50)
    print('  CALCULADORA DE CALDERA ACUOTUBULAR')
    print('  DML INGENIEROS CONSULTORES S.A.S.')
    print('=' * 50)
    print()
    print('Iniciando servidor en: http://127.0.0.1:8050')
    print('Presione Ctrl+C para detener')
    print()
    app.run(debug=True, host='127.0.0.1', port=8050)
