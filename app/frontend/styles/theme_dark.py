"""
Tema Oscuro - Dark Theme
=========================
Estilos para el modo oscuro tipo Windows 11.

DML INGENIEROS CONSULTORES S.A.S.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# COLORES PRINCIPALES
# ═══════════════════════════════════════════════════════════════════════════════

COLORS = {
    # Background
    'bg_primary': '#1E1E1E',      # Fondo principal
    'bg_secondary': '#252526',    # Fondo secundario
    'bg_tertiary': '#2D2D30',     # Fondo terciario (cards)
    'bg_hover': '#3E3E42',        # Hover

    # Texto
    'text_primary': '#FFFFFF',    # Texto principal
    'text_secondary': '#CCCCCC',  # Texto secundario
    'text_muted': '#808080',      # Texto deshabilitado
    'text_inverse': '#000000',    # Texto invertido

    # Acentos
    'accent': '#0078D4',          # Azul Windows 11
    'accent_hover': '#106EBE',    # Azul hover
    'accent_light': '#4CC2FF',    # Azul claro

    # Estados
    'success': '#107C10',         # Verde
    'warning': '#FF8C00',         # Naranja
    'error': '#E81123',           # Rojo
    'info': '#0078D4',            # Azul info

    # Bordes
    'border': '#3E3E42',          # Borde normal
    'border_light': '#4C4C4C',    # Borde claro

    # Gráficos
    'chart_bg': '#1E1E1E',
    'chart_grid': '#3E3E42',
    'chart_text': '#CCCCCC',
}


# ═══════════════════════════════════════════════════════════════════════════════
# ESTILOS DE COMPONENTES
# ═══════════════════════════════════════════════════════════════════════════════

def get_card_style() -> dict:
    """Estilo para tarjetas."""
    return {
        'backgroundColor': COLORS['bg_tertiary'],
        'border': f"1px solid {COLORS['border']}",
        'borderRadius': '8px',
        'padding': '20px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.3)',
        'height': '100%',
    }


def get_kpi_card_style() -> dict:
    """Estilo para tarjetas KPI."""
    return {
        'background': f'linear-gradient(135deg, {COLORS["bg_tertiary"]} 0%, {COLORS["bg_secondary"]} 100%)',
        'border': f"1px solid {COLORS['accent']}",
        'borderRadius': '12px',
        'padding': '24px',
        'textAlign': 'center',
        'boxShadow': '0 4px 16px rgba(0,120,212,0.2)',
        'height': '100%',
        'transition': 'all 0.3s ease',
    }


def get_input_style() -> dict:
    """Estilo para inputs."""
    return {
        'backgroundColor': COLORS['bg_secondary'],
        'color': COLORS['text_primary'],
        'border': f"1px solid {COLORS['border']}",
        'borderRadius': '6px',
        'padding': '8px 12px',
    }


def get_button_style(accent: bool = True) -> dict:
    """Estilo para botones."""
    if accent:
        return {
            'backgroundColor': COLORS['accent'],
            'color': COLORS['text_primary'],
            'border': 'none',
            'borderRadius': '6px',
            'padding': '10px 24px',
            'fontWeight': '600',
            'cursor': 'pointer',
            'transition': 'all 0.2s ease',
        }
    else:
        return {
            'backgroundColor': COLORS['bg_tertiary'],
            'color': COLORS['text_primary'],
            'border': f"1px solid {COLORS['border']}",
            'borderRadius': '6px',
            'padding': '10px 24px',
            'cursor': 'pointer',
            'transition': 'all 0.2s ease',
        }


def get_header_style() -> dict:
    """Estilo para el encabezado."""
    return {
        'backgroundColor': COLORS['bg_secondary'],
        'borderBottom': f"2px solid {COLORS['accent']}",
        'padding': '12px 24px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.3)',
    }


def get_sidebar_style() -> dict:
    """Estilo para la barra lateral."""
    return {
        'backgroundColor': COLORS['bg_secondary'],
        'borderRight': f"1px solid {COLORS['border']}",
        'padding': '20px',
        'height': '100vh',
        'overflowY': 'auto',
    }


def get_content_style() -> dict:
    """Estilo para el área de contenido."""
    return {
        'backgroundColor': COLORS['bg_primary'],
        'padding': '24px',
        'height': '100vh',
        'overflowY': 'auto',
    }


# ═══════════════════════════════════════════════════════════════════════════════
# COLORES PARA GRÁFICOS PLOTLY
# ═══════════════════════════════════════════════════════════════════════════════

PLOTLY_TEMPLATE = {
    'layout': {
        'paper_bgcolor': COLORS['bg_primary'],
        'plot_bgcolor': COLORS['bg_primary'],
        'font': {
            'color': COLORS['text_primary'],
            'family': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
        },
        'title': {
            'font': {'color': COLORS['text_primary'], 'size': 18},
        },
        'xaxis': {
            'gridcolor': COLORS['chart_grid'],
            'linecolor': COLORS['border'],
            'tickfont': {'color': COLORS['chart_text']},
            'titlefont': {'color': COLORS['text_secondary']},
        },
        'yaxis': {
            'gridcolor': COLORS['chart_grid'],
            'linecolor': COLORS['border'],
            'tickfont': {'color': COLORS['chart_text']},
            'titlefont': {'color': COLORS['text_secondary']},
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

# Colores para series de datos
CHART_COLORS = [
    COLORS['accent'],        # Azul
    COLORS['success'],       # Verde
    COLORS['warning'],       # Naranja
    COLORS['error'],         # Rojo
    '#9B59B6',               # Púrpura
    '#1ABC9C',               # Turquesa
    '#F39C12',               # Amarillo
    '#E74C3C',               # Coral
]


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE UTILIDAD
# ═══════════════════════════════════════════════════════════════════════════════

def get_color_for_value(value: float, thresholds: dict = None) -> str:
    """
    Retorna un color según el valor (para semáforo).

    Parameters
    ----------
    value : float
        Valor a evaluar
    thresholds : dict, opcional
        Diccionario con umbrales {'warning': X, 'error': Y}

    Returns
    -------
    str
        Color hexadecimal
    """
    if thresholds is None:
        return COLORS['accent']

    if value >= thresholds.get('error', float('inf')):
        return COLORS['error']
    elif value >= thresholds.get('warning', float('inf')):
        return COLORS['warning']
    else:
        return COLORS['success']


def get_color_palette(n: int = None) -> list:
    """
    Retorna una paleta de colores.

    Parameters
    ----------
    n : int, opcional
        Número de colores requeridos

    Returns
    -------
    list
        Lista de colores hexadecimales
    """
    if n is None:
        return CHART_COLORS
    return (CHART_COLORS * ((n // len(CHART_COLORS)) + 1))[:n]
