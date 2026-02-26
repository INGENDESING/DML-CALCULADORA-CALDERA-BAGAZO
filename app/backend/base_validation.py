"""
Módulo de Validación Base - Datos para Validación
==================================================
Contiene los datos base del proyecto para validar
que los cálculos sean correctos.

DML INGENIEROS CONSULTORES S.A.S.
Autores: Jonathan Arboleda Genes, Herminsul Rosero
"""

from dataclasses import dataclass
from typing import Dict, Any


# ═══════════════════════════════════════════════════════════════════════════════
# DATOS BASE DEL PROYECTO
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class BaseValidationData:
    """
    Datos base para validación obtenidos de la documentación.

    Referencia: /documentacion/sections/09_resultados.tex
    """

    # Datos de entrada
    m_stm: float = 100.0        # t/h
    P_stm: float = 106.0        # barg
    T_stm: float = 545.0        # °C
    T_fw: float = 270.0         # °C
    pct_purge: float = 2.0      # %
    efficiency: float = 94.0    # %

    # Bagazo
    bagazo_humidity: float = 48.0   # %
    bagazo_ash: float = 10.0        # %

    # Resultados esperados
    expected_ratio: float = 2.655       # t_vapor / t_bagazo
    expected_m_bagazo: float = 37.67    # t/h
    expected_m_fw: float = 102.04       # t/h
    expected_m_purge: float = 2.04      # t/h

    expected_Q_abs: float = 64.01       # MW
    expected_Q_fuel: float = 68.10      # MW

    expected_PCI: float = 6.51          # MJ/kg

    # Propiedades del vapor
    expected_h_steam: float = 3482.23   # kJ/kg
    expected_h_fw: float = 1183.44      # kJ/kg
    expected_h_purge: float = 1458.64   # kJ/kg


@dataclass
class Tolerance:
    """Tolerancias para validación."""
    ratio: float = 0.05          # ±5%
    m_bagazo: float = 0.5       # ±0.5 t/h
    Q_abs: float = 0.5          # ±0.5 MW
    Q_fuel: float = 0.5         # ±0.5 MW
    enthalpy: float = 5.0       # ±5 kJ/kg


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE VALIDACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

def validate_ratio(calculated: float, base: BaseValidationData = None,
                   tolerance: Tolerance = None) -> Dict[str, Any]:
    """
    Valida el ratio Vapor/Bagazo.

    Parameters
    ----------
    calculated : float
        Valor calculado
    base : BaseValidationData, opcional
        Datos base (usa default si no se especifica)
    tolerance : Tolerance, opcional
        Tolerancias (usa default si no se especifica)

    Returns
    -------
    dict
        Resultado de validación
    """
    if base is None:
        base = BaseValidationData()
    if tolerance is None:
        tolerance = Tolerance()

    expected = base.expected_ratio
    error = abs(calculated - expected)
    error_pct = (error / expected) * 100
    valid = error <= tolerance.ratio

    return {
        'valid': valid,
        'calculated': calculated,
        'expected': expected,
        'error': error,
        'error_pct': error_pct,
        'tolerance': tolerance.ratio,
        'message': f"Ratio: {calculated:.3f} (esperado: {expected:.3f}, "
                  f"error: {error_pct:.2f}%)"
    }


def validate_m_bagazo(calculated: float, base: BaseValidationData = None,
                      tolerance: Tolerance = None) -> Dict[str, Any]:
    """Valida el flujo de bagazo."""
    if base is None:
        base = BaseValidationData()
    if tolerance is None:
        tolerance = Tolerance()

    expected = base.expected_m_bagazo
    error = abs(calculated - expected)
    error_pct = (error / expected) * 100
    valid = error <= tolerance.m_bagazo

    return {
        'valid': valid,
        'calculated': calculated,
        'expected': expected,
        'error': error,
        'error_pct': error_pct,
        'message': f"Bagazo: {calculated:.2f} t/h (esperado: {expected:.2f} t/h, "
                  f"error: {error_pct:.2f}%)"
    }


