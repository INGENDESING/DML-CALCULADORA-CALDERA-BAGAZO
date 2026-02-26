"""
Módulo Psicrometría - Propiedades del Aire Húmedo
====================================================
Cálculo de propiedades del aire húmedo según altitud,
temperatura y humedad relativa.

DML INGENIEROS CONSULTORES S.A.S.
Autores: Jonathan Arboleda Genes, Herminsul Rosero

Referencias:
- ASHRAE Handbook - Fundamentals
- Wexler, A. (1976). Vapor pressure formulation.
"""

from typing import NamedTuple
from dataclasses import dataclass
import math


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════

# Constantes físicas
P_STD = 101.325  # Presión estándar al nivel del mar [kPa]
T_STD = 288.15   # Temperatura estándar [K] (15°C)
R_AIR = 287.05   # Constante específica del aire seco [J/kg·K]
R_VAPOR = 461.5  # Constante específica del vapor de agua [J/kg·K]
G = 9.80665     # Gravedad estándar [m/s²]
M_AIR = 28.965   # Peso molecular del aire seco [kg/kmol]
LAPSE_RATE = 0.0065  # Gradiente térmico [K/m] en tropósfera

# Relación de pesos moleculares
MW_RATIO = M_AIR / 18.015  # Aire / Agua = 1.608


# ═══════════════════════════════════════════════════════════════════════════════
# ESTRUCTURAS DE DATOS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class AirProperties:
    """Propiedades del aire."""
    P: float      # Presión atmosférica [kPa]
    T: float      # Temperatura [°C]
    rho: float    # Densidad [kg/m³]
    T_dew: float  # Temperatura de rocío [°C]
    W: float      # Humedad absoluta [kg agua/kg aire seco]
    RH: float     # Humedad relativa [%]
    P_v: float    # Presión de vapor [kPa]
    P_a: float    # Presión de aire seco [kPa]


@dataclass
class CombustionAir:
    """Aire de combustión con composición."""
    m_total: float  # Flujo másico total [kg aire/kg bagazo]
    m_dry: float    # Flujo de aire seco [kg aire seco/kg bagazo]
    m_vapor: float  # Flujo de vapor de agua [kg vapor/kg bagazo]

    # Composición en masa
    N2_pct: float   # Nitrógeno [%]
    O2_pct: float   # Oxígeno [%]
    H2O_pct: float  # Agua [%]


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE CÁLCULO
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_atmospheric_pressure(altitude_m: float) -> float:
    """
    Calcula la presión atmosférica según la altitud.

    Parameters
    ----------
    altitude_m : float
        Altitud sobre el nivel del mar [m]

    Returns
    -------
    float
        Presión atmosférica [kPa]

    Notes
    -----
    Usa la fórmula barométrica para la tropósfera (hasta 11000 m):
    P = P0 × (1 - L×h/T0)^(g×M/R×L)

    Para altitudes < 11000 m (typical en ingenios)
    """
    if altitude_m < 0:
        altitude_m = 0
    elif altitude_m > 11000:
        # Limitar a tropósfera
        altitude_m = 11000

    # Fórmula barométrica estándar
    exponent = (G * M_AIR) / (8314.3 * LAPSE_RATE)
    pressure = P_STD * (1 - LAPSE_RATE * altitude_m / T_STD) ** exponent

    return round(pressure, 3)


def calculate_saturation_vapor_pressure(T_celsius: float) -> float:
    """
    Calcula la presión de saturación de vapor (ecuación de Magnus-Tetens).

    Parameters
    ----------
    T_celsius : float
        Temperatura del aire [°C]

    Returns
    -------
    float
        Presión de saturación [kPa]

    Notes
    -----
    Ecuación de Magnus-Tetens:
    P_sat = 0.61078 × exp((17.27 × T) / (T + 237.3))

    Válida para: 0°C < T < 100°C
    """
    if T_celsius <= 0:
        T_celsius = 0.1

    P_sat = 0.61078 * math.exp((17.27 * T_celsius) / (T_celsius + 237.3))

    return round(P_sat, 4)


def calculate_vapor_pressure(RH_pct: float, P_sat: float) -> float:
    """
    Calcula la presión parcial de vapor de agua.

    Parameters
    ----------
    RH_pct : float
        Humedad relativa [%]
    P_sat : float
        Presión de saturación [kPa]

    Returns
    -------
    float
        Presión de vapor [kPa]
    """
    P_vapor = (RH_pct / 100) * P_sat

    return round(P_vapor, 4)


