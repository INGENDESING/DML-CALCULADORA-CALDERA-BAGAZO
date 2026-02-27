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

def _add_pipe(fig, x0, y0, x1, y1, color, width=3):
    """Dibuja una tubería (línea) entre dos puntos."""
    fig.add_shape(type='line', x0=x0, y0=y0, x1=x1, y1=y1,
                  line=dict(color=color, width=width))


def _add_arrow_head(fig, x, y, direction, color):
    """Dibuja una punta de flecha en la dirección indicada."""
    s = 0.012
    if direction == 'right':
        xs = [x, x - s, x - s, x]
        ys = [y, y + s * 0.7, y - s * 0.7, y]
    elif direction == 'left':
        xs = [x, x + s, x + s, x]
        ys = [y, y + s * 0.7, y - s * 0.7, y]
    elif direction == 'up':
        xs = [x, x - s * 0.7, x + s * 0.7, x]
        ys = [y, y - s, y - s, y]
    else:  # down
        xs = [x, x - s * 0.7, x + s * 0.7, x]
        ys = [y, y + s, y + s, y]
    fig.add_trace(go.Scatter(x=xs, y=ys, fill='toself', fillcolor=color,
                             line=dict(color=color, width=1),
                             hoverinfo='skip', showlegend=False))


def _add_label(fig, x, y, lines, color, align='left'):
    """Añade etiqueta de corriente con recuadro."""
    text = '<br>'.join(lines)
    fig.add_annotation(
        x=x, y=y, text=text, showarrow=False,
        font=dict(size=10, color='#FFFFFF', family='Consolas, monospace'),
        align=align, bgcolor='#252526',
        bordercolor=color, borderwidth=2, borderpad=6)


