"""
Aplicación Principal - Calculadora de Caldera
===============================================
Aplicación Dash para balance de materia y energía
de calderas acuotubulares con bagazo.

DML INGENIEROS CONSULTORES S.A.S.
Autores Jonathan Arboleda Genes, Herminsul Rosero
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import os
from datetime import datetime

# Importar backend - agregar ruta al path
import sys
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
if backend_path not in sys.path:
    sys.path.append(backend_path)

from balance import calculate_complete_balance, InputData, format_results_table
from validators import validate_inputs, get_default_values
from base_validation import get_base_inputs, validate_complete_results

# Importar componentes frontend
from layouts.layout_main import create_layout
from components.kpi_cards import create_ratio_kpi, create_kpi_card, create_kpi_row
from components.charts import (
    create_ratio_vs_ash_curve,
    create_ratio_vs_efficiency_curve,
    create_flue_gas_composition,
    create_energy_sankey,
    create_results_comparison
)
from components.pid_diagram import create_pid_plotly, create_pid_html
from components.report_generator import generate_pdf_report, is_pdf_generation_available
from components.pdf_modal import create_pdf_modal


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

COLORS = {
    'bg_primary': '#1E1E1E',
    'bg_secondary': '#252526',
    'accent': '#0078D4',
    'success': '#107C10',
    'warning': '#FF8C00',
    'error': '#E81123',
    'text_primary': '#FFFFFF',
    'text_secondary': '#CCCCCC',
    'border': '#4C4C4C',
    'grid': '#3E3E42',
}


# ═══════════════════════════════════════════════════════════════════════════════
# INICIALIZAR APP
# ═══════════════════════════════════════════════════════════════════════════════

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
    ],
    suppress_callback_exceptions=True,
    title='Calculadora Caldera Acuotubular - DML'
)

app.layout = create_layout()


# ═══════════════════════════════════════════════════════════════════════════════
# CALLBACK Calcular
# ═══════════════════════════════════════════════════════════════════════════════

@app.callback(
    [Output('store-results', 'data'),
     Output('validation-message', 'style'),
     Output('validation-message', 'children'),
     Output('initial-message', 'style'),
     Output('results-container', 'style'),
     Output('loading-overlay', 'style')],
    [Input('btn-calculate', 'n_clicks')],
    [State('m_stm', 'value'),
     State('P_stm', 'value'),
     State('T_stm', 'value'),
     State('T_fw', 'value'),
     State('pct_purge', 'value'),
     State('efficiency', 'value'),
     State('bagazo_humidity', 'value'),
     State('bagazo_ash', 'value'),
     State('altitude', 'value'),
     State('RH', 'value'),
     State('T_amb', 'value'),
     State('excess_air', 'value')]
)
def calculate_balance(n_clicks, m_stm, P_stm, T_stm, T_fw, pct_purge, efficiency,
                     bagazo_humidity, bagazo_ash, altitude, RH, T_amb, excess_air):
    """Ejecuta el cálculo del balance cuando se hace clic en CALCULAR."""
    if n_clicks is None or n_clicks == 0:
        return {}, {'display': 'none'}, '', {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

    # Validar inputs
    inputs_dict = {
        'm_stm': m_stm, 'P_stm': P_stm, 'T_stm': T_stm, 'T_fw': T_fw,
        'pct_purge': pct_purge, 'efficiency': efficiency,
        'bagazo_humidity': bagazo_humidity, 'bagazo_ash': bagazo_ash,
        'altitude': altitude, 'RH': RH, 'T_amb': T_amb, 'excess_air': excess_air,
    }

    validation = validate_inputs(**inputs_dict)

    if not validation.is_valid:
        error_style = {'display': 'block', 'background': f'{COLORS["error"]}20',
                       'border': f'1px solid {COLORS["error"]}', 'color': COLORS['error'],
                       'padding': '12px', 'borderRadius': '6px', 'fontSize': '12px'}
        error_msg = html.Div([
            html.I(className='fas fa-exclamation-triangle', style={'marginRight': '8px'}),
            html.B('Errores de validación:'),
            html.Ul([html.Li(e.message) for e in validation.errors])
        ])
        return {}, error_style, error_msg, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}

    # Crear objeto InputData y ejecutar cálculo
    try:
        input_data = InputData(m_stm=m_stm, P_stm=P_stm, T_stm=T_stm, T_fw=T_fw,
                               pct_purge=pct_purge, efficiency=efficiency,
                               bagazo_humidity=bagazo_humidity, bagazo_ash=bagazo_ash,
                               altitude=altitude, RH=RH, T_amb=T_amb, excess_air=excess_air)
        results = calculate_complete_balance(input_data)

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
            'h_steam': results.steam_props['h'],
        }

        success_style = {'display': 'block', 'background': f'{COLORS["success"]}20',
                         'border': f'1px solid {COLORS["success"]}', 'color': COLORS['success'],
                         'padding': '12px', 'borderRadius': '6px', 'fontSize': '12px'}
        success_msg = html.Div([
            html.I(className='fas fa-check-circle', style={'marginRight': '8px'}),
            f'Cálculo completado. Ratio {results.ratio_stm_bagazo:.3f} t/t'
        ])
        return (results_dict, success_style, success_msg,
                {'display': 'none'}, {'display': 'block'}, {'display': 'none'})

    except Exception as e:
        error_style = {'display': 'block', 'background': f'{COLORS["error"]}20',
                       'border': f'1px solid {COLORS["error"]}', 'color': COLORS['error'],
                       'padding': '12px', 'borderRadius': '6px', 'fontSize': '12px'}
        return {}, error_style, f'Error en cálculo {str(e)}', {'display': 'block'}, {'display': 'none'}, {'display': 'none'}


# ═══════════════════════════════════════════════════════════════════════════════
# CALLBACK KPI Ratio
# ═══════════════════════════════════════════════════════════════════════════════

@app.callback(Output('kpi-ratio-container', 'children'), [Input('store-results', 'data')])
def update_ratio_kpi(results):
    if not results:
        return html.Div()
    return create_ratio_kpi(results['ratio'], target=2.655)


# ═══════════════════════════════════════════════════════════════════════════════
# CALLBACK KPIs Secundarios
# ═══════════════════════════════════════════════════════════════════════════════

@app.callback(Output('kpi-secondary-container', 'children'), [Input('store-results', 'data')])
def update_secondary_kpis(results):
    if not results:
        return html.Div()
    kpis = [
        {'title': 'Flujo Bagazo', 'value': f"{results['m_bagazo']:.2f}", 'unit': 't/h',
         'subtitle': 'Combustible', 'color': COLORS['warning']},
        {'title': 'Flujo Agua', 'value': f"{results['m_fw']:.2f}", 'unit': 't/h',
         'subtitle': 'Alimentación', 'color': COLORS['accent']},
        {'title': 'Calor Absorbido', 'value': f"{results['Q_abs']:.2f}", 'unit': 'MW',
         'subtitle': 'Q_abs', 'color': COLORS['success']},
        {'title': 'Calor Combustible', 'value': f"{results['Q_fuel']:.2f}", 'unit': 'MW',
         'subtitle': 'Q_fuel', 'color': COLORS['error']},
    ]
    return create_kpi_row(kpis)


# ═══════════════════════════════════════════════════════════════════════════════
# CALLBACK Tabs Content
# ═══════════════════════════════════════════════════════════════════════════════

@app.callback(Output('tabs-content', 'children'), [Input('results-tabs', 'value'), Input('store-results', 'data')])
def update_tabs_content(active_tab, results):
    if not results:
        return html.Div('Esperando resultados...', style={'textAlign': 'center', 'padding': '40px', 'color': COLORS['text_secondary']})

    if active_tab == 'tab-pid':
        return html.Div([html.H4('DIAGRAMA DE FLUJO DE PROCESO', style={'color': COLORS['text_primary'], 'marginBottom': '16px'}),
                         dcc.Graph(figure=create_pid_plotly(results), style={'height': '500px'})])
    elif active_tab == 'tab-charts':
        return html.Div([html.Div([html.Div([html.H5('Ratio vs Cenizas', style={'color': COLORS['text_primary']}),
                                                 dcc.Graph(figure=create_ratio_vs_ash_curve(results), style={'height': '300px'})],
                                                style={'width': '48%', 'display': 'inline-block'}),
                                   html.Div([html.H5('Ratio vs Eficiencia', style={'color': COLORS['text_primary']}),
                                                 dcc.Graph(figure=create_ratio_vs_efficiency_curve(results), style={'height': '300px'})],
                                                style={'width': '48%', 'float': 'right', 'display': 'inline-block'})],
                                   style={'width': '100%'}),
                         html.Hr(style={'border': f'1px solid {COLORS["border"]}', 'margin': '20px 0'}),
                         html.H5('Composición de Gases', style={'color': COLORS['text_primary']}),
                         dcc.Graph(figure=create_flue_gas_composition({'CO2': 12, 'H2O': 14, 'N2': 70, 'O2': 3, 'SO2': 1}), style={'height': '350px'})])
    elif active_tab == 'tab-sankey':
        return html.Div([html.H4('BALANCE DE ENERGÍA', style={'color': COLORS['text_primary'], 'marginBottom': '16px'}),
                         dcc.Graph(figure=create_energy_sankey({'Q_fw': results['Q_fw'], 'Q_fuel': results['Q_fuel'],
                                                              'Q_steam': results['Q_steam'], 'Q_purge': results['Q_purge'],
                                                              'losses': results['losses']}), style={'height': '400px'})])
    return html.Div()


# ═══════════════════════════════════════════════════════════════════════════════
# CALLBACK Generar Reporte PDF
# ═══════════════════════════════════════════════════════════════════════════════

@app.callback(
    [Output('pdf-modal-content', 'children'),
     Output('pdf-modal', 'style'),
     Output('pdf-modal-backdrop', 'style')],
    [Input('btn-report', 'n_clicks'),
     Input('btn-close-pdf-modal', 'n_clicks')],
    [State('store-results', 'data')],
    prevent_initial_call=True
)
def handle_pdf_modal(report_clicks, close_clicks, results):
    """Maneja la generación del PDF y el estado del modal."""
    button_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    # Cerrar modal
    if button_id == 'btn-close-pdf-modal' and close_clicks and close_clicks > 0:
        return None, {'display': 'none'}, {'display': 'none'}

    # Generar y mostrar PDF
    if button_id == 'btn-report' and report_clicks and report_clicks > 0:
        if not results:
            return html.Div('No hay resultados para generar reporte',
                          style={'color': COLORS['text_primary']}), {'display': 'none'}, {'display': 'none'}

        try:
            inputs = {
                'm_stm': results.get('m_stm', 100),
                'P_stm': results.get('P_stm', 106),
                'T_stm': results.get('T_stm', 545),
                'T_fw': results.get('T_fw', 270),
                'pct_purge': results.get('pct_purge', 2),
                'efficiency': results.get('efficiency', 94),
                'bagazo_humidity': results.get('bagazo_humidity', 48),
                'bagazo_ash': results.get('bagazo_ash', 10),
                'altitude': results.get('altitude', 1000),
                'RH': results.get('RH', 75),
                'T_amb': results.get('T_amb', 30),
                'excess_air': results.get('excess_air', 20),
            }

            pdf_bytes = generate_pdf_report(results, inputs)

            if pdf_bytes:
                import base64
                pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
                pdf_data_url = f'data:application/pdf;base64,{pdf_b64}'

                iframe = html.Iframe(
                    src=pdf_data_url,
                    style={
                        'width': '100%',
                        'height': '500px',
                        'border': 'none',
                        'borderRadius': '8px'
                    }
                )

                modal_style = {
                    'position': 'fixed',
                    'top': '50%',
                    'left': '50%',
                    'transform': 'translate(-50%, -50%)',
                    'zIndex': '9999',
                    'display': 'block'
                }

                backdrop_style = {
                    'position': 'fixed',
                    'top': 0,
                    'left': 0,
                    'width': '100%',
                    'height': '100%',
                    'background': 'rgba(0,0,0,0.8)',
                    'zIndex': '9998',
                    'display': 'block'
                }

                return iframe, modal_style, backdrop_style
            else:
                return html.Div('Error generando PDF',
                              style={'color': COLORS['error']}), {'display': 'none'}, {'display': 'none'}
        except Exception as e:
            print(f"Error generando PDF: {e}")
            return html.Div(f'Error: {str(e)}',
                          style={'color': COLORS['error']}), {'display': 'none'}, {'display': 'none'}

    return None, {'display': 'none'}, {'display': 'none'}


@app.callback(Output('store-theme', 'data'), [Input('btn-theme-toggle', 'n_clicks')], [State('store-theme', 'data')])
def toggle_theme(n_clicks, current_theme):
    return 'light' if n_clicks > 0 and current_theme == 'dark' else 'dark'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050, use_reloader=False)

server = app.server
