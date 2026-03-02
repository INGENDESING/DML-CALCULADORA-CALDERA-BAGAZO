"""
Layout Principal - Estructura de la Aplicación
==============================================
Define el layout principal de la aplicación Dash.

DML INGENIEROS CONSULTORES S.A.S.
"""

import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc
from dash import dcc


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════

COLORS = {
    'bg_primary': '#1E1E1E',
    'bg_secondary': '#252526',
    'bg_tertiary': '#2D2D30',
    'accent': '#0078D4',
    'text_primary': '#FFFFFF',
    'text_secondary': '#CCCCCC',
    'border': '#3E3E42',
    'success': '#107C10',
    'warning': '#FF8C00',
    'error': '#E81123',
}


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════

def create_header() -> html.Div:
    """Crea el encabezado de la aplicación con logos mejorados."""
    return html.Div([
        html.Div([
            # Logos y título
            html.Div([
                # Logo DML
                html.Img(
                    src='/assets/logo1.png',
                    height='45px',
                    style={'marginRight': '15px', 'verticalAlign': 'middle'}
                ),
                # Logo CASTILLA
                html.Img(
                    src='/assets/logo2.png',
                    height='45px',
                    style={'marginRight': '20px', 'verticalAlign': 'middle'}
                ),
                # Separador vertical
                html.Div(style={
                    'width': '1px',
                    'height': '40px',
                    'background': COLORS['border'],
                    'marginRight': '20px'
                }),
                # Texto informativo
                html.Div([
                    html.H3('DML INGENIEROS CONSULTORES S.A.S.', style={
                        'margin': '0',
                        'fontSize': '20px',
                        'fontWeight': 'bold',
                        'color': COLORS['text_primary'],
                        'letterSpacing': '0.5px'
                    }),
                    html.P('Calculadora de Caldera Acuotubular con Bagazo', style={
                        'margin': '0',
                        'fontSize': '13px',
                        'color': COLORS['accent'],
                        'fontWeight': '500'
                    })
                ])
            ], style={'display': 'flex', 'alignItems': 'center'}),

            # Botones del header
            html.Div([
                html.Button([
                    html.I(className='fas fa-sun', style={'marginRight': '8px'}),
                    'Modo'
                ], id='btn-theme-toggle', n_clicks=0, style={
                    'background': COLORS['bg_tertiary'],
                    'color': COLORS['text_primary'],
                    'border': f"1px solid {COLORS['border']}",
                    'borderRadius': '6px',
                    'padding': '8px 16px',
                    'marginRight': '12px',
                    'cursor': 'pointer',
                    'fontSize': '13px'
                }),

                html.Button([
                    html.I(className='fas fa-info-circle', style={'marginRight': '8px'}),
                    'About'
                ], id='btn-about', n_clicks=0, style={
                    'background': COLORS['accent'],
                    'color': COLORS['text_primary'],
                    'border': 'none',
                    'borderRadius': '6px',
                    'padding': '8px 16px',
                    'cursor': 'pointer',
                    'fontSize': '13px'
                })
            ])
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'width': '100%'
        })
    ], style={
        'background': COLORS['bg_secondary'],
        'borderBottom': f"2px solid {COLORS['accent']}",
        'padding': '10px 24px',
        'boxShadow': '0 2px 12px rgba(0,0,0,0.4)',
        'position': 'sticky',
        'top': '0',
        'zIndex': '1000'
    })


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR - Panel de Entrada de Datos
# ═══════════════════════════════════════════════════════════════════════════════