def validate_Q_abs(calculated: float, base: BaseValidationData = None,
                   tolerance: Tolerance = None) -> Dict[str, Any]:
    """Valida el calor absorbido."""
    if base is None:
        base = BaseValidationData()
    if tolerance is None:
        tolerance = Tolerance()

    expected = base.expected_Q_abs
    error = abs(calculated - expected)
    error_pct = (error / expected) * 100
    valid = error <= tolerance.Q_abs

    return {
        'valid': valid,
        'calculated': calculated,
        'expected': expected,
        'error': error,
        'error_pct': error_pct,
        'message': f"Q_abs: {calculated:.2f} MW (esperado: {expected:.2f} MW, "
                  f"error: {error_pct:.2f}%)"
    }


def validate_complete_results(results: Dict[str, float],
                               base: BaseValidationData = None,
                               tolerance: Tolerance = None) -> Dict[str, Any]:
    """
    Valida todos los resultados contra los datos base.

    Parameters
    ----------
    results : dict
        Diccionario con resultados calculados. Claves esperadas:
        - ratio_stm_bagazo
        - m_bagazo
        - Q_abs
        - Q_fuel
    base : BaseValidationData, opcional
        Datos base
    tolerance : Tolerance, opcional
        Tolerancias

    Returns
    -------
    dict
        Reporte completo de validación
    """
    if base is None:
        base = BaseValidationData()
    if tolerance is None:
        tolerance = Tolerance()

    validations = {}

    # Validar cada resultado
    if 'ratio_stm_bagazo' in results:
        validations['ratio'] = validate_ratio(
            results['ratio_stm_bagazo'], base, tolerance
        )

    if 'm_bagazo' in results:
        validations['m_bagazo'] = validate_m_bagazo(
            results['m_bagazo'], base, tolerance
        )

    if 'Q_abs' in results:
        validations['Q_abs'] = validate_Q_abs(
            results['Q_abs'], base, tolerance
        )

    # Determinar si todo es válido
    all_valid = all(v['valid'] for v in validations.values())

    return {
        'all_valid': all_valid,
        'validations': validations,
        'summary': f"Validación: {'✓ APROBADA' if all_valid else '✗ FALLIDA'}"
    }


def get_base_inputs() -> Dict[str, float]:
    """
    Retorna los inputs base para inicializar la aplicación.

    Returns
    -------
    dict
        Diccionario con valores base
    """
    base = BaseValidationData()

    return {
        'm_stm': base.m_stm,
        'P_stm': base.P_stm,
        'T_stm': base.T_stm,
        'T_fw': base.T_fw,
        'pct_purge': base.pct_purge,
        'efficiency': base.efficiency,
        'bagazo_humidity': base.bagazo_humidity,
        'bagazo_ash': base.bagazo_ash,
        'altitude': 1000.0,  # Valor típico Valle del Cauca
        'RH': 75.0,
        'T_amb': 30.0,
        'excess_air': 20.0,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE FORMATEO
# ═══════════════════════════════════════════════════════════════════════════════

def format_validation_report(report: Dict[str, Any]) -> str:
    """Formatea el reporte de validación para mostrar."""
    lines = []
    lines.append(f"{report['summary']}")
    lines.append("")

    for key, val in report['validations'].items():
        status = "✓" if val['valid'] else "✗"
        lines.append(f"{status} {val['message']}")

    return "\n".join(lines)


if __name__ == "__main__":
    # Prueba de validación
    print("=== PRUEBA DE VALIDACIÓN BASE ===\n")

    # Simular resultados correctos
    results = {
        'ratio_stm_bagazo': 2.655,
        'm_bagazo': 37.67,
        'Q_abs': 64.01,
        'Q_fuel': 68.10
    }

    report = validate_complete_results(results)
    print(format_validation_report(report))

    # Mostrar inputs base
    print("\n=== INPUTS BASE ===\n")
    inputs = get_base_inputs()
    for key, val in inputs.items():
        print(f"{key}: {val}")
