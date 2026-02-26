"""
Componente Modal para PDF
=========================
Muestra el PDF en una ventana emergente.

DML INGENIEROS CONSULTORES S.A.S.
"""

import dash.html as html


def create_pdf_modal():
    """Crea un componente modal para mostrar el PDF."""
    return html.Div([
        # Fondo oscuro
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

        # Contenido del modal
        html.Div([
            html.Div([
                html.H4('REPORTE PDF', style={
                    'color': '#FFFFFF',
                    'margin': '0 0 15px 0'
                }),

                # Contenedor del PDF
                html.Div(
                    html.Iframe(
                        id='pdf-preview-frame',
                        style={
                            'width': '100%',
                            'height': '500px',
                            'border': 'none',
                            'borderRadius': '8px'
                        }
                    ),
                    style={
                        'background': '#FFFFFF',
                        'borderRadius': '8px',
                        'padding': '10px'
                    }
                ),

                # Botón cerrar
                html.Div([
                    html.Button(
                        'Cerrar',
                        id='btn-close-pdf-modal',
                        n_clicks=0,
                        style={
                            'background': '#0078D4',
                            'color': '#FFFFFF',
                            'border': 'none',
                            'borderRadius': '6px',
                            'padding': '8px 20px',
                            'cursor': 'pointer'
                        }
                    )
                ], style={'textAlign': 'center', 'marginTop': '15px'}),
            ], style={
                'background': '#252526',
                'padding': '20px',
                'borderRadius': '12px',
                'maxWidth': '700px',
                'margin': '0 auto'
            })
        ], style={
            'position': 'fixed',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'zIndex': '9999',
            'display': 'none'
        })
    ], id='pdf-modal')