def calculate_humidity_ratio(P_vapor: float, P_atm: float) -> float:
    """
    Calcula la humedad absoluta (ratio de humedad).

    Parameters
    ----------
    P_vapor : float
        Presión de vapor [kPa]
    P_atm : float
        Presión atmosférica [kPa]

    Returns
    -------
    float
        Humedad absoluta [kg agua/kg aire seco]

    Notes
    -----
    W = 0.622 × P_v / (P_atm - P_v)
    """
    P_air = P_atm - P_vapor
    if P_air <= 0:
        P_air = P_atm * 0.99

    W = 0.622 * P_vapor / P_air

    return round(W, 6)


def calculate_dew_point(T_celsius: float, RH_pct: float) -> float:
    """
    Calcula la temperatura de rocío.

    Parameters
    ----------
    T_celsius : float
        Temperatura del aire [°C]
    RH_pct : float
        Humedad relativa [%]

    Returns
    -------
    float
        Temperatura de rocío [°C]

    Notes
    -----
    Ecuación de Magnus-Tetens inversa:
    T_rocío = (B × γ) / (A - γ)
    donde γ = A×T/(B+T) + ln(HR/100)
    """
    A = 17.27
    B = 237.3

    gamma = (A * T_celsius) / (B + T_celsius) + math.log(RH_pct / 100)
    T_dew = (B * gamma) / (A - gamma)

    return round(T_dew, 1)


def calculate_air_density(P_atm: float, T_celsius: float,
                          P_vapor: float = 0) -> float:
    """
    Calcula la densidad del aire húmedo.

    Parameters
    ----------
    P_atm : float
        Presión atmosférica [kPa]
    T_celsius : float
        Temperatura del aire [°C]
    P_vapor : float
        Presión de vapor [kPa] (0 para aire seco)

    Returns
    -------
    float
        Densidad del aire [kg/m³]

    Notes
    -----
    ρ = (P_a / (R_a × T)) + (P_v / (R_v × T))
    """
    T_kelvin = T_celsius + 273.15
    P_air = P_atm - P_vapor

    if P_air <= 0:
        P_air = P_atm * 0.99

    # Densidad de aire seco + vapor
    rho = (P_air * 1000) / (R_AIR * T_kelvin) + \
          (P_vapor * 1000) / (R_VAPOR * T_kelvin)

    return round(rho, 4)


def calculate_air_properties(altitude_m: float, T_celsius: float,
                             RH_pct: float) -> AirProperties:
    """
    Calcula todas las propiedades del aire.

    Parameters
    ----------
    altitude_m : float
        Altitud [m]
    T_celsius : float
        Temperatura [°C]
    RH_pct : float
        Humedad relativa [%]

    Returns
    -------
    AirProperties
        Objeto con todas las propiedades del aire
    """
    # Presión atmosférica
    P_atm = calculate_atmospheric_pressure(altitude_m)

    # Presión de saturación y de vapor
    P_sat = calculate_saturation_vapor_pressure(T_celsius)
    P_v = calculate_vapor_pressure(RH_pct, P_sat)

    # Humedad absoluta
    W = calculate_humidity_ratio(P_v, P_atm)

    # Temperatura de rocío
    T_dew = calculate_dew_point(T_celsius, RH_pct)

    # Densidad
    rho = calculate_air_density(P_atm, T_celsius, P_v)

    # Presión de aire seco
    P_a = P_atm - P_v

    return AirProperties(
        P=round(P_atm, 2),
        T=round(T_celsius, 1),
        rho=round(rho, 3),
        T_dew=T_dew,
        W=round(W, 4),
        RH=round(RH_pct, 1),
        P_v=round(P_v, 3),
        P_a=round(P_a, 2)
    )


