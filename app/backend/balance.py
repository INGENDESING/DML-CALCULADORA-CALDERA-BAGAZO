"""
Módulo de Balance - Balance de Materia y Energía
==================================================
Cálculo completo del balance de materia y energía de una
caldera acuotubular alimentada con bagazo.

DML INGENIEROS CONSULTORES S.A.S.
Autores: Jonathan Arboleda Genes, Herminsul Rosero
"""

from typing import NamedTuple
from dataclasses import dataclass
import math

# Importar módulos internos
from thermodynamics import (
    get_steam_properties,
    get_feedwater_properties,
    get_saturated_liquid_properties,
    calculate_stream_energy_from_tons
)
from bagazo import (
    calculate_calorific_value,
    get_bagazo_composition,
    BagazoAR,
    CalorificValue
)
from combustion import (
    calculate_flue_gas_flow,
    estimate_flue_gas_temperature
)
from psychrometry import (
    calculate_air_flow_for_fuel
)


# ═══════════════════════════════════════════════════════════════════════════════
# ESTRUCTURAS DE DATOS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class InputData:
    """Datos de entrada para el balance."""
    # Datos del proyecto
    project_code: str = "P2807"
    document_code: str = "P2807-PR-MC-001"
    analyst: str = ""
    date: str = ""

    # Datos de vapor
    m_stm: float = 100.0      # Flujo de vapor [t/h]
    P_stm: float = 106.0      # Presión de vapor [barg]
    T_stm: float = 545.0      # Temperatura de vapor [°C]
    T_fw: float = 270.0       # Temperatura agua alimentación [°C]
    pct_purge: float = 2.0    # Porcentaje de purga [%]
    efficiency: float = 94.0  # Eficiencia térmica [%]

    # Datos de bagazo
    bagazo_humidity: float = 48.0   # Humedad [%]
    bagazo_ash: float = 10.0        # Cenizas [%]

    # Datos de aire
    altitude: float = 1000.0   # Altitud [msnm]
    RH: float = 75.0           # Humedad relativa [%]
    T_amb: float = 30.0        # Temperatura ambiente [°C]
    excess_air: float = 20.0   # Exceso de aire [%]


@dataclass
class StreamResult:
    """Resultado de una corriente."""
    name: str
    m_th: float          # Flujo másico [t/h]
    T_celsius: float     # Temperatura [°C]
    energy_MW: float     # Energía [MW]
    composition: dict = None  # Composición si aplica


@dataclass
class BalanceResults:
    """Resultados completos del balance."""
    # Ratio principal
    ratio_stm_bagazo: float  # t_vapor / t_bagazo

    # Corrientes de entrada
    feedwater: StreamResult
    bagazo: StreamResult
    air: StreamResult

    # Corrientes de salida
    steam: StreamResult
    blowdown: StreamResult
    flue_gas: StreamResult
    ash: StreamResult

    # Energía
    Q_abs_MW: float        # Calor absorbido [MW]
    Q_fuel_MW: float       # Calor del combustible [MW]
    losses_MW: float       # Pérdidas [MW]

    # Propiedades del vapor
    steam_props: dict

    # Composición de gases
    flue_gas_composition: dict

    # Datos de entrada
    inputs: InputData


# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════

from thermodynamics import (
    get_steam_properties,
    get_feedwater_properties,
    get_saturated_liquid_properties,
    calculate_stream_energy_from_tons
)
from bagazo import (
    calculate_calorific_value,
    get_bagazo_composition,
    BagazoAR,
    CalorificValue
)
from combustion import (
    calculate_flue_gas_flow,
    estimate_flue_gas_temperature
)
from psychrometry import calculate_air_flow_for_fuel


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE CÁLCULO
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_water_side_balance(inputs: InputData) -> dict:
    """
    Calcula el balance de materia del lado agua.

    Parameters
    ----------
    inputs : InputData
        Datos de entrada

    Returns
    -------
    dict
        m_fw: agua alimentación [t/h]
        m_purge: purga [t/h]
        m_stm: vapor [t/h]
    """
    m_stm = inputs.m_stm
    pct_purge = inputs.pct_purge / 100

    # m_fw = m_stm / (1 - pct_purga)
    m_fw = m_stm / (1 - pct_purge)

    # m_purge = m_fw - m_stm
    m_purge = m_fw - m_stm

    return {
        'm_fw': round(m_fw, 2),
        'm_purge': round(m_purge, 2),
        'm_stm': round(m_stm, 2)
    }


