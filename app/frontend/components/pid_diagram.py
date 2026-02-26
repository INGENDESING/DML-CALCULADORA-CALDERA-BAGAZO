"""
Componente P&ID Diagram - Diagrama de Flujo Interactivo
========================================================
Componente para visualizar el diagrama de proceso de la caldera.

DML INGENIEROS CONSULTORES S.A.S.
"""

import dash.html as html
import plotly.graph_objects as go
from typing import Dict, List


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

COLORS = {
    'accent': '#0078D4',
    'success': '#107C10',
    'warning': '#FF8C00',
    'error': '#E81123',
    'bg_primary': '#1E1E1E',
    'bg_secondary': '#252526',
    'text_primary': '#FFFFFF',
    'text_secondary': '#CCCCCC',
    'border': '#4C4C4C',
    'stream_steam': '#E74C3C',     # Rojo para vapor
    'stream_water': '#3498DB',     # Azul para agua
    'stream_fuel': '#F39C12',      # Naranja para combustible
    'stream_air': '#95A5A6',       # Gris para aire
    'stream_flue': '#7F8C8D',      # Gris oscuro para gases
    'equipment': '#2C3E50',        # Azul oscuro para equipos
}


# ═══════════════════════════════════════════════════════════════════════════════
# STREAM TAG - ETIQUETA DE CORRIENTE
# ═══════════════════════════════════════════════════════════════════════════════

def create_stream_tag(name: str, data: Dict, stream_type: str = 'water') -> html.Div:
    """
    Crea una etiqueta para una corriente con sus propiedades.

    Parameters
    ----------
    name : str
        Nombre de la corriente
    data : dict
        Datos de la corriente {m, T, P, h, energy}
    stream_type : str
        Tipo de corriente (water, steam, fuel, air, flue)

    Returns
    -------
    html.Div
        Componente de etiqueta
    """
    # Color según tipo
    colors = {
        'water': COLORS['stream_water'],
        'steam': COLORS['stream_steam'],
        'fuel': COLORS['stream_fuel'],
        'air': COLORS['stream_air'],
        'flue': COLORS['stream_flue'],
    }
    border_color = colors.get(stream_type, COLORS['accent'])

    # Unidades según tipo
    units = {
        'm': 't/h',
        'T': '°C',
        'P': 'barg',
        'h': 'kJ/kg',
        'energy': 'MW'
    }

    rows = []

    # Nombre
    rows.append(html.Div(name, style={
        'fontWeight': 'bold',
        'fontSize': '12px',
        'textTransform': 'uppercase',
        'marginBottom': '8px',
        'color': border_color
    }))

    # Propiedades
    if 'm' in data:
        rows.append(html.Div(f"Flujo: {data['m']} {units['m']}", style={
            'fontSize': '11px', 'margin': '2px 0'
        }))
    if 'T' in data:
        rows.append(html.Div(f"Temp: {data['T']} {units['T']}", style={
            'fontSize': '11px', 'margin': '2px 0'
        }))
    if 'P' in data:
        rows.append(html.Div(f"Pres: {data['P']} {units['P']}", style={
            'fontSize': '11px', 'margin': '2px 0'
        }))
    if 'h' in data:
        rows.append(html.Div(f"h: {data['h']} {units['h']}", style={
            'fontSize': '11px', 'margin': '2px 0'
        }))
    if 'energy' in data:
        rows.append(html.Div(f"E: {data['energy']} {units['energy']}", style={
            'fontSize': '11px', 'margin': '2px 0',
            'fontWeight': 'bold'
        }))
    if 'composition' in data:
        comp = data['composition']
        if comp:
            rows.append(html.Div(f"C: {comp.get('C', '-')}%", style={
                'fontSize': '10px', 'margin': '1px 0', 'color': '#808080'
            }))
            rows.append(html.Div(f"H: {comp.get('H', '-')}%", style={
                'fontSize': '10px', 'margin': '1px 0', 'color': '#808080'
            }))

    return html.Div(rows, style={
        'background': '#252526',
        'border': f"2px solid {border_color}",
        'borderRadius': '8px',
        'padding': '8px 12px',
        'minWidth': '120px',
        'fontFamily': 'monospace'
    })


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAMA P&ID CON PLOTLY
# ═══════════════════════════════════════════════════════════════════════════════

