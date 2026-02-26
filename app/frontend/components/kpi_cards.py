"""
Componente KPI Cards - Tarjetas de Indicadores Clave
====================================================
Componentes Dash para mostrar KPIs con estilo.

DML INGENIEROS CONSULTORES S.A.S.
"""

import dash.html as html
import dash.dcc as dcc
from dash import dash_table


# ═══════════════════════════════════════════════════════════════════════════════
# KPI CARD PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def create_kpi_card(title: str, value: str, unit: str = "",
                    subtitle: str = "", color: str = None,
                    icon: str = None, trend: float = None) -> html.Div:
    """
    Crea una tarjeta de KPI.

    Parameters
    ----------
    title : str
        Título del KPI
    value : str
        Valor principal (formateado)
    unit : str
        Unidad del valor
    subtitle : str
        Subtítulo o descripción
    color : str
        Color del acento (hex)
    icon : str
        Clase de icono (FontAwesome)
    trend : float
        Tendencia (+/-) para mostrar flecha

    Returns
    -------
    html.Div
        Componente de tarjeta KPI
    """
    trend_html = ""
    if trend is not None:
        trend_icon = "↑" if trend > 0 else "↓"
        trend_color = "#107C10" if trend > 0 else "#E81123"
        trend_html = html.Span(
            f" {trend_icon} {abs(trend):.1f}%",
            style={'color': trend_color, 'fontSize': '14px', 'marginLeft': '8px'}
        )

    icon_html = ""
    if icon:
        icon_html = html.I(
            className=icon,
            style={
                'fontSize': '24px',
                'color': color or '#0078D4',
                'marginBottom': '12px'
            }
        )

    return html.Div([
        html.Div([
            icon_html,
            html.Div(title, style={
                'fontSize': '14px',
                'color': '#808080',
                'textTransform': 'uppercase',
                'letterSpacing': '0.5px',
                'marginBottom': '8px'
            }),
            html.Div([
                html.Span(value, style={
                    'fontSize': '36px',
                    'fontWeight': 'bold',
                    'color': color or '#0078D4'
                }),
                html.Span(unit, style={
                    'fontSize': '18px',
                    'color': '#808080',
                    'marginLeft': '4px'
                }),
                trend_html
            ], style={'marginBottom': '4px'}),
            html.Div(subtitle, style={
                'fontSize': '12px',
                'color': '#808080'
            }) if subtitle else None
        ], style={'textAlign': 'center'})
    ], style={
        'background': f'linear-gradient(135deg, #2D2D30 0%, #252526 100%)',
        'border': f"2px solid {color or '#0078D4'}",
        'borderRadius': '12px',
        'padding': '20px',
        'textAlign': 'center',
        'boxShadow': '0 4px 16px rgba(0,120,212,0.2)',
        'height': '100%',
        'minHeight': '140px',
        'transition': 'all 0.3s ease',
    }, className='kpi-card')


# ═══════════════════════════════════════════════════════════════════════════════
# KPI CARD COMPACTO
# ═══════════════════════════════════════════════════════════════════════════════

def create_kpi_card_compact(title: str, value: str, unit: str = "",
                            color: str = None) -> html.Div:
    """
    Crea una tarjeta de KPI compacta.

    Parameters
    ----------
    title : str
        Título del KPI
    value : str
        Valor principal
    unit : str
        Unidad del valor
    color : str
        Color del acento

    Returns
    -------
    html.Div
        Componente de tarjeta compacta
    """
    return html.Div([
        html.Div(title, style={
            'fontSize': '12px',
            'color': '#808080',
            'marginBottom': '4px'
        }),
        html.Div([
            html.Span(value, style={
                'fontSize': '24px',
                'fontWeight': 'bold',
                'color': color or '#0078D4'
            }),
            html.Span(f" {unit}", style={
                'fontSize': '14px',
                'color': '#808080'
            })
        ])
    ], style={
        'background': '#2D2D30',
        'border': f"1px solid {color or '#3E3E42'}",
        'borderRadius': '8px',
        'padding': '12px 16px',
        'textAlign': 'center',
        'minWidth': '120px'
    })


# ═══════════════════════════════════════════════════════════════════════════════
# KPI CARD CON INDICADOR
# ═══════════════════════════════════════════════════════════════════════════════