def calculate_energy_balance(inputs: InputData, water_balance: dict) -> dict:
    """
    Calcula el balance de energía.

    Parameters
    ----------
    inputs : InputData
        Datos de entrada
    water_balance : dict
        Resultados del balance de agua

    Returns
    -------
    dict
        Q_abs: calor absorbido [MW]
        Q_fuel: calor del combustible [MW]
    """
    # Propiedades termodinámicas
    steam_props = get_steam_properties(inputs.P_stm, inputs.T_stm)
    fw_props = get_feedwater_properties(inputs.T_fw, inputs.P_stm + 5)  # Presión de bombeo
    purge_props = get_saturated_liquid_properties(inputs.P_stm)

    # Calor absorbido [MW]
    # Q_abs = m_stm*h_stm + m_purge*h_purge - m_fw*h_fw
    Q_steam = calculate_stream_energy_from_tons(water_balance['m_stm'], steam_props.h)
    Q_purge = calculate_stream_energy_from_tons(water_balance['m_purge'], purge_props.h)
    Q_fw = calculate_stream_energy_from_tons(water_balance['m_fw'], fw_props.h)

    Q_abs = Q_steam + Q_purge - Q_fw

    # Calor del combustible (considerando eficiencia)
    efficiency = inputs.efficiency / 100
    Q_fuel = Q_abs / efficiency

    return {
        'Q_abs_MW': round(Q_abs, 2),
        'Q_fuel_MW': round(Q_fuel, 2),
        'Q_steam_MW': round(Q_steam, 2),
        'Q_purge_MW': round(Q_purge, 2),
        'Q_fw_MW': round(Q_fw, 2),
        'steam_h': steam_props.h,
        'steam_s': steam_props.s,
        'steam_rho': steam_props.rho,
        'fw_h': fw_props.h,
        'purge_h': purge_props.h,
        'purge_T': purge_props.T
    }


def calculate_bagazo_consumption(Q_fuel_MW: float,
                                  bagazo_humidity: float,
                                  bagazo_ash: float) -> dict:
    """
    Calcula el consumo de bagazo.

    Parameters
    ----------
    Q_fuel_MW : float
        Calor requerido del combustible [MW]
    bagazo_humidity : float
        Humedad del bagazo [%]
    bagazo_ash : float
        Cenizas del bagazo [%]

    Returns
    -------
    dict
        m_bagazo_th: flujo de bagazo [t/h]
        m_bagazo_kgh: flujo de bagazo [kg/h]
        calorific_value: propiedades caloríficas
        composition: composición AR
    """
    # Poder calorífico
    cv = calculate_calorific_value(bagazo_humidity, bagazo_ash)

    # Consumo de bagazo [kg/h]
    # Q_fuel [MW] = Q_fuel [MJ/s] × 3600 [s/h] = Q_fuel [MJ/h]
    # PCI [kJ/kg] = PCI [MJ/kg] × 1000
    Q_fuel_MJh = Q_fuel_MW * 3600  # MJ/h
    PCI_MJ_kg = cv.PCI / 1000  # Convertir kJ/kg a MJ/kg
    m_bagazo_kgh = Q_fuel_MJh / PCI_MJ_kg  # kg/h

    # Convertir a t/h
    m_bagazo_th = m_bagazo_kgh / 1000

    # Composición AR
    comp_ar = get_bagazo_composition(bagazo_humidity, bagazo_ash)

    return {
        'm_bagazo_th': round(m_bagazo_th, 2),
        'm_bagazo_kgh': round(m_bagazo_kgh, 0),
        'calorific_value': cv,
        'composition': comp_ar,
        'bagazo_energy_MW': round(Q_fuel_MW, 2)
    }