def create_pid_plotly(results: Dict) -> go.Figure:
    """
    Crea diagrama PFD profesional de caldera acuotubular usando Plotly.

    Componentes dibujados:
    - Domo superior e inferior (cilindros horizontales)
    - Banco de tubos (downcomers + risers)
    - Hogar / zona de combustión
    - Sobrecalentador (serpentín)
    - Chimenea
    - 7 corrientes con etiquetas dinámicas

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

    # ── Coordenadas principales ──────────────────────────────────────────
    # Canvas lógico: x=[0, 1], y=[0, 1]
    # Caldera centrada en x=[0.30, 0.62]

    # Hogar (zona de combustión) — rectángulo inferior
    hx0, hy0, hx1, hy1 = 0.30, 0.15, 0.62, 0.42
    fig.add_shape(type='rect', x0=hx0, y0=hy0, x1=hx1, y1=hy1,
                  line=dict(color='#E74C3C', width=2),
                  fillcolor='rgba(231, 76, 60, 0.08)')
    fig.add_annotation(x=(hx0 + hx1) / 2, y=(hy0 + hy1) / 2,
                       text='<b>HOGAR</b><br><i>Zona de Combustión</i>',
                       showarrow=False, font=dict(size=11, color='#E74C3C'),
                       opacity=0.7)

    # Domo superior — rectángulo redondeado (simulado)
    ds_x0, ds_y0, ds_x1, ds_y1 = 0.33, 0.72, 0.59, 0.82
    fig.add_shape(type='rect', x0=ds_x0, y0=ds_y0, x1=ds_x1, y1=ds_y1,
                  line=dict(color=COLORS['accent'], width=3),
                  fillcolor='rgba(0, 120, 212, 0.12)')
    fig.add_annotation(x=(ds_x0 + ds_x1) / 2, y=(ds_y0 + ds_y1) / 2,
                       text='<b>DOMO SUPERIOR</b><br><i>Separación vapor/agua</i>',
                       showarrow=False, font=dict(size=10, color=COLORS['accent']))

    # Domo inferior — rectángulo más pequeño
    di_x0, di_y0, di_x1, di_y1 = 0.37, 0.44, 0.55, 0.52
    fig.add_shape(type='rect', x0=di_x0, y0=di_y0, x1=di_x1, y1=di_y1,
                  line=dict(color=COLORS['stream_water'], width=2),
                  fillcolor='rgba(52, 152, 219, 0.12)')
    fig.add_annotation(x=(di_x0 + di_x1) / 2, y=(di_y0 + di_y1) / 2,
                       text='<b>DOMO INF.</b>', showarrow=False,
                       font=dict(size=9, color=COLORS['stream_water']))

    # Banco de tubos — líneas verticales entre domos (downcomers/risers)
    tube_xs = [0.38, 0.42, 0.46, 0.50, 0.54]
    for tx in tube_xs:
        fig.add_shape(type='line', x0=tx, y0=di_y1, x1=tx, y1=ds_y0,
                      line=dict(color='#4A90D9', width=1.5, dash='dot'))

    # Sobrecalentador — serpentín a la derecha del domo superior
    sh_x0, sh_y0 = 0.59, 0.61
    sh_x1, sh_y1 = 0.66, 0.82
    fig.add_shape(type='rect', x0=sh_x0, y0=sh_y0, x1=sh_x1, y1=sh_y1,
                  line=dict(color=COLORS['stream_steam'], width=2),
                  fillcolor='rgba(231, 76, 60, 0.08)')
    # Líneas de serpentín
    for sy in [0.65, 0.69, 0.73, 0.77]:
        fig.add_shape(type='line', x0=sh_x0 + 0.01, y0=sy,
                      x1=sh_x1 - 0.01, y1=sy,
                      line=dict(color=COLORS['stream_steam'], width=1.5))
    fig.add_annotation(x=(sh_x0 + sh_x1) / 2, y=sh_y1 + 0.025,
                       text='<b>S.H.</b>', showarrow=False,
                       font=dict(size=9, color=COLORS['stream_steam']))

    # Chimenea — rectángulo vertical sobre el hogar
    ch_x0, ch_y0 = 0.43, 0.82
    ch_x1, ch_y1 = 0.49, 0.96
    fig.add_shape(type='rect', x0=ch_x0, y0=ch_y0, x1=ch_x1, y1=ch_y1,
                  line=dict(color=COLORS['stream_flue'], width=2),
                  fillcolor='rgba(127, 140, 141, 0.1)')
    fig.add_annotation(x=(ch_x0 + ch_x1) / 2, y=(ch_y0 + ch_y1) / 2,
                       text='<b>CHIM.</b>', showarrow=False,
                       font=dict(size=9, color=COLORS['stream_flue']),
                       textangle=-90)

    # Etiqueta central de equipo
    fig.add_annotation(
        x=(hx0 + hx1) / 2, y=0.05,
        text='<b>CALDERA ACUOTUBULAR</b>',
        showarrow=False,
        font=dict(size=13, color=COLORS['text_primary']),
        bgcolor=COLORS['equipment'], bordercolor=COLORS['accent'],
        borderwidth=2, borderpad=6)

    # ── TUBERÍAS DE CORRIENTES ───────────────────────────────────────────

    # 1) Agua de alimentación → domo superior (izquierda)
    _add_pipe(fig, 0.15, 0.77, ds_x0, 0.77, COLORS['stream_water'])
    _add_arrow_head(fig, ds_x0, 0.77, 'right', COLORS['stream_water'])

    # 2) Bagazo → hogar (izquierda, medio)
    _add_pipe(fig, 0.15, 0.33, hx0, 0.33, COLORS['stream_fuel'])
    _add_arrow_head(fig, hx0, 0.33, 'right', COLORS['stream_fuel'])

    # 3) Aire → hogar (izquierda, abajo)
    _add_pipe(fig, 0.15, 0.22, hx0, 0.22, COLORS['stream_air'])
    _add_arrow_head(fig, hx0, 0.22, 'right', COLORS['stream_air'])

    # 4) Vapor sobrecalentado → sale del sobrecalentador (derecha)
    _add_pipe(fig, sh_x1, 0.71, 0.85, 0.71, COLORS['stream_steam'])
    _add_arrow_head(fig, 0.85, 0.71, 'right', COLORS['stream_steam'])

    # 5) Purga → sale del domo inferior (derecha)
    _add_pipe(fig, di_x1, 0.48, 0.85, 0.48, COLORS['stream_water'])
    _add_arrow_head(fig, 0.85, 0.48, 'right', COLORS['stream_water'])

    # 6) Gases de combustión → salen por chimenea (arriba)
    # (ya la chimenea indica la salida, la flecha va en la parte superior)
    _add_arrow_head(fig, (ch_x0 + ch_x1) / 2, ch_y1, 'up', COLORS['stream_flue'])

    # 7) Cenizas → salen por debajo del hogar
    _add_pipe(fig, (hx0 + hx1) / 2, hy0, (hx0 + hx1) / 2, 0.08, '#8B7355')
    _add_arrow_head(fig, (hx0 + hx1) / 2, 0.08, 'down', '#8B7355')

    # Conexión domo superior → sobrecalentador
    _add_pipe(fig, ds_x1, 0.77, sh_x0, 0.77, COLORS['stream_steam'], 2)

    # ── ETIQUETAS DE CORRIENTES ──────────────────────────────────────────

    # Agua de alimentación (izquierda arriba)
    m_fw = results.get('m_fw', '-')
    T_fw = results.get('T_fw', '-')
    Q_fw = results.get('Q_fw', '-')
    _add_label(fig, 0.07, 0.88,
               ['<b>AGUA DE ALIMENTACIÓN</b>',
                f'Flujo: {m_fw} t/h',
                f'Temp: {T_fw} °C',
                f'E: {Q_fw} MW'],
               COLORS['stream_water'])

    # Bagazo (izquierda medio)
    m_bag = results.get('m_bagazo', '-')
    T_amb = results.get('T_amb', '-')
    Q_fuel = results.get('Q_fuel', '-')
    _add_label(fig, 0.07, 0.38,
               ['<b>BAGAZO (AR)</b>',
                f'Flujo: {m_bag} t/h',
                f'Temp: {T_amb} °C',
                f'E: {Q_fuel} MW'],
               COLORS['stream_fuel'])

    # Aire (izquierda abajo)
    m_air = results.get('m_air', '-')
    exc_air = results.get('excess_air', '-')
    _add_label(fig, 0.07, 0.14,
               ['<b>AIRE DE COMBUSTIÓN</b>',
                f'Flujo: {m_air} t/h',
                f'Temp: {T_amb} °C',
                f'Exc: {exc_air} %'],
               COLORS['stream_air'])

    # Vapor sobrecalentado (derecha arriba)
    m_stm = results.get('m_stm', '-')
    T_stm = results.get('T_stm', '-')
    P_stm = results.get('P_stm', '-')
    Q_stm = results.get('Q_steam', '-')
    h_stm = results.get('h_steam', '-')
    _add_label(fig, 0.92, 0.82,
               ['<b>VAPOR SOBRECALENTADO</b>',
                f'Flujo: {m_stm} t/h',
                f'Temp: {T_stm} °C',
                f'Pres: {P_stm} barg',
                f'h: {h_stm} kJ/kg',
                f'E: {Q_stm} MW'],
               COLORS['stream_steam'], align='right')

    # Purga (derecha medio)
    m_pur = results.get('m_purge', '-')
    T_pur = results.get('T_purge', '-')
    Q_pur = results.get('Q_purge', '-')
    _add_label(fig, 0.92, 0.40,
               ['<b>PURGA CONTINUA</b>',
                f'Flujo: {m_pur} t/h',
                f'Temp: {T_pur} °C',
                f'E: {Q_pur} MW'],
               COLORS['stream_water'], align='right')

    # Gases de combustión (arriba centro-derecha)
    m_flue = results.get('m_flue', '-')
    T_flue = results.get('T_flue', '-')
    Q_flue = results.get('Q_flue', '-')
    _add_label(fig, 0.62, 0.96,
               ['<b>GASES DE COMBUSTIÓN</b>',
                f'Flujo: {m_flue} t/h',
                f'Temp: {T_flue} °C',
                f'E: {Q_flue} MW'],
               COLORS['stream_flue'])

    # Cenizas (abajo centro)
    m_ash = results.get('m_ash', '-')
    _add_label(fig, 0.46, 0.02,
               ['<b>CENIZAS</b>',
                f'Flujo: {m_ash} t/h'],
               '#8B7355')

    # ── LAYOUT ───────────────────────────────────────────────────────────
    fig.update_layout(
        title=dict(
            text='DIAGRAMA DE FLUJO DE PROCESO (PFD) — CALDERA ACUOTUBULAR',
            font=dict(size=14, color=COLORS['text_primary']),
            x=0.5, xanchor='center'),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[-0.02, 1.02], fixedrange=True),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False,
                   range=[-0.02, 1.02], scaleanchor='x', fixedrange=True),
        plot_bgcolor=COLORS['bg_primary'],
        paper_bgcolor=COLORS['bg_primary'],
        height=620,
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(family='Segoe UI, Consolas, sans-serif'),
        showlegend=False,
        dragmode=False,
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
                    'energy': 0,
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
                    'energy': results.get('Q_flue', '-'),
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


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAMA P&ID CON IMAGEN + ETIQUETAS DINÁMICAS
# ═══════════════════════════════════════════════════════════════════════════════

def _stream_label(title, rows, color):
    """Crea una etiqueta de corriente compacta."""
    children = [html.Div(title, style={
        'fontWeight': 'bold', 'fontSize': '11px',
        'textTransform': 'uppercase', 'marginBottom': '4px', 'color': color
    })]
    for row in rows:
        children.append(html.Div(row, style={'fontSize': '10px', 'margin': '1px 0'}))
    return children


def create_pid_image(results: Dict) -> html.Div:
    """
    Crea diagrama PFD usando imagen1.png con etiquetas dinámicas superpuestas.

    Parameters
    ----------
    results : dict
        Resultados del balance

    Returns
    -------
    html.Div
        Componente HTML con imagen + etiquetas posicionadas
    """
    # Estilo base para etiquetas
    label_base = {
        'position': 'absolute',
        'background': 'rgba(30, 30, 30, 0.92)',
        'border': '2px solid',
        'borderRadius': '6px',
        'padding': '6px 10px',
        'fontFamily': 'Consolas, monospace',
        'color': '#FFFFFF',
        'fontSize': '10px',
        'zIndex': '10',
        'whiteSpace': 'nowrap',
    }

    # ── ENTRADAS (izquierda) ─────────────────────────────────────────

    # Agua de alimentación (abajo izquierda, junto a la flecha azul)
    lbl_fw = html.Div(
        _stream_label('AGUA DE ALIMENTACIÓN', [
            f"Flujo: {results.get('m_fw', '-')} t/h",
            f"Temp: {results.get('T_fw', '-')} °C",
            f"E: {results.get('Q_fw', '-')} MW",
        ], COLORS['stream_water']),
        style={**label_base, 'borderColor': COLORS['stream_water'],
               'bottom': '8%', 'left': '1%'})

    # Bagazo (arriba izquierda)
    lbl_bag = html.Div(
        _stream_label('BAGAZO (AR)', [
            f"Flujo: {results.get('m_bagazo', '-')} t/h",
            f"Temp: {results.get('T_amb', '-')} °C",
            f"E: {results.get('Q_fuel', '-')} MW",
        ], COLORS['stream_fuel']),
        style={**label_base, 'borderColor': COLORS['stream_fuel'],
               'top': '18%', 'left': '1%'})

    # Aire de combustión (medio izquierda)
    lbl_air = html.Div(
        _stream_label('AIRE DE COMBUSTIÓN', [
            f"Flujo: {results.get('m_air', '-')} t/h",
            f"Temp: {results.get('T_amb', '-')} °C",
            f"Exc: {results.get('excess_air', '-')} %",
        ], COLORS['stream_air']),
        style={**label_base, 'borderColor': COLORS['stream_air'],
               'top': '48%', 'left': '1%'})

    # ── SALIDAS (derecha) ────────────────────────────────────────────

    # Vapor sobrecalentado (arriba derecha)
    lbl_stm = html.Div(
        _stream_label('VAPOR SOBRECALENTADO', [
            f"Flujo: {results.get('m_stm', '-')} t/h",
            f"Temp: {results.get('T_stm', '-')} °C",
            f"Pres: {results.get('P_stm', '-')} barg",
            f"h: {results.get('h_steam', '-')} kJ/kg",
            f"E: {results.get('Q_steam', '-')} MW",
        ], COLORS['stream_steam']),
        style={**label_base, 'borderColor': COLORS['stream_steam'],
               'top': '18%', 'right': '1%'})

    # Purga continua (medio derecha)
    lbl_pur = html.Div(
        _stream_label('PURGA CONTINUA', [
            f"Flujo: {results.get('m_purge', '-')} t/h",
            f"Temp: {results.get('T_purge', '-')} °C",
            f"E: {results.get('Q_purge', '-')} MW",
        ], COLORS['stream_water']),
        style={**label_base, 'borderColor': COLORS['stream_water'],
               'top': '55%', 'right': '1%'})

    # Gases de combustión (arriba centro)
    lbl_gas = html.Div(
        _stream_label('GASES DE COMBUSTIÓN', [
            f"Flujo: {results.get('m_flue', '-')} t/h",
            f"Temp: {results.get('T_flue', '-')} °C",
            f"E: {results.get('Q_flue', '-')} MW",
        ], COLORS['stream_flue']),
        style={**label_base, 'borderColor': COLORS['stream_flue'],
               'top': '1%', 'left': '35%'})

    # Cenizas (abajo derecha)
    lbl_ash = html.Div(
        _stream_label('CENIZAS Y RESIDUOS', [
            f"Flujo: {results.get('m_ash', '-')} t/h",
        ], '#8B7355'),
        style={**label_base, 'borderColor': '#8B7355',
               'bottom': '3%', 'right': '30%'})

    return html.Div([
        # Título
        html.H4('DIAGRAMA DE FLUJO DE PROCESO (PFD) — CALDERA ACUOTUBULAR',
                 style={'color': COLORS['text_primary'], 'marginBottom': '12px',
                        'textAlign': 'center', 'fontSize': '14px'}),
        # Contenedor con posición relativa
        html.Div([
            html.Img(src='/assets/imagen1.png', style={
                'width': '100%', 'display': 'block', 'borderRadius': '8px'}),
            lbl_fw, lbl_bag, lbl_air,
            lbl_stm, lbl_pur, lbl_gas, lbl_ash,
        ], style={
            'position': 'relative',
            'maxWidth': '1000px',
            'margin': '0 auto',
        })
    ], style={
        'background': COLORS['bg_secondary'],
        'border': f'1px solid {COLORS["border"]}',
        'borderRadius': '12px',
        'padding': '16px',
    })
