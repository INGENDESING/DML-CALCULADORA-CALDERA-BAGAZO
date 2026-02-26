"""
Módulo de Combustión - Cálculos de Aire y Gases
=================================================
Cálculo estequiométrico de combustión del bagazo, incluyendo
aire teórico, aire real con exceso, y composición de gases.

DML INGENIEROS CONSULTORES S.A.S.
Autores: Jonathan Arboleda Genes, Herminsul Rosero

Referencias:
- Perry, R. H. (1997). Perry's Chemical Engineers' Handbook.
- Hugot, E. (1986). Handbook of Cane Sugar Engineering.
"""

from typing import NamedTuple
from dataclasses import dataclass
import math


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════

# Pesos moleculares [kg/kmol]
MW = {
    'C': 12.01,
    'H': 1.008,
    'O': 16.00,
    'N': 14.01,
    'S': 32.06,
    'H2O': 18.015,
    'CO2': 44.01,
    'SO2': 64.06,
    'N2': 28.013,
    'O2': 31.999,
    'AIR': 28.97  # Peso molecular promedio del aire
}

# Composición del aire seco (volumen o fracción molar)
AIR_COMPOSITION = {
    'N2': 0.7809,   # 78.09%
    'O2': 0.2095,   # 20.95%
    'Ar': 0.0093,   # 0.93% (Argón)
    'CO2': 0.0003   # 0.03% (trazas)
}

# Fracción de N2/O2 en aire seco (simplificado)
N2_O2_RATIO = 0.79 / 0.21  # 3.76


# ═══════════════════════════════════════════════════════════════════════════════
# ESTRUCTURAS DE DATOS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class FlueGasDry:
    """Composición de gases de combustión secos."""
    CO2: float  # Dióxido de carbono [kg/kg combustible]
    SO2: float  # Dióxido de azufre [kg/kg combustible]
    N2: float   # Nitrógeno [kg/kg combustible]
    O2: float   # Oxígeno (por exceso) [kg/kg combustible]

    @property
    def total(self) -> float:
        return self.CO2 + self.SO2 + self.N2 + self.O2


@dataclass
class FlueGasWet:
    """Composición de gases de combustión húmedos."""
    CO2: float  # Dióxido de carbono [kg/kg combustible]
    H2O: float  # Agua [kg/kg combustible]
    SO2: float  # Dióxido de azufre [kg/kg combustible]
    N2: float   # Nitrógeno [kg/kg combustible]
    O2: float   # Oxígeno (por exceso) [kg/kg combustible]

    @property
    def total(self) -> float:
        return self.CO2 + self.H2O + self.SO2 + self.N2 + self.O2


@dataclass
class CombustionAir:
    """Requerimientos de aire de combustión."""
    m_theoretical: float  # Aire teórico [kg aire/kg combustible]
    m_actual: float       # Aire real [kg aire/kg combustible]
    excess_air_pct: float # Exceso de aire [%]
    O2_required: float    # O2 teórico [kg O2/kg combustible]
    N2_from_air: float    # N2 del aire [kg N2/kg combustible]


@dataclass
class CombustionProducts:
    """Productos completos de combustión."""
    air: CombustionAir
    flue_gas_dry: FlueGasDry
    flue_gas_wet: FlueGasWet


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE CÁLCULO
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_stoichiometric_oxygen(C_ar: float, H_ar: float,
                                    S_ar: float, O_ar: float) -> float:
    """
    Calcula el O2 teórico requerido para combustión completa.

    Parameters
    ----------
    C_ar, H_ar, S_ar, O_ar : float
        Composición del combustible (fracción másica, 0-1)

    Returns
    -------
    float
        O2 requerido [kg O2/kg combustible]

    Notes
    -----
    Reacciones:
        C + O2 → CO2
        H + 0.25×O2 → 0.5×H2O
        S + O2 → SO2
        O del combustible reduce el requerimiento

    O2_req = (32/12)×C + (32/4)×H + (32/32)×S - O
    """
    # (32/12) = 2.667 para C → CO2
    # (32/4) = 8.0 para H → H2O
    # (32/32) = 1.0 para S → SO2
    O2_req = (32/12) * C_ar + 8.0 * H_ar + 1.0 * S_ar - O_ar

    return round(O2_req, 4)


