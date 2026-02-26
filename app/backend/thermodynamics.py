"""
Módulo de Termodinámica - Cálculos con IAPWS-97
=================================================
Cálculo de propiedades termodinámicas del agua y vapor
utilizando las formulaciones IAPWS-97 (Industrial Formulation 1997
for the Thermodynamic Properties of Water and Steam).

DML INGENIEROS CONSULTORES S.A.S.
Autores: Jonathan Arboleda Genes, Herminsul Rosero
"""

from typing import NamedTuple
from iapws import IAPWS97


# ═══════════════════════════════════════════════════════════════════════════════
# ESTRUCTURAS DE DATOS
# ═══════════════════════════════════════════════════════════════════════════════

class SteamProperties(NamedTuple):
    """Propiedades del vapor sobrecalentado."""
    h: float  # Entalpía específica [kJ/kg]
    s: float  # Entropía específica [kJ/kg·K]
    rho: float  # Densidad [kg/m³]
    T: float  # Temperatura [°C]
    P: float  # Presión [bara]


class WaterProperties(NamedTuple):
    """Propiedades del agua líquida."""
    h: float  # Entalpía específica [kJ/kg]
    T: float  # Temperatura [°C]
    P: float  # Presión [bara]


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE CÁLCULO
# ═══════════════════════════════════════════════════════════════════════════════

def get_steam_properties(P_barg: float, T_celsius: float) -> SteamProperties:
    """
    Calcula las propiedades del vapor sobrecalentado usando IAPWS-97.

    Parameters
    ----------
    P_barg : float
        Presión del vapor [barg] (presión manométrica)
    T_celsius : float
        Temperatura del vapor [°C]

    Returns
    -------
    SteamProperties
        Objeto con entalpía, entropía, densidad, temperatura y presión

    Example
    -------
    >>> props = get_steam_properties(106, 545)
    >>> props.h
    3482.23
    >>> props.rho
    32.5
    """
    # Convertir a unidades IAPWS: P en [MPa], T en [K]
    # IAPWS97 usa MPa como unidad de presión estándar
    P_mpa = (P_barg + 1.01325) / 10  # barg → MPa
    T_kelvin = T_celsius + 273.15  # °C → K

    # Crear objeto IAPWS97 para vapor sobrecalentado
    steam = IAPWS97(P=P_mpa, T=T_kelvin)

    return SteamProperties(
        h=round(steam.h, 2),
        s=round(steam.s, 4),
        rho=round(steam.rho, 2),
        T=round(T_celsius, 1),
        P=round(P_barg, 1)
    )


def get_feedwater_properties(T_celsius: float, P_barg: float) -> WaterProperties:
    """
    Calcula las propiedades del agua de alimentación usando IAPWS-97.

    Parameters
    ----------
    T_celsius : float
        Temperatura del agua [°C]
    P_barg : float
        Presión del agua [barg] (presión de bombeo)

    Returns
    -------
    WaterProperties
        Objeto con entalpía, temperatura y presión
    """
    # Convertir a unidades IAPWS: P en [MPa], T en [K]
    P_mpa = (P_barg + 1.01325) / 10
    T_kelvin = T_celsius + 273.15

    # Crear objeto IAPWS97 para agua comprimida (líquido)
    water = IAPWS97(P=P_mpa, T=T_kelvin)

    return WaterProperties(
        h=round(water.h, 2),
        T=round(T_celsius, 1),
        P=round(P_barg, 1)
    )


def get_saturated_liquid_properties(P_barg: float) -> WaterProperties:
    """
    Calcula las propiedades del líquido saturado (para purga) usando IAPWS-97.

    Parameters
    ----------
    P_barg : float
        Presión de saturación [barg]

    Returns
    -------
    WaterProperties
        Objeto con entalpía de líquido saturado
    """
    P_mpa = (P_barg + 1.01325) / 10

    # Crear objeto IAPWS97 para líquido saturado (calidad x=0)
    sat_liquid = IAPWS97(P=P_mpa, x=0)

    return WaterProperties(
        h=round(sat_liquid.h, 2),
        T=round(sat_liquid.T - 273.15, 1),  # K → °C
        P=round(P_barg, 1)
    )