def create_sidebar() -> html.Div:
    """Crea el sidebar con inputs de datos."""
    return html.Div([
        html.H4('DATOS DE ENTRADA', style={
            'margin': '0 0 20px 0',
            'color': COLORS['accent'],
            'fontSize': '14px',
            'textTransform': 'uppercase'
        }),

        # Metadatos del proyecto
        create_input_section('PROYECTO', [
            create_input_text('project_code', 'Código Proyecto', 'P2807'),
            create_input_text('document_code', 'Código Documento', 'P2807-PR-MC-001'),
            create_input_text('analyst', 'Analista', ''),
            create_input_text('date', 'Fecha', ''),
        ]),

        html.Hr(style={'border': f'1px solid {COLORS["border"]}', 'margin': '20px 0'}),

        # Datos de vapor
        create_input_section('VAPOR', [
            create_input_number('m_stm', 'Flujo de vapor', 100, 't/h', 10, 200),
            create_input_number('P_stm', 'Presión de vapor', 106, 'barg', 40, 150),
            create_input_number('T_stm', 'Temperatura vapor', 545, '°C', 400, 600),
            create_input_number('T_fw', 'Temp. agua alim.', 270, '°C', 150, 300),
            create_input_number('pct_purge', 'Purga continua', 2, '%', 0.5, 5),
            create_input_number('efficiency', 'Eficiencia térmica', 94, '%', 50, 95),
        ]),

        html.Hr(style={'border': f'1px solid {COLORS["border"]}', 'margin': '20px 0'}),

        # Datos de bagazo
        create_input_section('BAGAZO', [
            create_input_number('bagazo_humidity', 'Humedad', 48, '%', 40, 60),
            create_input_number('bagazo_ash', 'Cenizas', 10, '%', 1, 15),
        ]),

        html.Hr(style={'border': f'1px solid {COLORS["border"]}', 'margin': '20px 0'}),

        # Datos de aire
        create_input_section('AIRE', [
            create_input_number('altitude', 'Altitud', 1000, 'msnm', 0, 3000),
            create_input_number('RH', 'Humedad relativa', 75, '%', 30, 95),
            create_input_number('T_amb', 'Temp. ambiente', 30, '°C', 15, 40),
            create_input_number('excess_air', 'Exceso de aire', 20, '%', 10, 50),
        ]),

        html.Hr(style={'border': f'1px solid {COLORS["border"]}', 'margin': '20px 0'}),

        # Botón de cálculo
        html.Button([
            html.I(className='fas fa-calculator', style={'marginRight': '8px'}),
            'CALCULAR'
        ], id='btn-calculate', n_clicks=0, style={
            'width': '100%',
            'background': COLORS['accent'],
            'color': COLORS['text_primary'],
            'border': 'none',
            'borderRadius': '8px',
            'padding': '14px',
            'fontSize': '16px',
            'fontWeight': 'bold',
            'cursor': 'pointer',
            'transition': 'all 0.2s ease',
        }),

        # Mensaje de validación
        html.Div(id='validation-message', style={
            'marginTop': '16px',
            'padding': '12px',
            'borderRadius': '6px',
            'fontSize': '12px',
            'display': 'none'
        })
    ], style={
        'background': COLORS['bg_secondary'],
        'borderRight': f"1px solid {COLORS['border']}",
        'padding': '20px',
        'height': 'calc(100vh - 60px)',
        'overflowY': 'auto',
        'width': '320px',
        'minWidth': '320px'
    })


def create_input_section(title: str, inputs: list) -> html.Div:
    """Crea una sección de inputs."""
    return html.Div([
        html.Div(title, style={
            'fontSize': '12px',
            'color': COLORS['text_secondary'],
            'marginBottom': '12px',
            'fontWeight': 'bold'
        }),
        *inputs
    ])


def create_input_text(input_id: str, label: str, default: str = '') -> html.Div:
    """Crea un input de texto."""
    return html.Div([
        html.Label(label, style={
            'display': 'block',
            'fontSize': '11px',
            'color': COLORS['text_secondary'],
            'marginBottom': '4px'
        }),
        dcc.Input(
            id=input_id,
            type='text',
            value=default,
            placeholder=default,
            style={
                'width': '100%',
                'background': COLORS['bg_tertiary'],
                'color': COLORS['text_primary'],
                'border': f"1px solid {COLORS['border']}",
                'borderRadius': '4px',
                'padding': '6px 10px',
                'fontSize': '12px'
            }
        )
    ], style={'marginBottom': '12px'})


def create_input_number(input_id: str, label: str, default: float,
                        unit: str, min_val: float, max_val: float) -> html.Div:
    """Crea un input numérico."""
    return html.Div([
        html.Label(f'{label} [{unit}]', style={
            'display': 'block',
            'fontSize': '11px',
            'color': COLORS['text_secondary'],
            'marginBottom': '4px'
        }),
        dcc.Input(
            id=input_id,
            type='number',
            value=default,
            min=min_val,
            max=max_val,
            step=0.1,
            style={
                'width': '100%',
                'background': COLORS['bg_tertiary'],
                'color': COLORS['text_primary'],
                'border': f"1px solid {COLORS['border']}",
                'borderRadius': '4px',
                'padding': '6px 10px',
                'fontSize': '12px'
            }
        ),
        html.Small(f'Min: {min_val} | Max: {max_val}', style={
            'color': COLORS['text_secondary'],
            'fontSize': '10px',
            'opacity': '0.7'
        })
    ], style={'marginBottom': '12px'})


# ═══════════════════════════════════════════════════════════════════════════════
# CONTENT AREA - Panel de Resultados
# ═══════════════════════════════════════════════════════════════════════════════

