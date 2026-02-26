"""
Módulo de Validación - Validación de Datos de Entrada
=======================================================
Validación de rangos y consistencia de datos de entrada.

DML INGENIEROS CONSULTORES S.A.S.
Autores: Jonathan Arboleda Genes, Herminsul Rosero
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


# ═══════════════════════════════════════════════════════════════════════════════
# ESTRUCTURAS DE DATOS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ValidationResult:
    """Resultado de una validación."""
    valid: bool
    field: str
    message: str
    value: float = None
    min_value: float = None
    max_value: float = None


@dataclass
class ValidationReport:
    """Reporte completo de validación."""
    is_valid: bool
    errors: List[ValidationResult]
    warnings: List[ValidationResult]

    def get_error_messages(self) -> str:
        """Retorna los mensajes de error como string."""
        if not self.errors:
            return "Sin errores"
        return "\n".join([f"✗ {e.field}: {e.message}" for e in self.errors])

    def get_warning_messages(self) -> str:
        """Retorna los mensajes de advertencia como string."""
        if not self.warnings:
            return "Sin advertencias"
        return "\n".join([f"⚠ {w.field}: {w.message}" for w in self.warnings])


# ═══════════════════════════════════════════════════════════════════════════════
# DEFINICIONES DE RANGOS
# ═══════════════════════════════════════════════════════════════════════════════

RANGES = {
    # Vapor
    'm_stm': (10.0, 200.0, 't/h', 'Flujo de vapor'),
    'P_stm': (40.0, 150.0, 'barg', 'Presión de vapor'),
    'T_stm': (400.0, 600.0, '°C', 'Temperatura de vapor'),
    'T_fw': (150.0, 300.0, '°C', 'Temperatura agua alimentación'),
    'pct_purge': (0.5, 5.0, '%', 'Porcentaje de purga'),
    'efficiency': (50.0, 95.0, '%', 'Eficiencia térmica'),

    # Bagazo
    'bagazo_humidity': (40.0, 60.0, '%', 'Humedad del bagazo'),
    'bagazo_ash': (1.0, 15.0, '%', 'Cenizas del bagazo'),

    # Aire
    'altitude': (0.0, 3000.0, 'msnm', 'Altitud'),
    'RH': (30.0, 95.0, '%', 'Humedad relativa'),
    'T_amb': (15.0, 40.0, '°C', 'Temperatura ambiente'),
    'excess_air': (10.0, 50.0, '%', 'Exceso de aire'),
}


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE VALIDACIÓN
# ═══════════════════════════════════════════════════════════════════════════════

def validate_range(value: float, field: str) -> ValidationResult:
    """
    Valida que un valor esté dentro del rango permitido.

    Parameters
    ----------
    value : float
        Valor a validar
    field : str
        Nombre del campo (debe existir en RANGES)

    Returns
    -------
    ValidationResult
        Resultado de la validación
    """
    if field not in RANGES:
        return ValidationResult(
            valid=False,
            field=field,
            message=f"Campo desconocido: {field}"
        )

    min_val, max_val, unit, name = RANGES[field]

    if value < min_val or value > max_val:
        return ValidationResult(
            valid=False,
            field=field,
            message=f"{name} debe estar entre {min_val} y {max_val} {unit}",
            value=value,
            min_value=min_val,
            max_value=max_val
        )

    return ValidationResult(
        valid=True,
        field=field,
        message=f"{name} válido: {value} {unit}",
        value=value
    )


def validate_consistency(T_stm: float, T_fw: float,
                         P_stm: float) -> ValidationResult:
    """
    Valida la consistencia termodinámica entre temperaturas.

    Parameters
    ----------
    T_stm : float
        Temperatura del vapor [°C]
    T_fw : float
        Temperatura del agua de alimentación [°C]
    P_stm : float
        Presión del vapor [barg]

    Returns
    -------
    ValidationResult
        Resultado de la validación
    """
    # El vapor debe estar más caliente que el agua de alimentación
    if T_stm <= T_fw:
        return ValidationResult(
            valid=False,
            field='T_stm',
            message=f"La temperatura del vapor ({T_stm}°C) debe ser mayor "
                   f"que la del agua de alimentación ({T_fw}°C)"
        )

    # Verificar que el vapor esté sobrecalentado
    # Temperatura de saturación aproximada a la presión dada
    # (fórmula simplificada: T_sat ≈ T_sat_atm + P_stm × 3.6)
    T_sat_approx = 100 + P_stm * 2.8

    if T_stm < T_sat_approx + 10:
        return ValidationResult(
            valid=False,
            field='T_stm',
            message=f"La temperatura del vapor ({T_stm}°C) parece muy baja. "
                   f"Para {P_stm} barg, se esperan >{T_sat_approx + 10:.0f}°C"
        )

    return ValidationResult(
        valid=True,
        field='consistency',
        message="Consistencia termodinámica OK"
    )


def validate_bagazo_limits(humidity: float, ash: float) -> ValidationResult:
    """
    Valida que la suma de humedad + cenizas no exceda el límite.

    Parameters
    ----------
    humidity : float
        Humedad [%]
    ash : float
        Cenizas [%]

    Returns
    -------
    ValidationResult
        Resultado de la validación
    """
    total = humidity + ash

    if total > 90:
        return ValidationResult(
            valid=False,
            field='bagazo',
            message=f"Humedad + Cenizas = {total}% excede el límite práctico (90%)"
        )

    if total > 80:
        return ValidationResult(
            valid=True,  # Advertencia, no error
            field='bagazo',
            message=f"ADVERTENCIA: Humedad + Cenizas = {total}% es muy alto"
        )

    return ValidationResult(
        valid=True,
        field='bagazo',
        message="Composición de bagazo válida"
    )


def validate_inputs(**kwargs) -> ValidationReport:
    """
    Valida todos los inputs de entrada.

    Parameters
    ----------
    **kwargs : dict
        Diccionario con todos los valores a validar

    Returns
    -------
    ValidationReport
        Reporte completo de validación
    """
    errors = []
    warnings = []

    # Validación de rangos
    for field, value in kwargs.items():
        if field in RANGES and value is not None:
            result = validate_range(value, field)
            if not result.valid:
                errors.append(result)
            elif "ADVERTENCIA" in result.message:
                warnings.append(result)

    # Validación de consistencia
    if all(k in kwargs for k in ['T_stm', 'T_fw', 'P_stm']):
        consistency = validate_consistency(
            kwargs['T_stm'],
            kwargs['T_fw'],
            kwargs['P_stm']
        )
        if not consistency.valid:
            errors.append(consistency)

    # Validación de límites de bagazo
    if all(k in kwargs for k in ['bagazo_humidity', 'bagazo_ash']):
        bagazo_check = validate_bagazo_limits(
            kwargs['bagazo_humidity'],
            kwargs['bagazo_ash']
        )
        if not bagazo_check.valid:
            errors.append(bagazo_check)
        elif "ADVERTENCIA" in bagazo_check.message:
            warnings.append(bagazo_check)

    return ValidationReport(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )


def get_default_values() -> dict:
    """
    Retorna los valores por defecto para todos los campos.

    Returns
    -------
    dict
        Diccionario con valores por defecto
    """
    return {
        # Metadatos
        'project_code': 'P2807',
        'document_code': 'P2807-PR-MC-001',
        'analyst': '',
        'date': '',

        # Vapor
        'm_stm': 100.0,
        'P_stm': 106.0,
        'T_stm': 545.0,
        'T_fw': 270.0,
        'pct_purge': 2.0,
        'efficiency': 94.0,

        # Bagazo
        'bagazo_humidity': 48.0,
        'bagazo_ash': 10.0,

        # Aire
        'altitude': 1000.0,
        'RH': 75.0,
        'T_amb': 30.0,
        'excess_air': 20.0,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════════════════════

def format_validation_error(report: ValidationReport) -> str:
    """Formatea el reporte de errores para mostrar en UI."""
    if report.is_valid:
        return "✓ Todos los datos son válidos"

    output = []
    if report.errors:
        output.append("**Errores:**")
        for error in report.errors:
            output.append(f"  - {error.message}")

    if report.warnings:
        output.append("**Advertencias:**")
        for warning in report.warnings:
            output.append(f"  - {warning.message}")

    return "\n".join(output)


if __name__ == "__main__":
    # Prueba de validación
    print("=== PRUEBA DE VALIDACIÓN ===\n")

    # Caso válido
    valid_inputs = get_default_values()
    report = validate_inputs(**valid_inputs)
    print("Caso válido:")
    print(f"  Válido: {report.is_valid}")
    print()

    # Caso inválido
    invalid_inputs = valid_inputs.copy()
    invalid_inputs['m_stm'] = 5.0  # Fuera de rango
    invalid_inputs['T_stm'] = 200.0  # Menor que T_fw

    report = validate_inputs(**invalid_inputs)
    print("Caso inválido:")
    print(format_validation_error(report))