def get_saturation_temperature(P_barg: float) -> float:
    """
    Calcula la temperatura de saturación a una presión dada.

    Parameters
    ----------
    P_barg : float
        Presión [barg]

    Returns
    -------
    float
        Temperatura de saturación [°C]
    """
    P_mpa = (P_barg + 1.01325) / 10
    sat = IAPWS97(P=P_mpa, x=0)
    return round(sat.T - 273.15, 1)


# ═══════════════════════════════════════════════════════════════════════════════
# CÁLCULOS DE ENERGÍA
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_stream_energy(m_flow_kgh: float, h_kjkg: float) -> float:
    """
    Calcula el flujo de energía de una corriente.

    Parameters
    ----------
    m_flow_kgh : float
        Flujo másico [kg/h]
    h_kjkg : float
        Entalpía específica [kJ/kg]

    Returns
    -------
    float
        Flujo de energía [MW]
    """
    # E = m * h / (3.6 × 10^6) para convertir de kJ/h a MW
    # 1 MW = 1 MJ/s = 3600 MJ/h
    return round(m_flow_kgh * h_kjkg / 3_600_000, 2)


def calculate_stream_energy_from_tons(m_flow_th: float, h_kjkg: float) -> float:
    """
    Calcula el flujo de energía de una corriente (entrada en t/h).

    Parameters
    ----------
    m_flow_th : float
        Flujo másico [t/h]
    h_kjkg : float
        Entalpía específica [kJ/kg]

    Returns
    -------
    float
        Flujo de energía [MW]
    """
    return calculate_stream_energy(m_flow_th * 1000, h_kjkg)


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDACIÓN CON DATOS BASE
# ═══════════════════════════════════════════════════════════════════════════════

def validate_with_base_case() -> dict:
    """
    Valida los cálculos con los datos base del proyecto.

    Datos base (documentación):
    - Vapor: 100 t/h, 106 barg, 545 °C
    - Resultado esperado: h = 3482.23 kJ/kg

    Returns
    -------
    dict
        Diccionario con resultados de validación
    """
    # Vapor sobrecalentado
    steam = get_steam_properties(106, 545)

    # Agua de alimentación
    fw = get_feedwater_properties(270, 106)

    # Purga (líquido saturado)
    blowdown = get_saturated_liquid_properties(106)

    return {
        "vapor_enthalpy": {
            "calculated": steam.h,
            "expected": 3482.23,
            "error_percent": abs(steam.h - 3482.23) / 3482.23 * 100,
            "valid": abs(steam.h - 3482.23) < 1.0  # Tolerancia 1 kJ/kg
        },
        "feedwater_enthalpy": {
            "calculated": fw.h,
            "expected": 1183.44,
            "error_percent": abs(fw.h - 1183.44) / 1183.44 * 100,
            "valid": abs(fw.h - 1183.44) < 1.0
        },
        "blowdown_enthalpy": {
            "calculated": blowdown.h,
            "expected": 1458.64,
            "error_percent": abs(blowdown.h - 1458.64) / 1458.64 * 100,
            "valid": abs(blowdown.h - 1458.64) < 1.0
        }
    }


if __name__ == "__main__":
    # Prueba de validación
    print("=== VALIDACIÓN TERMODINÁMICA ===\n")

    validation = validate_with_base_case()

    for prop, data in validation.items():
        status = "✓" if data["valid"] else "✗"
        print(f"{status} {prop}:")
        print(f"   Calculado: {data['calculated']}")
        print(f"   Esperado:  {data['expected']}")
        print(f"   Error:     {data['error_percent']:.4f}%")
