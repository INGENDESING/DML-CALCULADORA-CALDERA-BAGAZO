"""
Generador de Reporte PDF
=========================
Módulo para generar reportes en PDF desde los resultados del balance.

DML INGENIEROS CONSULTORES S.A.S.
"""

import io
from datetime import datetime
from typing import Dict, Optional

# Intentar importar librerías PDF
try:
    from reportlab.lib.pagesizes import A4, letter
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_pdf_report(results: Dict, inputs: Dict, filename: str = None) -> Optional[bytes]:
    """
    Genera un reporte PDF con los resultados del balance.

    Parameters
    ----------
    results : dict
        Resultados del balance
    inputs : dict
        Inputs del usuario
    filename : str, opcional
        Nombre del archivo para guardar

    Returns
    -------
    bytes or None
        Contenido del PDF en bytes, o None si hay error
    """
    if not REPORTLAB_AVAILABLE:
        return None

    # Crear buffer
    buffer = io.BytesIO()

    # Crear documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Elementos del documento
    elements = []

    # Estilos
    styles = getSampleStyleSheet()

    # Estilo personalizado para título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0078D4'),
        alignment=TA_CENTER,
        spaceAfter=0.5*cm
    )

    # Estilo para subtítulo
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#333333'),
        alignment=TA_LEFT,
        spaceAfter=0.3*cm
    )

    # Encabezado
    elements.append(Paragraph("DML INGENIEROS CONSULTORES S.A.S.", ParagraphStyle(
        'Company', parent=styles['Normal'], fontSize=10, textColor=colors.gray, alignment=TA_CENTER
    )))
    elements.append(Spacer(0.5*cm, 0.5*cm))

    elements.append(Paragraph("CALCULADORA DE CALDERA ACUOTUBULAR", title_style))
    elements.append(Paragraph("Reporte de Balance de Materia y Energía", styles['Normal']))
    elements.append(Spacer(0.5*cm, 0.5*cm))

    # Fecha
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"<b>Fecha:</b> {fecha}", styles['Normal']))
    elements.append(Spacer(0.5*cm, 0.5*cm))

    # ==================== DATOS DE ENTRADA ====================
    elements.append(Paragraph("DATOS DE ENTRADA", subtitle_style))

    input_data = [
        ["Parámetro", "Valor", "Unidad"],
        ["Flujo de vapor", f"{inputs.get('m_stm', '-')}", "t/h"],
        ["Presión de vapor", f"{inputs.get('P_stm', '-')}", "barg"],
        ["Temperatura vapor", f"{inputs.get('T_stm', '-')}", "°C"],
        ["Temperatura agua alim.", f"{inputs.get('T_fw', '-')}", "°C"],
        ["Purga continua", f"{inputs.get('pct_purge', '-')}", "%"],
        ["Eficiencia térmica", f"{inputs.get('efficiency', '-')}", "%"],
        ["Humedad bagazo", f"{inputs.get('bagazo_humidity', '-')}", "%"],
        ["Cenizas bagazo", f"{inputs.get('bagazo_ash', '-')}", "%"],
        ["Altitud", f"{inputs.get('altitude', '-')}", "msnm"],
        ["Humedad relativa", f"{inputs.get('RH', '-')}", "%"],
        ["Temperatura ambiente", f"{inputs.get('T_amb', '-')}", "°C"],
        ["Exceso de aire", f"{inputs.get('excess_air', '-')}", "%"],
    ]

    input_table = Table(input_data, colWidths=[5*cm, 3*cm, 2*cm])
    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0078D4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
    ]))
    elements.append(input_table)
    elements.append(Spacer(0.5*cm, 0.5*cm))

    # ==================== RESULTADOS PRINCIPALES ====================
    elements.append(Paragraph("RESULTADOS PRINCIPALES", subtitle_style))

    # KPI del ratio con formato especial
    ratio = results.get('ratio', 0)
    target = 2.655
    deviation = ((ratio - target) / target) * 100

    ratio_color = colors.green if abs(deviation) <= 2 else (colors.orange if abs(deviation) <= 5 else colors.red)

    ratio_data = [
        ["Indicador", "Valor", "Referencia"],
        ["Ratio Vapor/Bagazo", f"{ratio:.3f} t/t", f"{target:.3f} t/t"],
        ["Desviación", f"{deviation:+.1f}%", "±2%"],
        ["Estado", "DENTRO DE TOLERANCIA" if abs(deviation) <= 2 else "FUERA DE TOLERANCIA", ""],
    ]

    ratio_table = Table(ratio_data, colWidths=[5*cm, 3*cm, 3*cm])
    ratio_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0078D4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (0, -1), ratio_color),
        ('TEXTCOLOR', (0, 1), (0, -1), colors.white),
        ('BACKGROUND', (1, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
    ]))
    elements.append(ratio_table)
    elements.append(Spacer(0.5*cm, 0.5*cm))

    # ==================== BALANCE DE MATERIA ====================
    elements.append(Paragraph("BALANCE DE MATERIA", subtitle_style))

    material_data = [
        ["Corriente", "Flujo", "Unidad"],
        ["ENTRADA - Agua alimentación", f"{results.get('m_fw', '-'):.2f}", "t/h"],
        ["ENTRADA - Bagazo (AR)", f"{results.get('m_bagazo', '-'):.2f}", "t/h"],
        ["ENTRADA - Aire combustión", f"{results.get('m_air', '-'):.2f}", "t/h"],
        ["", "", ""],
        ["SALIDA - Vapor sobrecalentado", f"{results.get('m_stm', '-'):.2f}", "t/h"],
        ["SALIDA - Purga continua", f"{results.get('m_purge', '-'):.2f}", "t/h"],
        ["SALIDA - Gases combustión", f"{results.get('m_flue', '-'):.2f}", "t/h"],
    ]

    material_table = Table(material_data, colWidths=[6*cm, 3*cm, 2*cm])
    material_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#107C10')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#E8F5E9')),
        ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#FFEBEE')),
        ('BACKGROUND', (0, 2), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
    ]))
    elements.append(material_table)
    elements.append(Spacer(0.5*cm, 0.5*cm))

    # ==================== BALANCE DE ENERGÍA ====================
    elements.append(Paragraph("BALANCE DE ENERGÍA", subtitle_style))

    energy_data = [
        ["Corriente", "Energía", "Unidad"],
        ["ENTRADA - Agua alimentación", f"{results.get('Q_fw', '-'):.2f}", "MW"],
        ["ENTRADA - Combustión (bagazo)", f"{results.get('Q_fuel', '-'):.2f}", "MW"],
        ["ENTRADA - TOTAL", f"{results.get('Q_fw', 0) + results.get('Q_fuel', 0):.2f}", "MW"],
        ["", "", ""],
        ["SALIDA - Vapor", f"{results.get('Q_steam', '-'):.2f}", "MW"],
        ["SALIDA - Purga", f"{results.get('Q_purge', '-'):.2f}", "MW"],
        ["SALIDA - Pérdidas", f"{results.get('losses', '-'):.2f}", "MW"],
        ["SALIDA - TOTAL", f"{results.get('Q_steam', 0) + results.get('Q_purge', 0) + results.get('losses', 0):.2f}", "MW"],
    ]

    energy_table = Table(energy_data, colWidths=[6*cm, 3*cm, 2*cm])
    energy_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF8C00')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#FFF3E0')),
        ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#FFEBEE')),
        ('BACKGROUND', (0, 2), (-1, -1), colors.HexColor('#F5F5F5')),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
    ]))
    elements.append(energy_table)
    elements.append(Spacer(0.5*cm, 0.5*cm))

    # ==================== EFICIENCIA ====================
    elements.append(Paragraph("EFICIENCIA", subtitle_style))

    eff = inputs.get('efficiency', 0)
    eff_color = colors.green if eff >= 90 else (colors.orange if eff >= 85 else colors.red)

    eff_data = [
        ["Parámetro", "Valor"],
        ["Eficiencia Térmica", f"{eff:.1f} %"],
        ["Energía Absorbida (Q_abs)", f"{results.get('Q_abs', '-'):.2f} MW"],
        ["Energía Combustible (Q_fuel)", f"{results.get('Q_fuel', '-'):.2f} MW"],
        ["Pérdidas", f"{results.get('losses', '-'):.2f} MW"],
    ]

    eff_table = Table(eff_data, colWidths=[7*cm, 4*cm])
    eff_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), eff_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
    ]))
    elements.append(eff_table)
    elements.append(Spacer(1*cm, 1*cm))

    # ==================== PIE DE PÁGINA ====================
    footer_data = [
        ["", ""],
        ["Generado por Calculadora de Caldera Acuotubular", "DML INGENIEROS CONSULTORES S.A.S."],
    ]

    footer_table = Table(footer_data, colWidths=[10*cm, 6*cm])
    footer_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.gray),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(footer_table)

    # Generar PDF
    try:
        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    except Exception as e:
        print(f"Error generando PDF: {e}")
        buffer.close()
        return None


def is_pdf_generation_available() -> bool:
    """Verifica si la generación de PDF está disponible."""
    return REPORTLAB_AVAILABLE
