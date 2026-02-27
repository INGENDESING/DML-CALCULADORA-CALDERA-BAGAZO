"""
Tests Unitarios - Módulo de Combustión
=======================================
Pruebas para validar los cálculos de combustión del bagazo,
aire teórico, aire real, y composición de gases.

DML INGENIEROS CONSULTORES S.A.S.
"""

import unittest
import sys
import os

# Agregar el path del backend al sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from combustion import (
    calculate_stoichiometric_oxygen,
    calculate_theoretical_air,
    calculate_actual_air,
    calculate_flue_gas_masses,
    calculate_flue_gas_flow,
    estimate_flue_gas_temperature,
    validate_with_base_case,
    FlueGasDry,
    FlueGasWet,
    CombustionAir,
    CombustionProducts
)


class TestStoichiometricOxygen(unittest.TestCase):
    """Tests para cálculo de O2 estequiométrico."""

    def test_o2_required_for_pure_carbon(self):
        """Verifica O2 requerido para carbono puro."""
        # C + O2 → CO2
        # O2_req = (32/12) * C = 2.667 * 1.0 = 2.667
        result = calculate_stoichiometric_oxygen(1.0, 0, 0, 0)
        self.assertAlmostEqual(result, 2.667, places=3)

    def test_o2_required_for_pure_hydrogen(self):
        """Verifica O2 requerido para hidrógeno puro."""
        # H + 0.25*O2 → 0.5*H2O
        # O2_req = 8.0 * H = 8.0 * 1.0 = 8.0
        result = calculate_stoichiometric_oxygen(0, 1.0, 0, 0)
        self.assertAlmostEqual(result, 8.0, places=3)

    def test_o2_required_for_pure_sulfur(self):
        """Verifica O2 requerido para azufre puro."""
        # S + O2 → SO2
        # O2_req = 1.0 * S = 1.0 * 1.0 = 1.0
        result = calculate_stoichiometric_oxygen(0, 0, 1.0, 0)
        self.assertAlmostEqual(result, 1.0, places=3)

    def test_o2_reduced_by_fuel_oxygen(self):
        """Verifica que el O2 del combustible reduce el requerimiento."""
        # El oxígeno del combustible resta del requerimiento
        result_with_O = calculate_stoichiometric_oxygen(0.5, 0, 0, 0.1)
        result_without_O = calculate_stoichiometric_oxygen(0.5, 0, 0, 0)
        self.assertLess(result_with_O, result_without_O)


class TestTheoreticalAir(unittest.TestCase):
    """Tests para cálculo de aire teórico."""

    def test_air_theoretical_calculation(self):
        """Verifica cálculo de aire teórico."""
        # Aire contiene 23.2% O2 en masa
        # Aire = O2 / 0.232
        O2_req = 1.0  # kg O2/kg combustible
        result = calculate_theoretical_air(O2_req)
        expected = 1.0 / 0.232
        self.assertAlmostEqual(result, expected, places=3)

    def test_air_theoretical_proportional_to_o2(self):
        """Verifica que el aire sea proporcional al O2 requerido."""
        air1 = calculate_theoretical_air(0.5)
        air2 = calculate_theoretical_air(1.0)
        self.assertAlmostEqual(air2, 2 * air1, places=3)


class TestActualAir(unittest.TestCase):
    """Tests para cálculo de aire real con exceso."""

    def test_air_actual_with_no_excess(self):
        """Verifica aire real sin exceso (0% exceso)."""
        air_th = 10.0
        air_act, O2_exc, N2_air = calculate_actual_air(air_th, 0)
        self.assertAlmostEqual(air_act, air_th, places=3)
        self.assertAlmostEqual(O2_exc, 0, places=3)

    def test_air_actual_with_excess(self):
        """Verifica aire real con 20% exceso."""
        air_th = 10.0
        air_act, O2_exc, N2_air = calculate_actual_air(air_th, 20)
        expected = 10.0 * 1.2  # 20% exceso
        self.assertAlmostEqual(air_act, expected, places=3)

    def test_n2_from_air_reasonable(self):
        """Verifica que el N2 del aire sea razonable."""
        air_th = 10.0
        air_act, O2_exc, N2_air = calculate_actual_air(air_th, 20)
        # N2 es ~76.8% del aire
        expected_N2 = air_act * 0.768
        self.assertAlmostEqual(N2_air, expected_N2, places=2)