def create_indicator_kpi(title: str, value: float, min_val: float = 0,
                         max_val: float = 100, unit: str = "",
                         thresholds: dict = None) -> html.Div:
    """
    Crea un KPI con indicador visual (gauge).

    Parameters
    ----------
    title : str
        Título del KPI
    value : float
        Valor actual
    min_val : float
        Valor mínimo del rango
    max_val : float
        Valor máximo del rango
    unit : str
        Unidad
    thresholds : dict
        Umbrales para colores {'warning': X, 'error': Y}

    Returns
    -------
    html.Div
        Componente con indicador
    """
    # Determinar color según valor
    color = '#0078D4'  # Default
    if thresholds:
        if value >= thresholds.get('error', max_val + 1):
            color = '#E81123'  # Rojo
        elif value >= thresholds.get('warning', max_val + 1):
            color = '#FF8C00'  # Naranja
        else:
            color = '#107C10'  # Verde

    # Porcentaje para la barra
    pct = (value - min_val) / (max_val - min_val) * 100
    pct = max(0, min(100, pct))

    return html.Div([
        html.Div(title, style={
            'fontSize': '14px',
            'color': '#808080',
            'marginBottom': '8px'
        }),
        html.Div([
            html.Span(f"{value:.1f}", style={
                'fontSize': '28px',
                'fontWeight': 'bold',
                'color': color
            }),
            html.Span(f" {unit}", style={
                'fontSize': '16px',
                'color': '#808080'
            })
        ], style={'marginBottom': '12px'}),
        html.Div([
            html.Div([
                html.Div(style={
                    'width': f'{pct}%',
                    'height': '100%',
                    'background': color,
                    'borderRadius': '4px',
                    'transition': 'width 0.5s ease'
                })
            ], style={
                'width': '100%',
                'height': '8px',
                'background': '#3E3E42',
                'borderRadius': '4px',
                'overflow': 'hidden'
            })
        ]),
        html.Div(f"{min_val} - {max_val} {unit}", style={
            'fontSize': '11px',
            'color': '#808080',
            'marginTop': '4px'
        })
    ], style={
        'background': '#2D2D30',
        'border': f"1px solid {color}",
        'borderRadius': '8px',
        'padding': '16px',
        'textAlign': 'center'
    })


# ═══════════════════════════════════════════════════════════════════════════════
# FILA DE KPIS
# ═══════════════════════════════════════════════════════════════════════════════

def create_kpi_row(kpis: list, n_cols: int = 4) -> html.Div:
    """
    Crea una fila con múltiples KPIs.

    Parameters
    ----------
    kpis : list
        Lista de diccionarios con los datos de cada KPI
        Cada diccionario: {title, value, unit, subtitle, color, icon}
    n_cols : int
        Número de columnas

    Returns
    -------
    html.Div
        Fila de KPIs
    """
    col_width = 12 // n_cols

    kpi_cards = []
    for kpi in kpis:
        kpi_cards.append(
            html.Div([
                create_kpi_card(
                    title=kpi.get('title', ''),
                    value=kpi.get('value', '-'),
                    unit=kpi.get('unit', ''),
                    subtitle=kpi.get('subtitle', ''),
                    color=kpi.get('color'),
                    icon=kpi.get('icon')
                )
            ], style={'padding': '8px'}, className=f'col-md-{col_width}')
        )

    return html.Div(kpi_cards, style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'margin': '0 -8px'
    })


# ═══════════════════════════════════════════════════════════════════════════════
# KPI PARA EL RATIO VAPOR/BAGAZO (PRINCIPAL)
# ═══════════════════════════════════════════════════════════════════════════════

def create_ratio_kpi(ratio: float, target: float = 2.655) -> html.Div:
    """
    Crea el KPI principal del ratio Vapor/Bagazo.

    Parameters
    ----------
    ratio : float
        Valor calculado del ratio
    target : float
        Valor objetivo

    Returns
    -------
    html.Div
        KPI del ratio
    """
    # Calcular desviación
    deviation = ((ratio - target) / target) * 100

    # Color según desviación
    if abs(deviation) <= 2:
        color = '#107C10'  # Verde - dentro de tolerancia
        status = "Dentro de tolerancia"
    elif abs(deviation) <= 5:
        color = '#FF8C00'  # Naranja - fuera de tolerancia pero aceptable
        status = "Fuera de tolerancia"
    else:
        color = '#E81123'  # Rojo - revisar
        status = "Revisar cálculos"

    return html.Div([
        html.Div([
            html.H3("RATIO VAPOR / BAGAZO", style={
                'fontSize': '14px',
                'color': '#808080',
                'margin': '0 0 16px 0',
                'textTransform': 'uppercase',
                'letterSpacing': '1px'
            }),
            html.Div([
                html.Span(f"{ratio:.3f}", style={
                    'fontSize': '64px',
                    'fontWeight': 'bold',
                    'color': color,
                    'lineHeight': '1'
                }),
                html.Span(" t_vapor/t_bagazo", style={
                    'fontSize': '18px',
                    'color': '#808080',
                    'marginLeft': '12px'
                })
            ], style={'marginBottom': '16px'}),
            html.Div([
                html.Span(f"Objetivo: {target:.3f}", style={
                    'fontSize': '14px',
                    'color': '#808080'
                }),
                html.Span(f" | Desviación: {deviation:+.1f}%", style={
                    'fontSize': '14px',
                    'color': color,
                    'marginLeft': '16px',
                    'fontWeight': 'bold'
                })
            ]),
            html.Div(status, style={
                'fontSize': '12px',
                'color': color,
                'marginTop': '8px',
                'textTransform': 'uppercase',
                'letterSpacing': '0.5px'
            })
        ], style={'textAlign': 'center'})
    ], style={
        'background': f'linear-gradient(135deg, #2D2D30 0%, #252526 100%)',
        'border': f"3px solid {color}",
        'borderRadius': '16px',
        'padding': '24px',
        'boxShadow': f'0 8px 32px {color}33',
    })