def calculate_theoretical_air(O2_required: float) -> float:
    """
    Calcula el aire teórico requerido.

    Parameters
    ----------
    O2_required : float
        O2 requerido [kg O2/kg combustible]

    Returns
    -------
    float
        Aire teórico [kg aire/kg combustible]

    Notes
    -----
    Aire contiene ~23.3% O2 en masa
    """
    # Aire contiene 23.2% O2 en masa (simplificado: 0.232)
    air_theoretical = O2_required / 0.232

    return round(air_theoretical, 4)


def calculate_actual_air(air_theoretical: float,
                         excess_air_pct: float) -> tuple:
    """
    Calcula el aire real con exceso.

    Parameters
    ----------
    air_theoretical : float
        Aire teórico [kg aire/kg combustible]
    excess_air_pct : float
        Exceso de aire [%]

    Returns
    -------
    tuple
        (aire_real, O2_exceso, N2_entrada)
    """
    excess_factor = 1 + excess_air_pct / 100
    air_actual = air_theoretical * excess_factor

    # O2 en exceso
    O2_excess = air_theoretical * (excess_air_pct / 100) * 0.232

    # N2 total del aire (79% en masa del aire sin O2)
    N2_from_air = air_actual * 0.768

    return (round(air_actual, 4), round(O2_excess, 4), round(N2_from_air, 4))


def calculate_flue_gas_masses(C_ar: float, H_ar: float, S_ar: float,
                               O_ar: float, N_ar: float, A_ar: float,
                               W_ar: float,
                               excess_air_pct: float) -> CombustionProducts:
    """
    Calcula la composición de los gases de combustión.

    Parameters
    ----------
    C_ar, H_ar, S_ar, O_ar, N_ar, A_ar, W_ar : float
        Composición del combustible (fracción másica, 0-1)
    excess_air_pct : float
        Exceso de aire [%]

    Returns
    -------
    CombustionProducts
        Objeto con aire y gases de combustión
    """
    # 1. O2 teórico requerido
    O2_req = calculate_stoichiometric_oxygen(C_ar, H_ar, S_ar, O_ar)

    # 2. Aire teórico y real
    air_th = calculate_theoretical_air(O2_req)
    air_act, O2_exc, N2_air = calculate_actual_air(air_th, excess_air_pct)

    # 3. Productos de combustión (por kg de combustible)

    # CO2 del carbono
    CO2 = C_ar * (MW['CO2'] / MW['C'])  # 44.01/12.01 = 3.664

    # H2O del hidrógeno + humedad del combustible
    H2O_from_H = H_ar * (MW['H2O'] / (2 * MW['H']))  # 9.0
    H2O_total = H2O_from_H + W_ar

    # SO2 del azufre
    SO2 = S_ar * (MW['SO2'] / MW['S'])  # 2.0

    # N2 del aire (que ingresa)
    N2 = N2_air

    # O2 en exceso (sale sin reaccionar)
    O2 = O2_exc

    # Cenizas (inertes)
    Ash = A_ar

    # Crear objetos
    flue_dry = FlueGasDry(
        CO2=round(CO2, 4),
        SO2=round(SO2, 4),
        N2=round(N2, 4),
        O2=round(O2, 4)
    )

    flue_wet = FlueGasWet(
        CO2=round(CO2, 4),
        H2O=round(H2O_total, 4),
        SO2=round(SO2, 4),
        N2=round(N2, 4),
        O2=round(O2, 4)
    )

    air_obj = CombustionAir(
        m_theoretical=air_th,
        m_actual=air_act,
        excess_air_pct=excess_air_pct,
        O2_required=O2_req,
        N2_from_air=N2_air
    )

    return CombustionProducts(
        air=air_obj,
        flue_gas_dry=flue_dry,
        flue_gas_wet=flue_wet
    )


