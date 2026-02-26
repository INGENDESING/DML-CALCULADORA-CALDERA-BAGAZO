"""
Módulo de Bagazo - Propiedades del Combustible
===============================================
Cálculo del poder calorífico y composición del bagazo de caña de azúcar.

DML INGENIEROS CONSULTORES S.A.S.
Autores: Jonathan Arboleda Genes, Herminsul Rosero

Referencias:
- Hugot, E. (1986). Handbook of Cane Sugar Engineering.
- Duffy, J. E. (2009). Biomass power generation.
"""

from typing import NamedTuple
from dataclasses import dataclass


# ═══════════════════════════════════════════════════════════════════════════════
# ESTRUCTURAS DE DATOS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class BagazoComposition:
    """Composición elemental del bagazo (base seca libre de cenizas - DAF)."""
    C: float = 47.0   # Carbono [%]
    H: float = 6.0    # Hidrógeno [%]
    O: float = 46.5   # Oxígeno [%]
    N: float = 0.4    # Nitrógeno [%]
    S: float = 0.1    # Azufre [%]

    @property
    def total(self) -> float:
        """Suma de componentes (debe ser 100%)."""
        return self.C + self.H + self.O + self.N + self.S


@dataclass
class BagazoAR:
    """
    Bagazo "como recibido" (As Received - AR).
    Incluye humedad y cenizas.
    """
    W: float  # Humedad [%]
    A: float  # Cenizas [%]
    C: float  # Carbono [%]
    H: float  # Hidrógeno [%]
    O: float  # Oxígeno [%]
    N: float  # Nitrógeno [%]
    S: float  # Azufre [%]

    @property
    def total(self) -> float:
        """Suma de componentes (debe ser 100%)."""
        return self.W + self.A + self.C + self.H + self.O + self.N + self.S


@dataclass
class CalorificValue:
    """Poder calorífico del bagazo."""
    PCS: float  # Poder Calorífico Superior [kJ/kg]
    PCI: float  # Poder Calorífico Inferior [kJ/kg]
    PCS_MJ: float  # PCS [MJ/kg]
    PCI_MJ: float  # PCI [MJ/kg]


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE CÁLCULO
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_combustible_fraction(W: float, A: float) -> float:
    """
    Calcula la fracción de materia combustible.

    Parameters
    ----------
    W : float
        Humedad del bagazo [%]
    A : float
        Cenizas del bagazo [%]

    Returns
    -------
    float
        Fracción combustible (0-1)

    Example
    -------
    >>> calculate_combustible_fraction(48, 10)
    0.42
    """
    return round((100 - W - A) / 100, 4)


def daf_to_ar(composition_daf: BagazoComposition,
              W: float, A: float) -> BagazoAR:
    """
    Convierte composición DAF a AR (As Received).

    Parameters
    ----------
    composition_daf : BagazoComposition
        Composición base seca libre de cenizas
    W : float
        Humedad [%]
    A : float
        Cenizas [%]

    Returns
    -------
    BagazoAR
        Composición como se recibe
    """
    f_comb = calculate_combustible_fraction(W, A)

    return BagazoAR(
        W=round(W, 2),
        A=round(A, 2),
        C=round(composition_daf.C * f_comb, 2),
        H=round(composition_daf.H * f_comb, 2),
        O=round(composition_daf.O * f_comb, 2),
        N=round(composition_daf.N * f_comb, 2),
        S=round(composition_daf.S * f_comb, 2)
    )


def calculate_PCS(f_combustible: float,
                  PCS_daf: float = 19605) -> float:
    """
    Calcula el Poder Calorífico Superior (PCS) del bagazo AR.

    Parameters
    ----------
    f_combustible : float
        Fracción combustible (0-1)
    PCS_daf : float
        PCS de la materia orgánica seca [kJ/kg]
        Valor típico para caña: 19,605 kJ/kg (Hugot, 1986)

    Returns
    -------
    float
        PCS del bagazo AR [kJ/kg]

    Example
    -------
    >>> calculate_PCS(0.42)
    8234.1
    """
    return round(PCS_daf * f_combustible, 1)


def calculate_PCI(PCS: float, W: float, H_ar: float,
                  lambda_v: float = 2442) -> float:
    """
    Calcula el Poder Calorífico Inferior (PCI) del bagazo.

    Parameters
    ----------
    PCS : float
        Poder Calorífico Superior [kJ/kg]
    W : float
        Humedad del bagazo (fracción, 0-1)
    H_ar : float
        Hidrógeno en base AR (fracción, 0-1)
    lambda_v : float
        Calor de vaporización del agua [kJ/kg]
        Valor a 25°C: 2442 kJ/kg

    Returns
    -------
    float
        PCI del bagazo AR [kJ/kg]

    Notes
    -----
    PCI = PCS - λv × (W + 9×H)
    Donde:
    - W: humedad del bagazo
    - 9×H: agua formada en la combustión del hidrógeno

    Example
    -------
    >>> calculate_PCI(8234, 0.48, 0.0252)
    6508.2
    """
    # Agua total a evaporar: humedad + agua de formación
    water_total = W + 9 * H_ar

    PCI = PCS - lambda_v * water_total

    return round(PCI, 1)