# ═══════════════════════════════════════════════════════════════════════════════
# TABLA DE RESULTADOS
# ═══════════════════════════════════════════════════════════════════════════════

def create_results_table(data: dict) -> dash_table.DataTable:
    """
    Crea una tabla con los resultados del balance.

    Parameters
    ----------
    data : dict
        Diccionario con los datos a mostrar

    Returns
    -------
    dash_table.DataTable
        Tabla de resultados
    """
    # Preparar datos para la tabla
    rows = []

    # Entradas
    rows.append({
        'Tipo': 'ENTRADA',
        'Corriente': 'Agua de Alimentación',
        'Flujo [t/h]': data.get('m_fw', '-'),
        'T [°C]': data.get('T_fw', '-'),
        'Energía [MW]': data.get('Q_fw', '-')
    })
    rows.append({
        'Tipo': 'ENTRADA',
        'Corriente': 'Bagazo (AR)',
        'Flujo [t/h]': data.get('m_bagazo', '-'),
        'T [°C]': data.get('T_amb', '-'),
        'Energía [MW]': data.get('Q_fuel', '-')
    })
    rows.append({
        'Tipo': 'ENTRADA',
        'Corriente': 'Aire de Combustión',
        'Flujo [t/h]': data.get('m_air', '-'),
        'T [°C]': data.get('T_amb', '-'),
        'Energía [MW]': '-'
    })

    # Separador
    rows.append({
        'Tipo': '',
        'Corriente': '',
        'Flujo [t/h]': '',
        'T [°C]': '',
        'Energía [MW]': ''
    })

    # Salidas
    rows.append({
        'Tipo': 'SALIDA',
        'Corriente': 'Vapor Sobrecalentado',
        'Flujo [t/h]': data.get('m_stm', '-'),
        'T [°C]': data.get('T_stm', '-'),
        'Energía [MW]': data.get('Q_steam', '-')
    })
    rows.append({
        'Tipo': 'SALIDA',
        'Corriente': 'Purga Continua',
        'Flujo [t/h]': data.get('m_purge', '-'),
        'T [°C]': data.get('T_purge', '-'),
        'Energía [MW]': data.get('Q_purge', '-')
    })
    rows.append({
        'Tipo': 'SALIDA',
        'Corriente': 'Gases de Combustión',
        'Flujo [t/h]': data.get('m_flue_gas', '-'),
        'T [°C]': data.get('T_flue', '-'),
        'Energía [MW]': 'Pérdidas'
    })

    return dash_table.DataTable(
        data=rows,
        columns=[
            {'name': 'Tipo', 'id': 'Tipo'},
            {'name': 'Corriente', 'id': 'Corriente'},
            {'name': 'Flujo [t/h]', 'id': 'Flujo [t/h]', 'type': 'numeric', 'format': {'specifier': '.2f'}},
            {'name': 'T [°C]', 'id': 'T [°C]', 'type': 'numeric', 'format': {'specifier': '.1f'}},
            {'name': 'Energía [MW]', 'id': 'Energía [MW]', 'type': 'numeric', 'format': {'specifier': '.2f'}},
        ],
        style_header={
            'backgroundColor': '#252526',
            'color': '#FFFFFF',
            'fontWeight': 'bold',
            'border': '1px solid #3E3E42',
        },
        style_cell={
            'backgroundColor': '#1E1E1E',
            'color': '#CCCCCC',
            'border': '1px solid #3E3E42',
            'padding': '8px',
            'textAlign': 'left',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 3},  # Fila separadora
                'backgroundColor': '#3E3E42',
                'height': '2px',
            }
        ],
        style_table={
            'border': '1px solid #3E3E42',
            'borderRadius': '8px',
            'overflow': 'hidden',
        }
    )