def create_pid_plotly(results: Dict) -> go.Figure:
    """
    Crea diagrama P&ID usando Plotly.

    Parameters
    ----------
    results : dict
        Resultados del balance con datos de todas las corrientes

    Returns
    -------
    go.Figure
        Figura Plotly con el diagrama
    """
    fig = go.Figure()

    # Coordenadas del diagrama
    coords = {
        'feedwater': (0.2, 0.9),
        'bagazo': (0.1, 0.5),
        'air': (0.1, 0.2),
        'boiler': (0.4, 0.5),
        'steam': (0.7, 0.7),
        'blowdown': (0.7, 0.3),
        'flue_gas': (0.7, 0.2),
        'ash': (0.5, 0.1),
    }

    # Dibujar caldera (rectángulo)
    fig.add_shape(
        type='rect',
        x0=0.3, y0=0.35, x1=0.5, y1=0.65,
        line=dict(color=COLORS['equipment'], width=3),
        fillcolor='rgba(44, 62, 80, 0.3)'
    )

    # Etiqueta de caldera
    fig.add_annotation(
        x=0.4, y=0.5,
        text='<b>CALDERA<br>ACUOTUBULAR</b>',
        showarrow=False,
        font=dict(size=12, color=COLORS['text_primary']),
        bgcolor=COLORS['equipment'],
        bordercolor=COLORS['accent'],
        borderwidth=2,
        borderpad=8
    )

    # Dibujar corrientes (flechas)
    streams = [
        # From, To, Color
        ('feedwater', 'boiler', COLORS['stream_water']),
        ('bagazo', 'boiler', COLORS['stream_fuel']),
        ('air', 'boiler', COLORS['stream_air']),
        ('boiler', 'steam', COLORS['stream_steam']),
        ('boiler', 'blowdown', COLORS['stream_water']),
        ('boiler', 'flue_gas', COLORS['stream_flue']),
    ]

    for stream in streams:
        x0, y0 = coords[stream[0]]
        x1, y1 = coords[stream[1]]
        color = stream[2]

        # Ajustar coordenadas al borde de la caldera
        if stream[0] == 'feedwater':
            x1 = 0.3
            y1 = 0.55
        elif stream[0] == 'bagazo':
            x1 = 0.3
            y1 = 0.5
        elif stream[0] == 'air':
            x1 = 0.3
            y1 = 0.45
        elif stream[1] == 'steam':
            x0 = 0.5
            y0 = 0.55
        elif stream[1] == 'blowdown':
            x0 = 0.5
            y0 = 0.45
        elif stream[1] == 'flue_gas':
            x0 = 0.4
            y0 = 0.35
            y1 = 0.15

        fig.add_annotation(
            x=x1, y=y1,
            ax=x0, ay=y0,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=3,
            arrowcolor=color
        )

    # Añadir etiquetas de corrientes
    # Agua de alimentación
    fig.add_annotation(
        x=coords['feedwater'][0], y=coords['feedwater'][1],
        text=f'<b>AGUA ALIM.</b><br>{results.get("m_fw", "-")} t/h<br>{results.get("T_fw", "-")} °C<br>{results.get("Q_fw", "-")} MW',
        showarrow=False,
        font=dict(size=10, color=COLORS['text_primary']),
        bgcolor=COLORS['stream_water'],
        bordercolor=COLORS['stream_water'],
        borderwidth=2,
        borderpad=5
    )

    # Bagazo
    fig.add_annotation(
        x=coords['bagazo'][0], y=coords['bagazo'][1],
        text=f'<b>BAGAZO (AR)</b><br>{results.get("m_bagazo", "-")} t/h<br>{results.get("T_amb", "-")} °C<br>{results.get("Q_fuel", "-")} MW',
        showarrow=False,
        font=dict(size=10, color=COLORS['text_primary']),
        bgcolor=COLORS['stream_fuel'],
        bordercolor=COLORS['stream_fuel'],
        borderwidth=2,
        borderpad=5
    )

    # Aire
    fig.add_annotation(
        x=coords['air'][0], y=coords['air'][1],
        text=f'<b>AIRE</b><br>{results.get("m_air", "-")} t/h<br>{results.get("T_amb", "-")} °C',
        showarrow=False,
        font=dict(size=10, color=COLORS['text_primary']),
        bgcolor=COLORS['stream_air'],
        bordercolor=COLORS['stream_air'],
        borderwidth=2,
        borderpad=5
    )

    # Vapor
    fig.add_annotation(
        x=coords['steam'][0], y=coords['steam'][1],
        text=f'<b>VAPOR</b><br>{results.get("m_stm", "-")} t/h<br>{results.get("T_stm", "-")} °C<br>{results.get("P_stm", "-")} barg<br>{results.get("Q_steam", "-")} MW',
        showarrow=False,
        font=dict(size=10, color=COLORS['text_primary']),
        bgcolor=COLORS['stream_steam'],
        bordercolor=COLORS['stream_steam'],
        borderwidth=2,
        borderpad=5
    )

    # Purga
    fig.add_annotation(
        x=coords['blowdown'][0], y=coords['blowdown'][1],
        text=f'<b>PURGA</b><br>{results.get("m_purge", "-")} t/h<br>{results.get("T_purge", "-")} °C<br>{results.get("Q_purge", "-")} MW',
        showarrow=False,
        font=dict(size=10, color=COLORS['text_primary']),
        bgcolor=COLORS['stream_water'],
        bordercolor=COLORS['stream_water'],
        borderwidth=2,
        borderpad=5
    )

    # Gases
    fig.add_annotation(
        x=coords['flue_gas'][0], y=coords['flue_gas'][1],
        text=f'<b>GASES</b><br>{results.get("m_flue", "-")} t/h<br>{results.get("T_flue", "-")} °C<br>Pérdidas',
        showarrow=False,
        font=dict(size=10, color=COLORS['text_primary']),
        bgcolor=COLORS['stream_flue'],
        bordercolor=COLORS['stream_flue'],
        borderwidth=2,
        borderpad=5
    )

    # Layout
    fig.update_layout(
        title=dict(
            text='DIAGRAMA DE FLUJO DE PROCESO (PFD)',
            font=dict(size=16, color=COLORS['text_primary'])
        ),
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 1]),
        yaxis=dict(showgrid=False, showticklabels=False, range=[0, 1]),
        plot_bgcolor=COLORS['bg_primary'],
        paper_bgcolor=COLORS['bg_primary'],
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(family='Segoe UI, sans-serif')
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAMA P&ID HTML (versión simplificada)
# ═══════════════════════════════════════════════════════════════════════════════