def create_content_area() -> html.Div:
    """Crea el área de contenido con resultados."""
    return html.Div([
        # Diagrama PFD siempre visible
        html.Div(id='pid-always-visible'),

        # KPIs siempre visibles
        html.Div(id='kpi-ratio-container', style={'marginTop': '16px'}),
        html.Div(id='kpi-secondary-container', style={'marginTop': '12px'}),

        # Loading overlay
        html.Div(id='loading-overlay', style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'background': 'rgba(0,0,0,0.7)',
            'display': 'none',
            'justifyContent': 'center',
            'alignItems': 'center',
            'zIndex': '9999'
        }, children=[
            html.Div([
                html.I(className='fas fa-spinner fa-spin', style={
                    'fontSize': '48px',
                    'color': COLORS['accent']
                }),
                html.P('Calculando...', style={
                    'marginTop': '16px',
                    'color': COLORS['text_primary']
                })
            ])
        ]),

        # Mensaje inicial
        html.Div(id='initial-message', style={
            'textAlign': 'center',
            'padding': '100px 20px',
            'color': COLORS['text_secondary']
        }, children=[
            html.I(className='fas fa-calculator', style={
                'fontSize': '64px',
                'marginBottom': '20px',
                'opacity': '0.5'
            }),
            html.H2('Bienvenido a la Calculadora de Caldera', style={
                'color': COLORS['text_primary']
            }),
            html.P('Ingrese los datos en el panel lateral y haga clic en CALCULAR',
                   style={'marginTop': '16px'})
        ]),

        # Contenedor de resultados (oculto inicialmente)
        html.Div(id='results-container', style={
            'display': 'none'
        }, children=[
            # Tabs para diferentes vistas
            dcc.Tabs(id='results-tabs', value='tab-table', style={
                'background': COLORS['bg_secondary']
            }, children=[
                # Tab Gráficos oculto (código conservado en app.py callback)
                dcc.Tab(label='Tabla de Resultados', value='tab-table', style={
                    'background': COLORS['bg_tertiary'],
                    'color': COLORS['text_primary'],
                    'border': f"1px solid {COLORS['border']}",
                    'borderRadius': '6px 6px 0 0',
                    'padding': '10px 20px'
                }, selected_style={
                    'background': COLORS['accent'],
                    'color': COLORS['text_primary'],
                    'border': f"1px solid {COLORS['accent']}",
                }),
                dcc.Tab(label='Balance Energético', value='tab-sankey', style={
                    'background': COLORS['bg_tertiary'],
                    'color': COLORS['text_primary'],
                    'border': f"1px solid {COLORS['border']}",
                    'borderRadius': '6px 6px 0 0',
                    'padding': '10px 20px'
                }, selected_style={
                    'background': COLORS['accent'],
                    'color': COLORS['text_primary'],
                    'border': f"1px solid {COLORS['accent']}",
                }),
            ]),

            # Contenido de tabs
            html.Div(id='tabs-content', style={
                'padding': '20px 0'
            }),

            # Botón de reporte
            html.Div([
                html.Button([
                    html.I(className='fas fa-file-pdf', style={'marginRight': '8px'}),
                    'GENERAR REPORTE PDF'
                ], id='btn-report', n_clicks=0, style={
                    'background': COLORS['success'],
                    'color': COLORS['text_primary'],
                    'border': 'none',
                    'borderRadius': '6px',
                    'padding': '10px 24px',
                    'fontSize': '14px',
                    'fontWeight': 'bold',
                    'cursor': 'pointer',
                    'marginTop': '20px'
                })
            ], style={'textAlign': 'center'})
        ])
    ], style={
        'flex': '1',
        'padding': '24px',
        'overflowY': 'auto',
        'height': 'calc(100vh - 60px)'
    })


# ═══════════════════════════════════════════════════════════════════════════════
# LAYOUT COMPLETO
# ═══════════════════════════════════════════════════════════════════════════════

def create_layout() -> html.Div:
    """Crea el layout completo de la aplicación."""
    return html.Div([
        # Store para datos
        dcc.Store(id='store-results'),
        dcc.Store(id='store-theme', data='dark'),

        # Header
        create_header(),

        # Contenedor principal
        html.Div([
            # Sidebar
            create_sidebar(),

            # Content area
            create_content_area()
        ], style={
            'display': 'flex',
            'height': 'calc(100vh - 60px)'
        }),

        # Modal PDF - backdrop
        html.Div(style={
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'width': '100%',
            'height': '100%',
            'background': 'rgba(0,0,0,0.8)',
            'zIndex': '9998',
            'display': 'none'
        }, id='pdf-modal-backdrop'),
        # Modal PDF - contenido
        html.Div([
            html.Div([
                html.H4('REPORTE PDF', style={
                    'color': COLORS['text_primary'],
                    'margin': '0 0 15px 0'
                }),
                html.Div(id='pdf-modal-content', style={
                    'background': '#FFFFFF',
                    'borderRadius': '8px',
                    'padding': '10px',
                    'height': '500px'
                }),
                html.Div([
                    html.Button('Cerrar', id='btn-close-pdf-modal', n_clicks=0, style={
                        'background': COLORS['accent'],
                        'color': COLORS['text_primary'],
                        'border': 'none',
                        'borderRadius': '6px',
                        'padding': '8px 20px',
                        'cursor': 'pointer',
                        'marginTop': '15px'
                    })
                ], style={'textAlign': 'center'})
            ], style={
                'background': COLORS['bg_secondary'],
                'padding': '20px',
                'borderRadius': '12px',
                'maxWidth': '700px',
                'margin': '0 auto'
            })
        ], id='pdf-modal', style={
            'position': 'fixed',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'zIndex': '9999',
            'display': 'none',
            'width': '90%',
        }),

        # Modal About
        html.Div(id='modal-about', style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'background': 'rgba(0,0,0,0.7)',
            'display': 'none',
            'justifyContent': 'center',
            'alignItems': 'center',
            'zIndex': '9999'
        })
    ], style={
        'background': COLORS['bg_primary'],
        'minHeight': '100vh'
    })