def calculate_flue_gas_flow(m_fuel_kgh: float,
                            composition_ar: dict,
                            excess_air_pct: float) -> dict:
    """
    Calcula el flujo másico de gases de combustión.

    Parameters
    ----------
    m_fuel_kgh : float
        Flujo de combustible [kg/h]
    composition_ar : dict
        Composición AR del combustible (fracciones 0-1)
        Claves: 'C', 'H', 'O', 'N', 'S', 'A', 'W'
    excess_air_pct : float
        Exceso de aire [%]

    Returns
    -------
    dict
        Flujos de gases [kg/h] y composición porcentual
    """
    # Obtener productos de combustión
    products = calculate_flue_gas_masses(
        composition_ar['C'], composition_ar['H'], composition_ar['S'],
        composition_ar['O'], composition_ar['N'], composition_ar['A'],
        composition_ar['W'], excess_air_pct
    )

    # Flujos másicos
    m_CO2 = products.flue_gas_wet.CO2 * m_fuel_kgh
    m_H2O = products.flue_gas_wet.H2O * m_fuel_kgh
    m_SO2 = products.flue_gas_wet.SO2 * m_fuel_kgh
    m_N2 = products.flue_gas_wet.N2 * m_fuel_kgh
    m_O2 = products.flue_gas_wet.O2 * m_fuel_kgh
    m_Ash = composition_ar['A'] * m_fuel_kgh

    m_total_wet = m_CO2 + m_H2O + m_SO2 + m_N2 + m_O2
    m_total_dry = m_CO2 + m_SO2 + m_N2 + m_O2

    return {
        'flows': {
            'CO2': round(m_CO2, 2),
            'H2O': round(m_H2O, 2),
            'SO2': round(m_SO2, 2),
            'N2': round(m_N2, 2),
            'O2': round(m_O2, 2),
            'Ash': round(m_Ash, 2),
            'total_wet': round(m_total_wet, 2),
            'total_dry': round(m_total_dry, 2)
        },
        'composition_wet': {
            'CO2': round(m_CO2 / m_total_wet * 100, 2),
            'H2O': round(m_H2O / m_total_wet * 100, 2),
            'SO2': round(m_SO2 / m_total_wet * 100, 2),
            'N2': round(m_N2 / m_total_wet * 100, 2),
            'O2': round(m_O2 / m_total_wet * 100, 2),
        },
        'combustion': products
    }


def estimate_flue_gas_temperature(T_steam: float, excess_air: float) -> float:
    """
    Estima la temperatura de gases de combustión.

    Parameters
    ----------
    T_steam : float
        Temperatura del vapor [°C]
    excess_air : float
        Exceso de aire [%]

    Returns
    -------
    float
        Temperatura estimada de gases [°C]

    Notes
    -----
    Estimación empírica para calderas bagaceras.
    T_gases ≈ T_steam - 10 + (excess_air / 5)
    """
    # Base: vapor - 10°C
    T_base = T_steam - 10

    # Penalización por exceso de aire
    T_penalty = excess_air / 5

    return round(T_base + T_penalty, 1)


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDACIÓN CON DATOS BASE
# ═══════════════════════════════════════════════════════════════════════════════

def validate_with_base_case() -> dict:
    """
    Valida los cálculos con los datos base del proyecto.

    Datos base (documentación):
    - Bagazo: C=19.74%, H=2.52%, O=19.53%, N=0.17%, S=0.04%, A=10%, W=48%
    - Exceso de aire: 20%

    Returns
    -------
    dict
        Diccionario con resultados de validación
    """
    # Composición AR (fracciones)
    comp_ar = {
        'C': 0.1974,
        'H': 0.0252,
        'O': 0.1953,
        'N': 0.0017,
        'S': 0.0004,
        'A': 0.10,
        'W': 0.48
    }

    products = calculate_flue_gas_masses(
        comp_ar['C'], comp_ar['H'], comp_ar['S'],
        comp_ar['O'], comp_ar['N'], comp_ar['A'],
        comp_ar['W'], 20.0
    )

    return {
        'air_theoretical': round(products.air.m_theoretical, 3),
        'air_actual': round(products.air.m_actual, 3),
        'excess_air': products.air.excess_air_pct,
        'O2_required': round(products.air.O2_required, 3),
        'flue_gas_CO2': products.flue_gas_dry.CO2,
        'flue_gas_SO2': products.flue_gas_dry.SO2,
        'flue_gas_N2': products.flue_gas_dry.N2,
        'flue_gas_O2': products.flue_gas_dry.O2,
        'flue_gas_H2O': products.flue_gas_wet.H2O
    }


if __name__ == "__main__":
    # Prueba de validación
    print("=== VALIDACIÓN COMBUSTIÓN ===\n")

    results = validate_with_base_case()

    print(f"Aire teórico: {results['air_theoretical']} kg aire/kg bagazo")
    print(f"Aire real: {results['air_actual']} kg aire/kg bagazo")
    print(f"O2 requerido: {results['O2_required']} kg O2/kg bagazo")
    print(f"\nGases de combustión (por kg bagazo):")
    print(f"  CO2: {results['flue_gas_CO2']} kg")
    print(f"  H2O: {results['flue_gas_H2O']} kg")
    print(f"  SO2: {results['flue_gas_SO2']} kg")
    print(f"  N2:  {results['flue_gas_N2']} kg")
    print(f"  O2:  {results['flue_gas_O2']} kg")