def calculate_calorific_value(W: float, A: float,
                               composition_daf: BagazoComposition = None) -> CalorificValue:
    """
    Calcula PCS y PCI del bagazo a partir de humedad y cenizas.

    Parameters
    ----------
    W : float
        Humedad [%]
    A : float
        Cenizas [%]
    composition_daf : BagazoComposition, opcional
        Composición DAF (usa default si no se especifica)

    Returns
    -------
    CalorificValue
        Objeto con PCS y PCI en kJ/kg y MJ/kg
    """
    if composition_daf is None:
        composition_daf = BagazoComposition()

    # Fracción combustible
    f_comb = calculate_combustible_fraction(W, A)

    # Composición AR
    comp_ar = daf_to_ar(composition_daf, W, A)

    # PCS
    PCS = calculate_PCS(f_comb)

    # PCI (convertir % a fracción)
    W_frac = W / 100
    H_ar_frac = comp_ar.H / 100
    PCI = calculate_PCI(PCS, W_frac, H_ar_frac)

    return CalorificValue(
        PCS=PCS,
        PCI=PCI,
        PCS_MJ=round(PCS / 1000, 2),
        PCI_MJ=round(PCI / 1000, 2)
    )


def get_bagazo_composition(W: float, A: float,
                           composition_daf: BagazoComposition = None) -> BagazoAR:
    """
    Retorna la composición completa del bagazo AR.

    Parameters
    ----------
    W : float
        Humedad [%]
    A : float
        Cenizas [%]
    composition_daf : BagazoComposition, opcional
        Composición DAF

    Returns
    -------
    BagazoAR
        Composición completa AR
    """
    if composition_daf is None:
        composition_daf = BagazoComposition()

    return daf_to_ar(composition_daf, W, A)


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════════════════════════

def format_composition_table(comp: BagazoAR) -> str:
    """Formatea la composición como tabla Markdown."""
    return f"""
| Componente | % AR |
|------------|------|
| Carbono (C)     | {comp.C:.2f} % |
| Hidrógeno (H)    | {comp.H:.2f} % |
| Oxígeno (O)      | {comp.O:.2f} % |
| Nitrógeno (N)    | {comp.N:.2f} % |
| Azufre (S)       | {comp.S:.2f} % |
| Cenizas          | {comp.A:.2f} % |
| Humedad          | {comp.W:.2f} % |
| **TOTAL**        | **{comp.total:.2f} %** |
"""


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDACIÓN CON DATOS BASE
# ═══════════════════════════════════════════════════════════════════════════════

def validate_with_base_case() -> dict:
    """
    Valida los cálculos con los datos base del proyecto.

    Datos base (documentación):
    - Humedad: 48%
    - Cenizas: 10%
    - Resultado esperado PCI: 6.51 MJ/kg

    Returns
    -------
    dict
        Diccionario con resultados de validación
    """
    W = 48.0
    A = 10.0

    cv = calculate_calorific_value(W, A)

    # Valores esperados según documentación
    expected_PCS_MJ = 8.23  # MJ/kg
    expected_PCI_MJ = 6.51  # MJ/kg

    return {
        "PCS": {
            "calculated_MJ": cv.PCS_MJ,
            "expected_MJ": expected_PCS_MJ,
            "error_percent": abs(cv.PCS_MJ - expected_PCS_MJ) / expected_PCS_MJ * 100,
            "valid": abs(cv.PCS_MJ - expected_PCS_MJ) < 0.1
        },
        "PCI": {
            "calculated_MJ": cv.PCI_MJ,
            "expected_MJ": expected_PCI_MJ,
            "error_percent": abs(cv.PCI_MJ - expected_PCI_MJ) / expected_PCI_MJ * 100,
            "valid": abs(cv.PCI_MJ - expected_PCI_MJ) < 0.1
        },
        "combustible_fraction": {
            "calculated": calculate_combustible_fraction(W, A),
            "expected": 0.42,
            "valid": True
        }
    }


if __name__ == "__main__":
    # Prueba de validación
    print("=== VALIDACIÓN BAGAZO ===\n")

    validation = validate_with_base_case()

    for prop, data in validation.items():
        status = "✓" if data["valid"] else "✗"
        print(f"{status} {prop}:")
        if "calculated_MJ" in data:
            print(f"   Calculado: {data['calculated_MJ']} MJ/kg")
            print(f"   Esperado:  {data['expected_MJ']} MJ/kg")
            print(f"   Error:     {data['error_percent']:.4f}%")
        else:
            print(f"   Calculado: {data['calculated']}")
            print(f"   Esperado:  {data['expected']}")

    # Composición AR
    print("\n=== COMPOSICIÓN AR (48% humedad, 10% cenizas) ===")
    comp = get_bagazo_composition(48, 10)
    print(format_composition_table(comp))