class TestFlueGasMasses(unittest.TestCase):
    """Tests para composición de gases de combustión."""

    def test_flue_gas_returns_combustion_products(self):
        """Verifica que retorna un objeto CombustionProducts."""
        comp = {
            'C': 0.5, 'H': 0.05, 'S': 0.001, 'O': 0.4,
            'N': 0.01, 'A': 0.03, 'W': 0.009
        }
        result = calculate_flue_gas_masses(
            comp['C'], comp['H'], comp['S'], comp['O'],
            comp['N'], comp['A'], comp['W'], 20.0
        )
        self.assertIsInstance(result, CombustionProducts)
        self.assertIsInstance(result.air, CombustionAir)
        self.assertIsInstance(result.flue_gas_dry, FlueGasDry)
        self.assertIsInstance(result.flue_gas_wet, FlueGasWet)

    def test_co2_from_carbon(self):
        """Verifica cálculo de CO2 a partir del carbono."""
        # CO2 = C * (44.01/12.01) = C * 3.664
        C_ar = 0.5
        result = calculate_flue_gas_masses(C_ar, 0, 0, 0, 0, 0, 0, 20)
        expected_CO2 = C_ar * (44.01 / 12.01)
        self.assertAlmostEqual(result.flue_gas_dry.CO2, expected_CO2, places=3)

    def test_h2o_from_hydrogen_and_moisture(self):
        """Verifica cálculo de H2O del hidrógeno y humedad."""
        # H2O_from_H = H * (18.015 / 2.016) = H * 9.0 (aprox)
        H_ar = 0.05
        W_ar = 0.10
        result = calculate_flue_gas_masses(0, H_ar, 0, 0, 0, 0, W_ar, 20)
        expected_H2O = H_ar * 9.0 + W_ar
        self.assertAlmostEqual(result.flue_gas_wet.H2O, expected_H2O, places=2)

    def test_so2_from_sulfur(self):
        """Verifica cálculo de SO2 a partir del azufre."""
        # SO2 = S * (64.06/32.06) = S * 2.0
        S_ar = 0.01
        result = calculate_flue_gas_masses(0, 0, S_ar, 0, 0, 0, 0, 20)
        expected_SO2 = S_ar * 2.0
        self.assertAlmostEqual(result.flue_gas_dry.SO2, expected_SO2, places=3)

    def test_wet_gas_contains_water(self):
        """Verifica que el gas húmedo contiene más masa que el seco."""
        result = calculate_flue_gas_masses(0.5, 0.05, 0.001, 0.4, 0.01, 0.03, 0.009, 20)
        self.assertGreater(result.flue_gas_wet.total, result.flue_gas_dry.total)


class TestFlueGasFlow(unittest.TestCase):
    """Tests para flujo de gases de combustión."""

    def test_flue_gas_flow_scales_with_fuel(self):
        """Verifica que el flujo de gases escala con el combustible."""
        comp = {
            'C': 0.1974, 'H': 0.0252, 'O': 0.1953,
            'N': 0.0017, 'S': 0.0004, 'A': 0.10, 'W': 0.48
        }
        result1 = calculate_flue_gas_flow(10000, comp, 20)
        result2 = calculate_flue_gas_flow(20000, comp, 20)
        self.assertAlmostEqual(
            result2['flows']['total_wet'],
            2 * result1['flows']['total_wet'],
            places=0
        )

    def test_flue_gas_flow_contains_all_components(self):
        """Verifica que el resultado contenga todos los componentes."""
        comp = {
            'C': 0.1974, 'H': 0.0252, 'O': 0.1953,
            'N': 0.0017, 'S': 0.0004, 'A': 0.10, 'W': 0.48
        }
        result = calculate_flue_gas_flow(10000, comp, 20)

        self.assertIn('CO2', result['flows'])
        self.assertIn('H2O', result['flows'])
        self.assertIn('SO2', result['flows'])
        self.assertIn('N2', result['flows'])
        self.assertIn('O2', result['flows'])
        self.assertIn('Ash', result['flows'])
        self.assertIn('total_wet', result['flows'])
        self.assertIn('total_dry', result['flows'])


class TestFlueGasTemperature(unittest.TestCase):
    """Tests para estimación de temperatura de gases de chimenea."""

    def test_temperature_decreases_with_excess_air(self):
        """Verifica que más exceso de aire baje T_gases (más masa, misma energía)."""
        T_low_excess = estimate_flue_gas_temperature(10, 48)
        T_high_excess = estimate_flue_gas_temperature(50, 48)
        self.assertGreater(T_low_excess, T_high_excess)

    def test_temperature_increases_with_humidity(self):
        """Verifica que más humedad del bagazo eleve T_gases."""
        T_dry = estimate_flue_gas_temperature(20, 40)
        T_wet = estimate_flue_gas_temperature(20, 55)
        self.assertGreater(T_wet, T_dry)

    def test_temperature_base_case(self):
        """Caso base: 20% exceso, 48% humedad → 125°C."""
        T_gases = estimate_flue_gas_temperature(20, 48)
        # 127.8 - 4.0 + 1.2 = 125.0
        self.assertAlmostEqual(T_gases, 125.0, places=0)

    def test_temperature_in_realistic_range(self):
        """T_gases debe estar en 110-145°C para condiciones típicas."""
        T_gases = estimate_flue_gas_temperature(20, 48)
        self.assertGreater(T_gases, 110)
        self.assertLess(T_gases, 145)


class TestBagazoComposition(unittest.TestCase):
    """Tests para composición específica del bagazo."""

    def test_bagazo_base_case(self):
        """
        Valida cálculos con composición base del bagazo.

        Datos base (documentación):
        - Bagazo: C=19.74%, H=2.52%, O=19.53%, N=0.17%, S=0.04%, A=10%, W=48%
        - Exceso de aire: 20%
        """
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

        # Verificar que el aire teórico sea razonable
        # Para bagazo con estas propiedades: ~2.3 kg aire/kg bagazo
        self.assertGreater(products.air.m_theoretical, 2.0)
        self.assertLess(products.air.m_theoretical, 3.0)

        # Verificar que el aire real sea mayor al teórico (20% exceso)
        self.assertGreater(products.air.m_actual, products.air.m_theoretical)


class TestValidationBaseCase(unittest.TestCase):
    """Tests de validación contra datos base."""

    def test_validate_with_base_case(self):
        """Valida usando la función de validación del módulo."""
        result = validate_with_base_case()

        # Verificar que retorne todos los campos esperados
        self.assertIn('air_theoretical', result)
        self.assertIn('air_actual', result)
        self.assertIn('excess_air', result)
        self.assertIn('O2_required', result)
        self.assertIn('flue_gas_CO2', result)
        self.assertIn('flue_gas_H2O', result)

        # Verificar valores razonables
        self.assertGreater(result['air_theoretical'], 0)
        self.assertGreater(result['air_actual'], result['air_theoretical'])
        self.assertEqual(result['excess_air'], 20.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