def create_pid_html(results: Dict) -> html.Div:
    """
    Crea diagrama P&ID usando HTML/CSS (más simple).

    Parameters
    ----------
    results : dict
        Resultados del balance

    Returns
    -------
    html.Div
        Componente HTML con el diagrama
    """
    # Contenedor principal
    diagram = html.Div([
        # Título
        html.H4('DIAGRAMA DE FLUJO DE PROCESO (PFD)', style={
            'textAlign': 'center',
            'margin': '0 0 20px 0',
            'color': COLORS['accent']
        }),

        # Diagrama
        html.Div([
            # Columna de Entradas
            html.Div([
                # Agua de alimentación
                create_stream_tag('AGUA DE ALIMENTACIÓN', {
                    'm': results.get('m_fw', '-'),
                    'T': results.get('T_fw', '-'),
                    'energy': results.get('Q_fw', '-')
                }, 'water'),

                html.Div(style={'height': '20px'}),

                # Bagazo
                create_stream_tag('BAGAZO (AR)', {
                    'm': results.get('m_bagazo', '-'),
                    'T': results.get('T_amb', '-'),
                    'composition': results.get('bagazo_comp'),
                    'energy': results.get('Q_fuel', '-')
                }, 'fuel'),

                html.Div(style={'height': '20px'}),

                # Aire
                create_stream_tag('AIRE DE COMBUSTIÓN', {
                    'm': results.get('m_air', '-'),
                    'T': results.get('T_amb', '-'),
                }, 'air'),
            ], style={
                'width': '25%',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center'
            }),

            # Caldera (centro)
            html.Div([
                html.Div('CALDERA', style={
                    'fontWeight': 'bold',
                    'fontSize': '14px',
                    'marginBottom': '8px'
                }),
                html.Div('ACUOTUBULAR', style={
                    'fontSize': '12px',
                    'color': '#808080'
                }),
                html.Div(style={
                    'width': '120px',
                    'height': '120px',
                    'background': f'linear-gradient(135deg, {COLORS["equipment"]} 0%, #34495E 100%)',
                    'border': f'3px solid {COLORS["accent"]}',
                    'borderRadius': '12px',
                    'marginTop': '16px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'boxShadow': f'0 4px 20px {COLORS["accent"]}40'
                }, children=[
                    html.I(className='fas fa-fire', style={
                        'fontSize': '48px',
                        'color': COLORS['warning']
                    })
                ])
            ], style={
                'width': '40%',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center',
                'justifyContent': 'center'
            }),

            # Columna de Salidas
            html.Div([
                # Vapor
                create_stream_tag('VAPOR SOBREC.', {
                    'm': results.get('m_stm', '-'),
                    'T': results.get('T_stm', '-'),
                    'P': results.get('P_stm', '-'),
                    'h': results.get('h_steam', '-'),
                    'energy': results.get('Q_steam', '-')
                }, 'steam'),

                html.Div(style={'height': '20px'}),

                # Purga
                create_stream_tag('PURGA CONTINUA', {
                    'm': results.get('m_purge', '-'),
                    'T': results.get('T_purge', '-'),
                    'energy': results.get('Q_purge', '-')
                }, 'water'),

                html.Div(style={'height': '20px'}),

                # Gases
                create_stream_tag('GASES DE COMB.', {
                    'm': results.get('m_flue', '-'),
                    'T': results.get('T_flue', '-'),
                }, 'flue'),
            ], style={
                'width': '25%',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'center'
            })
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'padding': '20px'
        })
    ], style={
        'background': COLORS['bg_secondary'],
        'border': f'1px solid {COLORS["border"]}',
        'borderRadius': '12px',
        'padding': '20px'
    })

    return diagram
