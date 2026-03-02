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
    from reportlab.graphics.shapes import Drawing, Rect, Line, String, Polygon
    from reportlab.graphics import renderPDF
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGRAMA PFD PARA PDF
# ═══════════════════════════════════════════════════════════════════════════════

def _fmt(val, decimals=2):
    """Formatea un valor numérico o retorna '-'."""
    if val is None or val == '-':
        return '-'
    try:
        return f"{float(val):.{decimals}f}"
    except (ValueError, TypeError):
        return str(val)


def _create_pfd_drawing(results: Dict) -> Drawing:
    """
    Crea el diagrama PFD como Drawing de ReportLab.

    Layout simplificado:
    [Etiquetas entrada] → [CALDERA] → [Etiquetas salida]
    """
    w, h = 500, 320
    d = Drawing(w, h)

    # Colores
    blue = colors.HexColor('#0078D4')
    red = colors.HexColor('#E74C3C')
    orange = colors.HexColor('#F39C12')
    gray = colors.HexColor('#95A5A6')
    dark_gray = colors.HexColor('#7F8C8D')
    brown = colors.HexColor('#8B7355')
    bg_dark = colors.HexColor('#2D2D30')
    white = colors.white

    # ── Rectángulo central: CALDERA ──
    cx, cy, cw, ch = 185, 80, 130, 160
    d.add(Rect(cx, cy, cw, ch, fillColor=colors.HexColor('#1E3A5F'),
               strokeColor=blue, strokeWidth=2))
    d.add(String(cx + cw/2, cy + ch/2 + 12, 'CALDERA',
                 fontSize=11, fillColor=white, textAnchor='middle',
                 fontName='Helvetica-Bold'))
    d.add(String(cx + cw/2, cy + ch/2 - 4, 'ACUOTUBULAR',
                 fontSize=9, fillColor=colors.HexColor('#80B0E0'), textAnchor='middle'))

    # ── Título ──
    d.add(String(w/2, h - 10, 'DIAGRAMA DE FLUJO DE PROCESO (PFD)',
                 fontSize=11, fillColor=colors.HexColor('#333333'),
                 textAnchor='middle', fontName='Helvetica-Bold'))

    # ── Helper: flecha horizontal ──
    def arrow_h(x1, y1, x2, y2, clr):
        d.add(Line(x1, y1, x2, y2, strokeColor=clr, strokeWidth=2))
        # Punta de flecha
        if x2 > x1:  # derecha
            d.add(Polygon([x2, y2, x2-6, y2+4, x2-6, y2-4], fillColor=clr, strokeColor=clr))
        else:  # izquierda
            d.add(Polygon([x2, y2, x2+6, y2+4, x2+6, y2-4], fillColor=clr, strokeColor=clr))

    # ── Helper: etiqueta de corriente ──
    def stream_label(x, y, title, lines, clr, align='start'):
        ty = y + len(lines) * 11 + 4
        d.add(String(x, ty, title, fontSize=8, fillColor=clr,
                     fontName='Helvetica-Bold', textAnchor=align))
        for i, line in enumerate(lines):
            d.add(String(x, ty - (i+1)*11, line, fontSize=7,
                         fillColor=colors.HexColor('#333333'), textAnchor=align))

    # ── ENTRADAS (izquierda) ──

    # Agua de alimentación (arriba)
    y_fw = 210
    arrow_h(120, y_fw, cx, y_fw, colors.HexColor('#3498DB'))
    stream_label(5, y_fw - 8, 'AGUA DE ALIMENTACIÓN', [
        f"Flujo: {_fmt(results.get('m_fw'))} t/h",
        f"Temp: {_fmt(results.get('T_fw'), 1)} °C",
        f"E: {_fmt(results.get('Q_fw'))} MW",
    ], colors.HexColor('#3498DB'))

    # Bagazo (medio)
    y_bag = 150
    arrow_h(120, y_bag, cx, y_bag, orange)
    stream_label(5, y_bag - 8, 'BAGAZO (AR)', [
        f"Flujo: {_fmt(results.get('m_bagazo'))} t/h",
        f"Temp: {_fmt(results.get('T_amb'), 1)} °C",
        f"E: {_fmt(results.get('Q_fuel'))} MW",
    ], orange)

    # Aire (abajo)
    y_air = 95
    arrow_h(120, y_air, cx, y_air, gray)
    stream_label(5, y_air - 8, 'AIRE DE COMBUSTIÓN', [
        f"Flujo: {_fmt(results.get('m_air'))} t/h",
        f"Temp: {_fmt(results.get('T_amb'), 1)} °C",
        f"Exc: {_fmt(results.get('excess_air'), 1)} %",
    ], gray)

    # ── SALIDAS (derecha) ──

    # Vapor sobrecalentado (arriba)
    y_stm = 220
    arrow_h(cx + cw, y_stm, 380, y_stm, red)
    stream_label(385, y_stm - 8, 'VAPOR SOBRECALENTADO', [
        f"Flujo: {_fmt(results.get('m_stm'))} t/h",
        f"Temp: {_fmt(results.get('T_stm'), 1)} °C",
        f"Pres: {_fmt(results.get('P_stm'), 1)} barg",
        f"h: {_fmt(results.get('h_steam'), 1)} kJ/kg",
        f"E: {_fmt(results.get('Q_steam'))} MW",
    ], red)

    # Purga continua (medio-alto)
    y_pur = 155
    arrow_h(cx + cw, y_pur, 380, y_pur, colors.HexColor('#3498DB'))
    stream_label(385, y_pur - 8, 'PURGA CONTINUA', [
        f"Flujo: {_fmt(results.get('m_purge'))} t/h",
        f"Temp: {_fmt(results.get('T_purge'), 1)} °C",
        f"E: {_fmt(results.get('Q_purge'))} MW",
    ], colors.HexColor('#3498DB'))

    # Gases de combustión (medio-bajo)
    y_gas = 100
    arrow_h(cx + cw, y_gas, 380, y_gas, dark_gray)
    stream_label(385, y_gas - 8, 'GASES DE COMBUSTIÓN', [
        f"Flujo: {_fmt(results.get('m_flue'))} t/h",
        f"Temp: {_fmt(results.get('T_flue'), 1)} °C",
        f"E: {_fmt(results.get('Q_flue'))} MW",
    ], dark_gray)

    # Cenizas (abajo derecha)
    y_ash = 55
    arrow_h(cx + cw, y_ash, 380, y_ash, brown)
    stream_label(385, y_ash - 4, 'CENIZAS', [
        f"Flujo: {_fmt(results.get('m_ash'))} t/h",
    ], brown)

    return d


