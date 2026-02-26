"""
Componente Charts - Gráficos Plotly Interactivos
=================================================
Gráficos interactivos para visualización de resultados.

DML INGENIEROS CONSULTORES S.A.S.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import List, Dict, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE ESTILOS
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
    'grid': '#3E3E42',
    'border': '#4C4C4C',
}

TEMPLATE = {
    'layout': {
        'paper_bgcolor': COLORS['bg_primary'],
        'plot_bgcolor': COLORS['bg_primary'],
        'font': {
            'color': COLORS['text_primary'],
            'family': 'Segoe UI, sans-serif',
        },
        'xaxis': {
            'gridcolor': COLORS['grid'],
            'linecolor': COLORS['border'],
            'tickfont': {'color': COLORS['text_secondary']},
            'title': {'font': {'color': COLORS['text_primary']}},
        },
        'yaxis': {
            'gridcolor': COLORS['grid'],
            'linecolor': COLORS['border'],
            'tickfont': {'color': COLORS['text_secondary']},
            'title': {'font': {'color': COLORS['text_primary']}},
        },
        'legend': {
            'bgcolor': COLORS['bg_secondary'],
            'bordercolor': COLORS['border'],
            'font': {'color': COLORS['text_primary']},
        },
        'hovermode': 'closest',
        'margin': {'l': 60, 'r': 30, 't': 50, 'b': 60},
    }
}


# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO DE CURVA VAPOR/BAGAZO VS CENIZAS
# ═══════════════════════════════════════════════════════════════════════════════

def create_ratio_vs_ash_curve(base_params: dict, ash_range: Tuple[float, float] = (1, 15)) -> go.Figure:
    """
    Crea gráfico de Ratio vs % Cenizas.

    Parameters
    ----------
    base_params : dict
        Parámetros base para el cálculo
    ash_range : tuple
        Rango de cenizas (min, max) [%]

    Returns
    -------
    go.Figure
        Gráfico Plotly
    """
    # Generar puntos para la curva
    ash_values = np.linspace(ash_range[0], ash_range[1], 50)
    ratio_values = []

    for ash in ash_values:
        # Simplificación: ratio decreases as ash increases
        # Usar correlación basada en los datos del proyecto
        base_ratio = 2.655  # Para 10% cenizas, 48% humedad
        base_ash = 10.0

        # Ajuste empírico
        ratio = base_ratio * (base_ash / ash) ** 0.3
        ratio_values.append(ratio)

    # Crear gráfico
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ash_values,
        y=ratio_values,
        mode='lines+markers',
        name='Ratio Vapor/Bagazo',
        line=dict(color=COLORS['accent'], width=3),
        marker=dict(size=6, color=COLORS['accent']),
        hovertemplate='<b>%Cenizas: %{x:.1f}%</b><br>Ratio: %{y:.3f} t/t<extra></extra>'
    ))

    # Marcar punto actual
    current_ash = base_params.get('bagazo_ash', 10)
    current_ratio = base_params.get('ratio', 2.655)

    fig.add_trace(go.Scatter(
        x=[current_ash],
        y=[current_ratio],
        mode='markers',
        name='Actual',
        marker=dict(size=15, color=COLORS['warning'], symbol='diamond',
                    line=dict(width=2, color=COLORS['text_primary'])),
        hovertemplate='<b>Actual</b><br>Cenizas: %{x:.1f}%<br>Ratio: %{y:.3f} t/t<extra></extra>'
    ))

    # Layout
    fig.update_layout(
        title=dict(
            text='VARIACIÓN DEL RATIO VAPOR/BAGAZO CON % CENIZAS',
            font=dict(size=16, color=COLORS['text_primary'])
        ),
        xaxis=dict(
            title_text='% Cenizas del Bagazo',
            range=[ash_range[0] - 1, ash_range[1] + 1]
        ),
        yaxis=dict(
            title_text='Ratio Vapor/Bagazo [t_vapor/t_bagazo]'
        ),
        template=TEMPLATE,
        height=350,
        hovermode='x unified'
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO DE CURVA VAPOR/BAGAZO VS EFICIENCIA
# ═══════════════════════════════════════════════════════════════════════════════

def create_ratio_vs_efficiency_curve(base_params: dict,
                                      eff_range: Tuple[float, float] = (50, 95)) -> go.Figure:
    """
    Crea gráfico de Ratio vs % Eficiencia.

    Parameters
    ----------
    base_params : dict
        Parámetros base
    eff_range : tuple
        Rango de eficiencia (min, max) [%]

    Returns
    -------
    go.Figure
        Gráfico Plotly
    """
    eff_values = np.linspace(eff_range[0], eff_range[1], 50)
    ratio_values = []

    base_ratio = 2.655  # Para 94% eficiencia
    base_eff = 94.0

    for eff in eff_values:
        # Ratio es proporcional a la eficiencia
        # (menor eficiencia = más bagazo = menor ratio)
        ratio = base_ratio * (eff / base_eff)
        ratio_values.append(ratio)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=eff_values,
        y=ratio_values,
        mode='lines+markers',
        name='Ratio Vapor/Bagazo',
        line=dict(color=COLORS['success'], width=3),
        marker=dict(size=6, color=COLORS['success']),
        hovertemplate='<b>Eficiencia: %{x:.1f}%</b><br>Ratio: %{y:.3f} t/t<extra></extra>'
    ))

    # Marcar punto actual
    current_eff = base_params.get('efficiency', 94)
    current_ratio = base_params.get('ratio', 2.655)

    fig.add_trace(go.Scatter(
        x=[current_eff],
        y=[current_ratio],
        mode='markers',
        name='Actual',
        marker=dict(size=15, color=COLORS['warning'], symbol='diamond',
                    line=dict(width=2, color=COLORS['text_primary'])),
        hovertemplate='<b>Actual</b><br>Eficiencia: %{x:.1f}%<br>Ratio: %{y:.3f} t/t<extra></extra>'
    ))

    # Zona óptima (85-95%)
    fig.add_vrect(
        x0=85, x1=95,
        fillcolor="rgba(16, 124, 16, 0.1)",
        layer="below", line_width=0,
        annotation_text="Zona Óptima"
    )

    fig.update_layout(
        title=dict(
            text='VARIACIÓN DEL RATIO VAPOR/BAGAZO CON EFICIENCIA',
            font=dict(size=16, color=COLORS['text_primary'])
        ),
        xaxis=dict(title_text='Eficiencia Térmica [%]'),
        yaxis=dict(title_text='Ratio Vapor/Bagazo [t_vapor/t_bagazo]'),
        template=TEMPLATE,
        height=350,
        hovermode='x unified'
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO DE COMPOSICIÓN DE GASES
# ═══════════════════════════════════════════════════════════════════════════════

def create_flue_gas_composition(composition: dict) -> go.Figure:
    """
    Crea gráfico de torta con composición de gases.

    Parameters
    ----------
    composition : dict
        Diccionario con composición de gases
        {CO2: %, H2O: %, N2: %, O2: %, SO2: %}

    Returns
    -------
    go.Figure
        Gráfico Plotly
    """
    components = ['CO2', 'H2O', 'N2', 'O2', 'SO2']
    values = [composition.get(c, 0) for c in components]
    pie_colors = ['#808080', '#0078D4', '#A0A0A0', '#FF8C00', '#E81123']

    fig = go.Figure(data=[
        go.Pie(
            labels=components,
            values=values,
            marker=dict(colors=pie_colors, line=dict(color='#1E1E1E', width=2)),
            textinfo='label+percent',
            textfont=dict(size=13, color='#FFFFFF'),
            hovertemplate='%{label}: %{value:.1f}%<extra></extra>',
            hole=0.3,
        )
    ])

    fig.update_layout(
        title=dict(
            text='COMPOSICIÓN DE GASES DE COMBUSTIÓN',
            font=dict(size=16, color=COLORS['text_primary'])
        ),
        template=TEMPLATE,
        height=350,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.1,
            xanchor='center',
            x=0.5,
            font=dict(color=COLORS['text_secondary'])
        )
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAMA SANKEY - BALANCE DE ENERGÍA
# ═══════════════════════════════════════════════════════════════════════════════

def create_energy_sankey(energy_data: dict) -> go.Figure:
    """
    Crea diagrama Sankey del balance de energía.

    Parameters
    ----------
    energy_data : dict
        Diccionario con flujos de energía
        {
            Q_fw: energía agua alimentación [MW],
            Q_fuel: energía combustible [MW],
            Q_steam: energía vapor [MW],
            Q_purge: energía purga [MW],
            losses: pérdidas [MW]
        }

    Returns
    -------
    go.Figure
        Gráfico Sankey Plotly
    """
    # Nodos
    nodes = [
        'Agua Alimentación',
        'Bagazo (Combustible)',
        'Caldera',
        'Vapor Sobrecalentado',
        'Purga Continua',
        'Pérdidas'
    ]

    # Colores por nodo
    node_colors = [
        COLORS['accent'],     # Agua (azul)
        COLORS['warning'],    # Bagazo (naranja)
        COLORS['text_secondary'],  # Caldera (gris)
        COLORS['success'],    # Vapor (verde)
        COLORS['accent'],     # Purga (azul)
        COLORS['error'],      # Pérdidas (rojo)
    ]

    # Valores [origen, destino, valor]
    Q_fw = energy_data.get('Q_fw', 33.6)
    Q_fuel = energy_data.get('Q_fuel', 68.1)
    Q_steam = energy_data.get('Q_steam', 96.7)
    Q_purge = energy_data.get('Q_purge', 0.82)
    losses = energy_data.get('losses', 4.09)

    source = [0, 1, 2, 2, 2]  # Orígenes
    target = [2, 2, 3, 4, 5]  # Destinos
    value = [Q_fw, Q_fuel, Q_steam, Q_purge, losses]  # Valores [MW]

    # Etiquetas para los enlaces
    link_labels = [
        f'{Q_fw:.1f} MW',
        f'{Q_fuel:.1f} MW',
        f'{Q_steam:.1f} MW',
        f'{Q_purge:.2f} MW',
        f'{losses:.2f} MW'
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color=COLORS['border'], width=0.5),
            label=nodes,
            color=node_colors,
            customdata=[Q_fw, Q_fuel, Q_fw + Q_fuel, Q_steam, Q_purge, losses],
            hovertemplate='%{label}<br>Energía: %{customdata:.2f} MW<extra></extra>'
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            label=link_labels,
            color=[
                f'rgba(0, 120, 212, 0.3)',
                f'rgba(255, 140, 0, 0.3)',
                f'rgba(16, 124, 16, 0.3)',
                f'rgba(0, 120, 212, 0.3)',
                f'rgba(232, 17, 35, 0.3)',
            ],
            hovertemplate='%{label}<extra></extra>'
        )
    )])

    fig.update_layout(
        title=dict(
            text='BALANCE DE ENERGÍA - DIAGRAMA SANKEY [MW]',
            font=dict(size=16, color=COLORS['text_primary'])
        ),
        font=dict(size=12, color=COLORS['text_primary']),
        template=TEMPLATE,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICO DE COMPARACIÓN DE RESULTADOS
# ═══════════════════════════════════════════════════════════════════════════════

def create_results_comparison(calculated: dict, expected: dict = None) -> go.Figure:
    """
    Crea gráfico de barras comparando calculado vs esperado.

    Parameters
    ----------
    calculated : dict
        Valores calculados
    expected : dict
        Valores esperados (base)

    Returns
    -------
    go.Figure
        Gráfico de comparación
    """
    if expected is None:
        expected = {
            'ratio': 2.655,
            'm_bagazo': 37.67,
            'Q_abs': 64.01,
            'Q_fuel': 68.10
        }

    metrics = ['Ratio\n[t/t]', 'Bagazo\n[t/h]', 'Q_abs\n[MW]', 'Q_fuel\n[MW]']
    calc_values = [
        calculated.get('ratio', 0),
        calculated.get('m_bagazo', 0),
        calculated.get('Q_abs', 0),
        calculated.get('Q_fuel', 0)
    ]
    exp_values = [
        expected.get('ratio', 0),
        expected.get('m_bagazo', 0),
        expected.get('Q_abs', 0),
        expected.get('Q_fuel', 0)
    ]

    fig = go.Figure(data=[
        go.Bar(
            name='Calculado',
            x=metrics,
            y=calc_values,
            marker_color=COLORS['accent'],
            text=[f'{v:.2f}' for v in calc_values],
            textposition='outside',
        ),
        go.Bar(
            name='Esperado (Base)',
            x=metrics,
            y=exp_values,
            marker_color=COLORS['success'],
            text=[f'{v:.2f}' for v in exp_values],
            textposition='outside',
        )
    ])

    fig.update_layout(
        title=dict(
            text='VALIDACIÓN DE RESULTADOS',
            font=dict(size=16, color=COLORS['text_primary'])
        ),
        xaxis=dict(title_text=''),
        yaxis=dict(title_text='Valor'),
        barmode='group',
        template=TEMPLATE,
        height=350,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    return fig