def calculate_complete_balance(inputs: InputData) -> BalanceResults:
    """
    Realiza el cálculo completo del balance de materia y energía.

    Parameters
    ----------
    inputs : InputData
        Datos de entrada completos

    Returns
    -------
    BalanceResults
        Resultados completos del balance
    """
    # 1. Balance de agua
    water_bal = calculate_water_side_balance(inputs)

    # 2. Balance de energía
    energy_bal = calculate_energy_balance(inputs, water_bal)

    # 3. Consumo de bagazo
    bagazo_data = calculate_bagazo_consumption(
        energy_bal['Q_fuel_MW'],
        inputs.bagazo_humidity,
        inputs.bagazo_ash
    )

    # 4. Ratio principal
    ratio = inputs.m_stm / bagazo_data['m_bagazo_th']

    # 5. Gases de combustión (antes del aire, para obtener ratio correcto)
    comp_ar_dict = {
        'C': bagazo_data['composition'].C / 100,
        'H': bagazo_data['composition'].H / 100,
        'O': bagazo_data['composition'].O / 100,
        'N': bagazo_data['composition'].N / 100,
        'S': bagazo_data['composition'].S / 100,
        'A': bagazo_data['composition'].A / 100,
        'W': bagazo_data['composition'].W / 100
    }

    flue_gas_data = calculate_flue_gas_flow(
        bagazo_data['m_bagazo_kgh'],
        comp_ar_dict,
        inputs.excess_air
    )

    # 6. Aire de combustión (ratio real desde combustión con excess_air del usuario)
    air_per_kg_bagazo = flue_gas_data['combustion'].air.m_actual

    air_data = calculate_air_flow_for_fuel(
        bagazo_data['m_bagazo_kgh'],
        air_per_kg_bagazo,
        inputs.altitude,
        inputs.T_amb,
        inputs.RH
    )

    # Temperatura de gases
    T_flue = estimate_flue_gas_temperature(inputs.excess_air, inputs.bagazo_humidity)

    # Energía de gases de salida [MW]
    # Cp ponderado por composición másica de gases
    comp_wet = flue_gas_data['composition_wet']  # porcentajes másicos
    Cp_gas = (
        comp_wet['CO2'] * 0.846 +
        comp_wet['H2O'] * 1.890 +
        comp_wet['N2']  * 1.040 +
        comp_wet['O2']  * 0.920 +
        comp_wet['SO2'] * 0.640
    ) / 100  # dividir por 100 porque comp_wet está en %

    m_flue_kgh = flue_gas_data['flows']['total_wet']
    Q_flue_MW = round(m_flue_kgh * Cp_gas * (T_flue - inputs.T_amb) / 3_600_000, 2)

    # 7. Cenizas
    m_ash_th = bagazo_data['m_bagazo_th'] * (inputs.bagazo_ash / 100)

    # 8. Crear objetos de resultado

    # Corrientes de entrada
    feedwater = StreamResult(
        name="Agua de Alimentación",
        m_th=water_bal['m_fw'],
        T_celsius=inputs.T_fw,
        energy_MW=energy_bal['Q_fw_MW']
    )

    bagazo = StreamResult(
        name="Bagazo (AR)",
        m_th=bagazo_data['m_bagazo_th'],
        T_celsius=inputs.T_amb,
        energy_MW=bagazo_data['bagazo_energy_MW'],
        composition={
            'C': bagazo_data['composition'].C,
            'H': bagazo_data['composition'].H,
            'O': bagazo_data['composition'].O,
            'N': bagazo_data['composition'].N,
            'S': bagazo_data['composition'].S,
            'Ash': bagazo_data['composition'].A,
            'H2O': bagazo_data['composition'].W,
            'PCI_MJ_kg': bagazo_data['calorific_value'].PCI_MJ
        }
    )

    air = StreamResult(
        name="Aire de Combustión",
        m_th=air_data['flows']['air_total_th'],
        T_celsius=inputs.T_amb,
        energy_MW=0,  # No se cuenta energía del aire
        composition=air_data['composition']
    )

    # Corrientes de salida
    steam = StreamResult(
        name="Vapor Sobrecalentado",
        m_th=inputs.m_stm,
        T_celsius=inputs.T_stm,
        energy_MW=energy_bal['Q_steam_MW']
    )

    blowdown = StreamResult(
        name="Purga Continua",
        m_th=water_bal['m_purge'],
        T_celsius=energy_bal['purge_T'],
        energy_MW=energy_bal['Q_purge_MW']
    )

    flue_gas = StreamResult(
        name="Gases de Combustión",
        m_th=flue_gas_data['flows']['total_wet'] / 1000,
        T_celsius=T_flue,
        energy_MW=Q_flue_MW,
        composition=flue_gas_data['composition_wet']
    )

    ash_stream = StreamResult(
        name="Cenizas",
        m_th=m_ash_th,
        T_celsius=T_flue,
        energy_MW=0
    )

    # Propiedades del vapor
    steam_props = {
        'h': energy_bal['steam_h'],
        's': energy_bal['steam_s'],
        'rho': energy_bal['steam_rho'],
        'P': inputs.P_stm
    }

    return BalanceResults(
        ratio_stm_bagazo=round(ratio, 3),
        feedwater=feedwater,
        bagazo=bagazo,
        air=air,
        steam=steam,
        blowdown=blowdown,
        flue_gas=flue_gas,
        ash=ash_stream,
        Q_abs_MW=energy_bal['Q_abs_MW'],
        Q_fuel_MW=energy_bal['Q_fuel_MW'],
        losses_MW=round(energy_bal['Q_fuel_MW'] - energy_bal['Q_abs_MW'], 2),
        steam_props=steam_props,
        flue_gas_composition=flue_gas_data['composition_wet'],
        inputs=inputs
    )


