"""
Tema Claro - Light Theme
=========================
Estilos para el modo claro.

DML INGENIEROS CONSULTORES S.A.S.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# COLORES PRINCIPALES
# ═══════════════════════════════════════════════════════════════════════════════

COLORS = {
    # Background
    'bg_primary': '#FFFFFF',      # Fondo principal
    'bg_secondary': '#F5F5F5',    # Fondo secundario
    'bg_tertiary': '#FAFAFA',     # Fondo terciario (cards)
    'bg_hover': '#E8E8E8',        # Hover

    # Texto
    'text_primary': '#1A1A1A',    # Texto principal
    'text_secondary': '#555555',  # Texto secundario
    'text_muted': '#999999',      # Texto deshabilitado
    'text_inverse': '#FFFFFF',    # Texto invertido

    # Acentos
    'accent': '#0078D4',          # Azul Windows 11
    'accent_hover': '#005A9E',    # Azul hover
    'accent_light': '#4CC2FF',    # Azul claro

    # Estados
    'success': '#107C10',         # Verde
    'warning': '#FF8C00',         # Naranja
    'error': '#E81123',           # Rojo
    'info': '#0078D4',            # Azul info

    # Bordes
    'border': '#E0E0E0',          # Borde normal
    'border_light': '#F0F0F0',    # Borde claro

    # Gráficos
    'chart_bg': '#FFFFFF',
    'chart_grid': '#E8E8E8',
    'chart_text': '#555555',
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
        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
        'height': '100%',
    }


def get_kpi_card_style() -> dict:
    """Estilo para tarjetas KPI."""
    return {
        'background': f'linear-gradient(135deg, {COLORS["bg_tertiary"]} 0%, {COLORS["bg_secondary"]} 100%)',
        'border': f"2px solid {COLORS['accent']}",
        'borderRadius': '12px',
        'padding': '24px',
        'textAlign': 'center',
        'boxShadow': '0 4px 16px rgba(0,120,212,0.15)',
        'height': '100%',
        'transition': 'all 0.3s ease',
    }


def get_input_style() -> dict:
    """Estilo para inputs."""
    return {
        'backgroundColor': COLORS['bg_primary'],
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
            'color': COLORS['text_inverse'],
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
        'backgroundColor': COLORS['bg_primary'],
        'borderBottom': f"2px solid {COLORS['accent']}",
        'padding': '12px 24px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
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
            'bgcolor': COLORS['bg_primary'],
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
    """Retorna un color según el valor (para semáforo)."""
    if thresholds is None:
        return COLORS['accent']

    if value >= thresholds.get('error', float('inf')):
        return COLORS['error']
    elif value >= thresholds.get('warning', float('inf')):
        return COLORS['warning']
    else:
        return COLORS['success']


def get_color_palette(n: int = None) -> list:
    """Retorna una paleta de colores."""
    if n is None:
        return CHART_COLORS
    return (CHART_COLORS * ((n // len(CHART_COLORS)) + 1))[:n]
