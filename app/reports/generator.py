"""
Generador de Reportes PDF
===========================
Genera reportes PDF con los resultados del balance.

DML INGENIEROS CONSULTORES S.A.S.
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from typing import Dict
import os


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

COLORS = {
    'dml_blue': colors.HexColor('#0078D4'),
    'dml_dark': colors.HexColor('#1E1E1E'),
    'gray_light': colors.HexColor('#CCCCCC'),
    'gray_medium': colors.HexColor('#808080'),
    'success': colors.HexColor('#107C10'),
    'warning': colors.HexColor('#FF8C00'),
}


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

class ReportGenerator:
    """Generador de reportes PDF para cálculos de caldera."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        self.story = []

    def _setup_styles(self):
        """Configura estilos personalizados."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='TitleMain',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=COLORS['dml_blue'],
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=COLORS['dml_dark'],
            spaceAfter=10,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Encabezado de sección
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=COLORS['dml_blue'],
            spaceBefore=12,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))

        # Normal justificado
        self.styles.add(ParagraphStyle(
            name='BodyJustified',
            parent=self.styles['BodyText'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        ))

        # Celda de tabla
        self.styles.add(ParagraphStyle(
            name='CellText',
            parent=self.styles['BodyText'],
            fontSize=9,
            alignment=TA_CENTER
        ))

        # KPI grande
        self.styles.add(ParagraphStyle(
            name='KPIValue',
            parent=self.styles['BodyText'],
            fontSize=24,
            textColor=COLORS['dml_blue'],
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

    def _add_header(self, project_code: str, document_code: str, analyst: str):
        """Agrega el encabezado del reporte."""
        header_data = [
            [
                Paragraph('<b>DML INGENIEROS CONSULTORES S.A.S.</b>', self.styles['BodyText']),
                Paragraph(f'<b>CÓDIGO:</b> {project_code}', self.styles['BodyText']),
            ],
            [
                Paragraph('Memoria de Cálculo - Caldera Acuotubular', self.styles['BodyText']),
                Paragraph(f'<b>DOCUMENTO:</b> {document_code}', self.styles['BodyText']),
            ],
            [
                Paragraph(f'<b>ANALISTA:</b> {analyst}', self.styles['BodyText']),
                Paragraph(f'<b>FECHA:</b> {datetime.now().strftime("%Y-%m-%d")}', self.styles['BodyText']),
            ],
        ]

        header_table = Table(header_data, colWidths=[10*cm, 6*cm])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLORS['dml_blue']),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))

        self.story.append(header_table)
        self.story.append(Spacer(1, 1*cm))

    def _add_title(self, title: str):
        """Agrega un título al documento."""
        self.story.append(Paragraph(title, self.styles['TitleMain']))

    def _add_section(self, title: str):
        """Agrega un encabezado de sección."""
        self.story.append(Paragraph(title, self.styles['SectionHeader']))

    def _add_kpi_card(self, title: str, value: str, unit: str = ''):
        """Agrega una tarjeta de KPI."""
        data = [
            [Paragraph(title, self.styles['BodyText'])],
            [Paragraph(f'{value} {unit}', self.styles['KPIValue'])],
        ]

        table = Table(data, colWidths=[5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('BORDER', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        self.story.append(table)

    def _add_table(self, headers: list, rows: list, col_widths: list = None):
        """Agrega una tabla al documento."""
        data = [headers] + rows

        if col_widths is None:
            col_widths = [None] * len(headers)

        table = Table(data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['dml_blue']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))

        self.story.append(table)

    def generate(self, results: Dict, metadata: Dict, output_path: str):
        """
        Genera el reporte PDF completo.

        Parameters
        ----------
        results : dict
            Resultados del balance
        metadata : dict
            Metadatos del proyecto (project_code, document_code, analyst)
        output_path : str
            Ruta del archivo PDF de salida
        """
        # Crear documento
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        # Limpiar story
        self.story = []

        # Encabezado
        self._add_header(
            metadata.get('project_code', 'P2807'),
            metadata.get('document_code', 'P2807-PR-MC-001'),
            metadata.get('analyst', '')
        )

        # Título
        self._add_title('BALANCE DE MATERIA Y ENERGÍA')
        self._add_title('CALDERA AQUOTUBULAR DE COGENERACIÓN')
        self.story.append(Spacer(1, 0.5*cm))

        # KPI Principal
        self._add_section('RESULTADO PRINCIPAL')
        self._add_kpi_card(
            'RATIO VAPOR / BAGAZO',
            f"{results.get('ratio', 0):.3f}",
            't_vapor/t_bagazo'
        )
        self.story.append(Spacer(1, 0.5*cm))

        # KPIs Secundarios
        kpi_data = [
            ['Parámetro', 'Valor', 'Unidad'],
            ['Flujo de Vapor', f"{results.get('m_stm', 0):.2f}", 't/h'],
            ['Flujo de Bagazo', f"{results.get('m_bagazo', 0):.2f}", 't/h'],
            ['Flujo Agua Alim.', f"{results.get('m_fw', 0):.2f}", 't/h'],
            ['Flujo Purga', f"{results.get('m_purge', 0):.2f}", 't/h'],
            ['Calor Absorbido', f"{results.get('Q_abs', 0):.2f}", 'MW'],
            ['Calor Combustible', f"{results.get('Q_fuel', 0):.2f}", 'MW'],
        ]
        self._add_table(kpi_data[0], kpi_data[1:])

        self.story.append(Spacer(1, 0.5*cm))

        # Tabla de Balance
        self._add_section('BALANCE DE MATERIA Y ENERGÍA')
        balance_data = [
            ['Tipo', 'Corriente', 'Flujo [t/h]', 'T [°C]', 'Energía [MW]'],
            ['ENTRADA', 'Agua de Alimentación', f"{results.get('m_fw', 0):.2f}",
             f"{results.get('T_fw', 0):.1f}", f"{results.get('Q_fw', 0):.2f}"],
            ['ENTRADA', 'Bagazo (AR)', f"{results.get('m_bagazo', 0):.2f}",
             f"{results.get('T_amb', 0):.1f}", f"{results.get('Q_fuel', 0):.2f}"],
            ['ENTRADA', 'Aire de Combustión', f"{results.get('m_air', 0):.2f}",
             f"{results.get('T_amb', 0):.1f}", '-'],
            ['', '', '', '', ''],
            ['SALIDA', 'Vapor Sobrecalentado', f"{results.get('m_stm', 0):.2f}",
             f"{results.get('T_stm', 0):.1f}", f"{results.get('Q_steam', 0):.2f}"],
            ['SALIDA', 'Purga Continua', f"{results.get('m_purge', 0):.2f}",
             f"{results.get('T_purge', 0):.1f}", f"{results.get('Q_purge', 0):.2f}"],
            ['SALIDA', 'Gases de Combustión', f"{results.get('m_flue', 0):.2f}",
             f"{results.get('T_flue', 0):.1f}", 'Pérdidas'],
        ]
        self._add_table(balance_data[0], balance_data[1:])

        self.story.append(Spacer(1, 0.5*cm))

        # Conclusión
        self._add_section('CONCLUSIÓN')
        conclusion_text = f"""
        El cálculo del balance de materia y energía para la caldera acuotubular
        arrojó un ratio Vapor/Bagazo de {results.get('ratio', 0):.3f} t_vapor/t_bagazo.
        Este valor se encuentra dentro del rango esperado para calderas bagaceras
        operando con las condiciones especificadas.
        """
        self.story.append(Paragraph(conclusion_text.strip(), self.styles['BodyJustified']))

        # Pie de página
        self.story.append(Spacer(1, 2*cm))
        footer_text = f"""
        <b>DML INGENIEROS CONSULTORES S.A.S.</b>
        <br/>
        Tel: 661 24 08 | Email: administrativo@dmlsas.com.co | Cali - Colombia
        """
        self.story.append(Paragraph(footer_text.strip(), self.styles['BodyText']))

        # Construir PDF
        doc.build(self.story)

        return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN DE UTILIDAD
# ═══════════════════════════════════════════════════════════════════════════════

def generate_report(results: Dict, metadata: Dict, output_path: str = None) -> str:
    """
    Genera un reporte PDF con los resultados.

    Parameters
    ----------
    results : dict
        Resultados del balance
    metadata : dict
        Metadatos del proyecto
    output_path : str, opcional
        Ruta de salida (si es None, usa un nombre por defecto)

    Returns
    -------
    str
        Ruta del PDF generado
    """
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"reporte_caldera_{timestamp}.pdf"

    generator = ReportGenerator()
    generator.generate(results, metadata, output_path)

    return output_path


if __name__ == "__main__":
    # Prueba de generación
    test_results = {
        'ratio': 2.655,
        'm_stm': 100.0,
        'm_bagazo': 37.67,
        'm_fw': 102.04,
        'm_purge': 2.04,
        'm_air': 150.5,
        'm_flue': 180.3,
        'T_fw': 270.0,
        'T_stm': 545.0,
        'T_purge': 318.0,
        'T_flue': 160.0,
        'T_amb': 30.0,
        'P_stm': 106.0,
        'Q_fw': 33.6,
        'Q_steam': 96.7,
        'Q_purge': 0.82,
        'Q_fuel': 68.1,
        'Q_abs': 64.01,
    }

    test_metadata = {
        'project_code': 'P2807',
        'document_code': 'P2807-PR-MC-001',
        'analyst': 'Ing. Juan Pérez'
    }

    path = generate_report(test_results, test_metadata, "test_report.pdf")
    print(f"Reporte generado: {path}")