def format_results_table(results: BalanceResults) -> str:
    """Formatea los resultados como tabla Markdown."""
    return f"""
# BALANCE DE MATERIA Y ENERGÍA

## Datos de Entrada
| Parámetro | Valor |
|-----------|-------|
| Código Proyecto | {results.inputs.project_code} |
| Flujo de vapor | {results.inputs.m_stm} t/h |
| Presión vapor | {results.inputs.P_stm} barg |
| Temperatura vapor | {results.inputs.T_stm} °C |
| Temperatura agua alim. | {results.inputs.T_fw} °C |
| Purga continua | {results.inputs.pct_purge} % |
| Eficiencia térmica | {results.inputs.efficiency} % |
| Humedad bagazo | {results.inputs.bagazo_humidity} % |
| Cenizas bagazo | {results.inputs.bagazo_ash} % |

## Resultados Principales
| Parámetro | Valor |
|-----------|-------|
| **RATIO VAPOR/BAGAZO** | **{results.ratio_stm_bagazo} t/t** |
| Flujo bagazo | {results.bagazo.m_th} t/h |
| Flujo agua alim. | {results.feedwater.m_th} t/h |
| Flujo purga | {results.blowdown.m_th} t/h |
| Q absorbido | {results.Q_abs_MW} MW |
| Q combustible | {results.Q_fuel_MW} MW |
| Pérdidas | {results.losses_MW} MW |

## Balance de Energía
| Corriente | Flujo [t/h] | T [°C] | Energía [MW] |
|-----------|-------------|--------|--------------|
| **ENTRADAS** | | | |
| Agua alimentación | {results.feedwater.m_th} | {results.feedwater.T_celsius} | {results.feedwater.energy_MW} |
| Bagazo | {results.bagazo.m_th} | {results.bagazo.T_celsius} | {results.bagazo.energy_MW} |
| Aire combustión | {results.air.m_th} | {results.air.T_celsius} | - |
| **SALIDAS** | | | |
| Vapor sobrecalentado | {results.steam.m_th} | {results.steam.T_celsius} | {results.steam.energy_MW} |
| Purga continua | {results.blowdown.m_th} | {results.blowdown.T_celsius} | {results.blowdown.energy_MW} |
| Gases combustión | {results.flue_gas.m_th} | {results.flue_gas.T_celsius} | Pérdidas |
| Cenizas | {results.ash.m_th} | {results.ash.T_celsius} | - |
"""


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDACIÓN CON DATOS BASE
# ═══════════════════════════════════════════════════════════════════════════════

def validate_with_base_case() -> dict:
    """
    Valida los cálculos con los datos base del proyecto.

    Returns
    -------
    dict
        Resultados de validación
    """
    # Datos base
    inputs = InputData(
        m_stm=100.0,
        P_stm=106.0,
        T_stm=545.0,
        T_fw=270.0,
        pct_purge=2.0,
        efficiency=94.0,
        bagazo_humidity=48.0,
        bagazo_ash=10.0,
        altitude=1000.0,
        RH=75.0,
        T_amb=30.0,
        excess_air=20.0
    )

    results = calculate_complete_balance(inputs)

    expected_ratio = 2.655

    return {
        'ratio_calculated': results.ratio_stm_bagazo,
        'ratio_expected': expected_ratio,
        'error_percent': abs(results.ratio_stm_bagazo - expected_ratio) / expected_ratio * 100,
        'valid': abs(results.ratio_stm_bagazo - expected_ratio) < 0.05,
        'm_bagazo': results.bagazo.m_th,
        'm_bagazo_expected': 37.67,
        'Q_abs': results.Q_abs_MW,
        'Q_fuel': results.Q_fuel_MW
    }


if __name__ == "__main__":
    # Prueba de validación
    print("=== VALIDACIÓN BALANCE COMPLETO ===\n")

    validation = validate_with_base_case()

    print(f"Ratio Vapor/Bagazo: {validation['ratio_calculated']}")
    print(f"Ratio Esperado: {validation['ratio_expected']}")
    print(f"Error: {validation['error_percent']:.2f}%")
    print(f"Válido: {'SÍ' if validation['valid'] else 'NO'}")

    print(f"\nFlujo bagazo: {validation['m_bagazo']} t/h (esperado: 37.67)")
    print(f"Q absorbido: {validation['Q_abs']} MW")
    print(f"Q combustible: {validation['Q_fuel']} MW")