def calculate_combustion_air_composition(altitude_m: float,
                                         T_celsius: float,
                                         RH_pct: float) -> CombustionAir:
    """
    Calcula la composición del aire de combustión.

    Parameters
    ----------
    altitude_m : float
        Altitud [m]
    T_celsius : float
        Temperatura ambiente [°C]
    RH_pct : float
        Humedad relativa [%]

    Returns
    -------
    CombustionAir
        Objeto con composición del aire de combustión

    Notes
    -----
    Retorna valores por kg de aire seco de entrada.
    """
    props = calculate_air_properties(altitude_m, T_celsius, RH_pct)

    # Por kg de aire seco
    m_dry = 1.0  # kg aire seco
    m_vapor = props.W  # kg vapor / kg aire seco
    m_total = m_dry + m_vapor  # kg aire húmedo / kg aire seco

    # Composición del aire seco
    O2_dry_pct = 23.2  # % en masa
    N2_dry_pct = 76.8  # % en masa

    # Composición del aire húmedo (% en masa del total)
    O2_pct = (m_dry * O2_dry_pct / 100) / m_total * 100
    N2_pct = (m_dry * N2_dry_pct / 100) / m_total * 100
    H2O_pct = m_vapor / m_total * 100

    return CombustionAir(
        m_total=round(m_total, 4),
        m_dry=1.0,
        m_vapor=round(m_vapor, 4),
        N2_pct=round(N2_pct, 2),
        O2_pct=round(O2_pct, 2),
        H2O_pct=round(H2O_pct, 2)
    )


def calculate_air_flow_for_fuel(m_fuel_kgh: float,
                                m_air_per_kg_fuel: float,
                                altitude_m: float,
                                T_celsius: float,
                                RH_pct: float) -> dict:
    """
    Calcula el flujo de aire de combustión.

    Parameters
    ----------
    m_fuel_kgh : float
        Flujo de combustible [kg/h]
    m_air_per_kg_fuel : float
        Aire requerido [kg aire/kg combustible]
    altitude_m : float
        Altitud [m]
    T_celsius : float
        Temperatura ambiente [°C]
    RH_pct : float
        Humedad relativa [%]

    Returns
    -------
    dict
        Flujos de aire [kg/h o t/h] y composición
    """
    comp = calculate_combustion_air_composition(altitude_m, T_celsius, RH_pct)

    # Flujo total de aire húmedo
    m_air_humid_kgh = m_fuel_kgh * m_air_per_kg_fuel  # kg aire húmedo/h

    # Descomponer en aire seco y vapor
    m_air_dry_kgh = m_air_humid_kgh / comp.m_total
    m_vapor_kgh = m_air_dry_kgh * comp.m_vapor

    # Componentes del aire seco
    m_O2_kgh = m_air_dry_kgh * 0.232
    m_N2_kgh = m_air_dry_kgh * 0.768

    return {
        'flows': {
            'air_total_kgh': round(m_air_humid_kgh, 2),
            'air_total_th': round(m_air_humid_kgh / 1000, 2),
            'air_dry_kgh': round(m_air_dry_kgh, 2),
            'vapor_kgh': round(m_vapor_kgh, 2),
            'O2_kgh': round(m_O2_kgh, 2),
            'N2_kgh': round(m_N2_kgh, 2),
        },
        'composition': {
            'N2': comp.N2_pct,
            'O2': comp.O2_pct,
            'H2O': comp.H2O_pct
        },
        'properties': {
            'T': T_celsius,
            'RH': RH_pct,
            'altitude': altitude_m
        }
    }


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDACIÓN CON DATOS TÍPICOS
# ═══════════════════════════════════════════════════════════════════════════════

def validate_with_typical_case() -> dict:
    """
    Valida con condiciones típicas de ingenio.

    Condiciones típicas:
    - Altitud: 1000 msnm (Valle del Cauca)
    - Temperatura: 30°C
    - Humedad relativa: 75%

    Returns
    -------
    dict
        Resultados de validación
    """
    props = calculate_air_properties(1000, 30, 75)

    return {
        'P_atm': props.P,
        'rho': props.rho,
        'W': props.W,
        'T_dew': props.T_dew,
        'composition': calculate_combustion_air_composition(1000, 30, 75)
    }


if __name__ == "__main__":
    # Prueba de validación
    print("=== VALIDACIÓN PSICROMETRÍA ===\n")

    results = validate_with_typical_case()

    print(f"Presión atmosférica: {results['P_atm']} kPa")
    print(f"Densidad del aire: {results['rho']} kg/m³")
    print(f"Humedad absoluta: {results['W']} kg agua/kg aire seco")
    print(f"Temperatura de rocío: {results['T_dew']} °C")
    print(f"\nComposición aire combustión (por kg aire seco):")
    comp = results['composition']
    print(f"  Total: {comp.m_total} kg aire húmedo")
    print(f"  N2: {comp.N2_pct}%")
    print(f"  O2: {comp.O2_pct}%")
    print(f"  H2O: {comp.H2O_pct}%")