# ═══════════════════════════════════════════════════════════════════════════════
# GENERADOR PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

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
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )

    # Elementos del documento
    elements = []

    # Estilos
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#0078D4'),
        alignment=TA_CENTER,
        spaceAfter=0.3*cm
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        alignment=TA_LEFT,
        spaceAfter=0.2*cm,
        spaceBefore=0.3*cm
    )

    # ==================== ENCABEZADO ====================
    elements.append(Paragraph("DML INGENIEROS CONSULTORES S.A.S.", ParagraphStyle(
        'Company', parent=styles['Normal'], fontSize=10, textColor=colors.gray, alignment=TA_CENTER
    )))
    elements.append(Spacer(0.3*cm, 0.3*cm))
    elements.append(Paragraph("CALCULADORA DE CALDERA ACUOTUBULAR", title_style))
    elements.append(Paragraph("Reporte de Balance de Materia y Energía", ParagraphStyle(
        'Sub', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10
    )))
    elements.append(Spacer(0.2*cm, 0.2*cm))

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elements.append(Paragraph(f"<b>Fecha:</b> {fecha}", styles['Normal']))
    elements.append(Spacer(0.3*cm, 0.3*cm))

    # ==================== KPIs ====================
    elements.append(Paragraph("INDICADORES CLAVE (KPIs)", subtitle_style))

    ratio = results.get('ratio', 0)

    # KPI principal: Ratio
    ratio_data = [
        [Paragraph('<b>RATIO VAPOR / BAGAZO</b>', ParagraphStyle(
            'r1', parent=styles['Normal'], alignment=TA_CENTER, fontSize=10, textColor=colors.white)),
         '', ''],
        [Paragraph(f'<b><font size="28">{ratio:.3f}</font></b>', ParagraphStyle(
            'r2', parent=styles['Normal'], alignment=TA_CENTER, textColor=colors.HexColor('#0078D4'))),
         '', ''],
        [Paragraph('t_vapor / t_bagazo', ParagraphStyle(
            'r3', parent=styles['Normal'], alignment=TA_CENTER, fontSize=9, textColor=colors.gray)),
         '', ''],
    ]

    ratio_table = Table(ratio_data, colWidths=[17*cm/3, 17*cm/3, 17*cm/3])
    ratio_table.setStyle(TableStyle([
        ('SPAN', (0, 0), (2, 0)),
        ('SPAN', (0, 1), (2, 1)),
        ('SPAN', (0, 2), (2, 2)),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0078D4')),
        ('BACKGROUND', (0, 1), (-1, 2), colors.HexColor('#F0F6FC')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, 1), 8),
        ('BOTTOMPADDING', (0, 2), (-1, 2), 8),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#0078D4')),
    ]))
    elements.append(ratio_table)
    elements.append(Spacer(0.3*cm, 0.3*cm))

    # KPIs secundarios en fila
    kpi_data = [
        ['Flujo Bagazo', 'Flujo Agua', 'PCI Bagazo', 'Calor Absorbido'],
        [f"{_fmt(results.get('m_bagazo'))} t/h",
         f"{_fmt(results.get('m_fw'))} t/h",
         f"{_fmt(results.get('PCI_MJ_kg'))} MJ/kg",
         f"{_fmt(results.get('Q_abs'))} MW"],
    ]

    kpi_table = Table(kpi_data, colWidths=[4.25*cm]*4)
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#252526')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#FFF3E0')),   # Bagazo - naranja
        ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#E3F2FD')),   # Agua - azul
        ('BACKGROUND', (2, 1), (2, 1), colors.HexColor('#FFEBEE')),   # PCI - rojo
        ('BACKGROUND', (3, 1), (3, 1), colors.HexColor('#E8F5E9')),   # Q_abs - verde
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CCCCCC')),
        ('TOPPADDING', (0, 1), (-1, 1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
    ]))
    elements.append(kpi_table)
    elements.append(Spacer(0.3*cm, 0.3*cm))

    # ==================== DIAGRAMA PFD ====================
    elements.append(Paragraph("DIAGRAMA DE FLUJO DE PROCESO (PFD)", subtitle_style))

    pfd = _create_pfd_drawing(results)
    elements.append(pfd)
    elements.append(Spacer(0.3*cm, 0.3*cm))

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

    input_table = Table(input_data, colWidths=[6*cm, 3*cm, 2*cm])
    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0078D4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
    ]))
    elements.append(input_table)
    elements.append(Spacer(0.3*cm, 0.3*cm))

    # ==================== TABLA DE RESULTADOS ====================
    elements.append(Paragraph("TABLA DE RESULTADOS", subtitle_style))

    results_data = [
        ["Tipo", "Corriente", "Flujo [t/h]", "T [°C]", "Energía [MW]"],
        ["ENTRADA", "Agua de Alimentación",
         _fmt(results.get('m_fw')), _fmt(results.get('T_fw'), 1), _fmt(results.get('Q_fw'))],
        ["ENTRADA", "Bagazo (AR)",
         _fmt(results.get('m_bagazo')), _fmt(results.get('T_amb'), 1), _fmt(results.get('Q_fuel'))],
        ["ENTRADA", "Aire de Combustión",
         _fmt(results.get('m_air')), _fmt(results.get('T_amb'), 1), "-"],
        ["", "", "", "", ""],
        ["SALIDA", "Vapor Sobrecalentado",
         _fmt(results.get('m_stm')), _fmt(results.get('T_stm'), 1), _fmt(results.get('Q_steam'))],
        ["SALIDA", "Purga Continua",
         _fmt(results.get('m_purge')), _fmt(results.get('T_purge'), 1), _fmt(results.get('Q_purge'))],
        ["SALIDA", "Gases de Combustión",
         _fmt(results.get('m_flue')), _fmt(results.get('T_flue'), 1), _fmt(results.get('Q_flue'))],
        ["SALIDA", "Cenizas",
         _fmt(results.get('m_ash')), "-", "-"],
    ]

    results_table = Table(results_data, colWidths=[2.5*cm, 5*cm, 3*cm, 2.5*cm, 3*cm])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#252526')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
        # Entradas - fondo azul claro
        ('BACKGROUND', (0, 1), (-1, 3), colors.HexColor('#E3F2FD')),
        # Separador
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#CCCCCC')),
        # Salidas - fondo naranja claro
        ('BACKGROUND', (0, 5), (-1, -1), colors.HexColor('#FFF3E0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#AAAAAA')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(results_table)
    elements.append(Spacer(0.5*cm, 0.5*cm))

    # ==================== EFICIENCIA ====================
    elements.append(Paragraph("EFICIENCIA", subtitle_style))

    eff = inputs.get('efficiency', 0)
    eff_color = colors.HexColor('#107C10') if eff >= 90 else (colors.HexColor('#FF8C00') if eff >= 85 else colors.HexColor('#E81123'))

    eff_data = [
        ["Parámetro", "Valor"],
        ["Eficiencia Térmica", f"{eff:.1f} %"],
        ["Energía Absorbida (Q_abs)", f"{_fmt(results.get('Q_abs'))} MW"],
        ["Energía Combustible (Q_fuel)", f"{_fmt(results.get('Q_fuel'))} MW"],
        ["Pérdidas", f"{_fmt(results.get('losses'))} MW"],
    ]

    eff_table = Table(eff_data, colWidths=[7*cm, 4*cm])
    eff_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), eff_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('GRID', (0, 0), (-1, -1), 1, colors.gray),
    ]))
    elements.append(eff_table)
    elements.append(Spacer(0.5*cm, 0.5*cm))

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
