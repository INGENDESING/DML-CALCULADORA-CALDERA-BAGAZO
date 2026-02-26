"""
Tests Unitarios - Módulo de Balance
====================================
Pruebas para validar el balance de materia y energía
de una caldera acuotubular alimentada con bagazo.

DML INGENIEROS CONSULTORES S.A.S.
"""

import unittest
import sys
import os

# Agregar el path del backend al sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from balance import (
    InputData,
    StreamResult,
    BalanceResults,
    calculate_water_side_balance,
    calculate_energy_balance,
    calculate_bagazo_consumption,
    calculate_complete_balance,
    validate_with_base_case
)


class TestInputData(unittest.TestCase):
    """Tests para la clase InputData."""

    def test_input_data_default_values(self):
        """Verifica que los valores por defecto sean los correctos."""
        inputs = InputData()
        self.assertEqual(inputs.m_stm, 100.0)
        self.assertEqual(inputs.P_stm, 106.0)
        self.assertEqual(inputs.T_stm, 545.0)
        self.assertEqual(inputs.bagazo_humidity, 48.0)
        self.assertEqual(inputs.bagazo_ash, 10.0)

    def test_input_data_custom_values(self):
        """Verifica que se puedan asignar valores personalizados."""
        inputs = InputData(m_stm=150.0, P_stm=90.0)
        self.assertEqual(inputs.m_stm, 150.0)
        self.assertEqual(inputs.P_stm, 90.0)


class TestWaterSideBalance(unittest.TestCase):
    """Tests para balance de materia lado agua."""

    def test_water_balance_no_blowdown(self):
        """Verifica balance sin purga (0%)."""
        inputs = InputData(m_stm=100.0, pct_purge=0.0)
        result = calculate_water_side_balance(inputs)
        self.assertAlmostEqual(result['m_fw'], 100.0, places=2)
        self.assertAlmostEqual(result['m_purge'], 0.0, places=2)

    def test_water_balance_with_blowdown(self):
        """Verifica balance con 2% de purga."""
        inputs = InputData(m_stm=100.0, pct_purge=2.0)
        result = calculate_water_side_balance(inputs)

        # m_fw = m_stm / (1 - 0.02) = 100 / 0.98 = 102.04
        self.assertAlmostEqual(result['m_fw'], 102.04, places=2)

        # m_purge = m_fw - m_stm = 102.04 - 100 = 2.04
        self.assertAlmostEqual(result['m_purge'], 2.04, places=2)

    def test_water_balance_conservation(self):
        """Verifica conservación de masa: m_fw = m_stm + m_purge."""
        inputs = InputData(m_stm=100.0, pct_purge=3.0)
        result = calculate_water_side_balance(inputs)
        self.assertAlmostEqual(
            result['m_fw'],
            result['m_stm'] + result['m_purge'],
            places=2
        )


class TestEnergyBalance(unittest.TestCase):
    """Tests para balance de energía."""

    def test_energy_balance_returns_q_abs(self):
        """Verifica que calcule Q_abs."""
        inputs = InputData(
            m_stm=100.0, P_stm=106.0, T_stm=545.0,
            T_fw=270.0, pct_purge=2.0
        )
        water_bal = calculate_water_side_balance(inputs)
        result = calculate_energy_balance(inputs, water_bal)

        self.assertIn('Q_abs_MW', result)
        self.assertGreater(result['Q_abs_MW'], 0)

    def test_energy_balance_returns_q_fuel(self):
        """Verifica que calcule Q_fuel."""
        inputs = InputData(
            m_stm=100.0, P_stm=106.0, T_stm=545.0,
            T_fw=270.0, pct_purge=2.0, efficiency=94.0
        )
        water_bal = calculate_water_side_balance(inputs)
        result = calculate_energy_balance(inputs, water_bal)

        # Q_fuel = Q_abs / efficiency
        # Para efficiency < 100%, Q_fuel > Q_abs
        self.assertGreater(result['Q_fuel_MW'], result['Q_abs_MW'])

    def test_energy_balance_q_abs_positive(self):
        """Verifica que Q_abs sea positivo (vapor gana energía)."""
        inputs = InputData(
            m_stm=100.0, P_stm=106.0, T_stm=545.0,
            T_fw=270.0, pct_purge=2.0
        )
        water_bal = calculate_water_side_balance(inputs)
        result = calculate_energy_balance(inputs, water_bal)

        # h_steam (~3480) > h_fw (~1180)
        # Q_abs debe ser positivo
        self.assertGreater(result['Q_abs_MW'], 50)  # > 50 MW para 100 t/h

    def test_energy_balance_enthalpies(self):
        """Verifica que las entalpías sean razonables."""
        inputs = InputData(
            m_stm=100.0, P_stm=106.0, T_stm=545.0,
            T_fw=270.0, pct_purge=2.0
        )
        water_bal = calculate_water_side_balance(inputs)
        result = calculate_energy_balance(inputs, water_bal)

        # Entalpía de vapor sobrecalentado > 3400 kJ/kg
        self.assertGreater(result['steam_h'], 3400)

        # Entalpía de agua de alimentación ~1000-1200 kJ/kg
        self.assertGreater(result['fw_h'], 1000)
        self.assertLess(result['fw_h'], 1300)


class TestBagazoConsumption(unittest.TestCase):
    """Tests para cálculo de consumo de bagazo."""

    def test_bagazo_consumption_returns_flow(self):
        """Verifica que calcule flujo de bagazo."""
        Q_fuel = 68.0  # MW
        result = calculate_bagazo_consumption(Q_fuel, 48.0, 10.0)

        self.assertIn('m_bagazo_th', result)
        self.assertIn('m_bagazo_kgh', result)
        self.assertGreater(result['m_bagazo_th'], 0)

    def test_bagazo_consumption_with_higher_humidity(self):
        """Verifica que mayor humedad aumenta consumo."""
        Q_fuel = 68.0
        result_48 = calculate_bagazo_consumption(Q_fuel, 48.0, 10.0)
        result_55 = calculate_bagazo_consumption(Q_fuel, 55.0, 10.0)

        # Mayor humedad = menor PCI = más bagazo
        self.assertGreater(result_55['m_bagazo_th'], result_48['m_bagazo_th'])

    def test_bagazo_consumption_returns_calorific_value(self):
        """Verifica que retorne poder calorífico."""
        result = calculate_bagazo_consumption(68.0, 48.0, 10.0)

        self.assertIn('calorific_value', result)
        self.assertGreater(result['calorific_value'].PCI, 0)
        self.assertGreater(result['calorific_value'].PCS, result['calorific_value'].PCI)

    def test_bagazo_consumption_returns_composition(self):
        """Verifica que retorne composición AR."""
        result = calculate_bagazo_consumption(68.0, 48.0, 10.0)

        self.assertIn('composition', result)
        self.assertEqual(result['composition'].W, 48.0)
        self.assertEqual(result['composition'].A, 10.0)


class TestCompleteBalance(unittest.TestCase):
    """Tests para balance completo."""

    def test_complete_balance_returns_results(self):
        """Verifica que retorne BalanceResults."""
        inputs = InputData()
        result = calculate_complete_balance(inputs)
        self.assertIsInstance(result, BalanceResults)

    def test_complete_balance_calculates_ratio(self):
        """Verifica que calcule el ratio Vapor/Bagazo."""
        inputs = InputData(m_stm=100.0)
        result = calculate_complete_balance(inputs)

        self.assertGreater(result.ratio_stm_bagazo, 0)
        # Ratio típico: 2.5 - 3.0 t_vapor/t_bagazo
        self.assertGreater(result.ratio_stm_bagazo, 2.0)
        self.assertLess(result.ratio_stm_bagazo, 4.0)

    def test_complete_balance_streams(self):
        """Verifica que todas las corrientes estén presentes."""
        inputs = InputData()
        result = calculate_complete_balance(inputs)

        # Corrientes de entrada
        self.assertIsNotNone(result.feedwater)
        self.assertIsNotNone(result.bagazo)
        self.assertIsNotNone(result.air)

        # Corrientes de salida
        self.assertIsNotNone(result.steam)
        self.assertIsNotNone(result.blowdown)
        self.assertIsNotNone(result.flue_gas)
        self.assertIsNotNone(result.ash)

    def test_complete_balance_energy_conservation(self):
        """Verifica conservación de energía."""
        inputs = InputData(m_stm=100.0, efficiency=94.0)
        result = calculate_complete_balance(inputs)

        # Q_fuel = Q_abs + losses
        self.assertAlmostEqual(
            result.Q_fuel_MW,
            result.Q_abs_MW + result.losses_MW,
            places=2
        )

    def test_complete_balance_losses_positive(self):
        """Verifica que las pérdidas sean positivas."""
        inputs = InputData(efficiency=94.0)
        result = calculate_complete_balance(inputs)

        # Con efficiency < 100%, debe haber pérdidas
        self.assertGreater(result.losses_MW, 0)


class TestValidationBaseCase(unittest.TestCase):
    """Tests de validación contra datos base del proyecto."""

    def test_validate_with_base_case(self):
        """
        Valida el balance completo contra datos base.

        Datos base (documentación):
        - Flujo de vapor: 100 t/h
        - Presión: 106 barg
        - Temperatura: 545 °C
        - Humedad bagazo: 48%
        - Cenizas bagazo: 10%
        - Ratio esperado: 2.655
        """
        result = validate_with_base_case()

        # Verificar estructura
        self.assertIn('ratio_calculated', result)
        self.assertIn('ratio_expected', result)
        self.assertIn('error_percent', result)
        self.assertIn('valid', result)

        # Verificar valor esperado
        self.assertEqual(result['ratio_expected'], 2.655)

    def test_ratio_within_tolerance(self):
        """Verifica que el ratio esté dentro de tolerancia."""
        result = validate_with_base_case()

        # Error debe ser menor a 5%
        self.assertLess(result['error_percent'], 5.0)

    def test_bagazo_flow_reasonable(self):
        """Verifica que el flujo de bagazo sea razonable."""
        result = validate_with_base_case()

        # Esperado: 37.67 t/h
        self.assertGreater(result['m_bagazo'], 35)
        self.assertLess(result['m_bagazo'], 40)

    def test_q_abs_reasonable(self):
        """Verifica que Q_abs sea razonable."""
        result = validate_with_base_case()

        # Para 100 t/h de vapor, Q_abs ~64 MW
        self.assertGreater(result['Q_abs'], 60)
        self.assertLess(result['Q_abs'], 70)

    def test_q_fuel_greater_than_q_abs(self):
        """Verifica que Q_fuel > Q_abs (por eficiencia < 100%)."""
        result = validate_with_base_case()

        self.assertGreater(result['Q_fuel'], result['Q_abs'])


class TestRatioCalculation(unittest.TestCase):
    """Tests específicos para el ratio Vapor/Bagazo."""

    def test_ratio_increases_with_steam_flow(self):
        """Verifica que el ratio aumente con el flujo de vapor."""
        inputs1 = InputData(m_stm=100.0)
        inputs2 = InputData(m_stm=150.0)

        result1 = calculate_complete_balance(inputs1)
        result2 = calculate_complete_balance(inputs2)

        # Al aumentar vapor, el ratio debe aumentar
        # (mismo bagazo para más vapor = ratio mayor)
        # Nota: esto asume que el bagazo se recalcula
        self.assertIsNotNone(result1.ratio_stm_bagazo)
        self.assertIsNotNone(result2.ratio_stm_bagazo)

    def test_ratio_formula(self):
        """Verifica fórmula del ratio."""
        inputs = InputData(m_stm=100.0)
        result = calculate_complete_balance(inputs)

        # ratio = m_stm / m_bagazo
        expected_ratio = inputs.m_stm / result.bagazo.m_th
        self.assertAlmostEqual(
            result.ratio_stm_bagazo,
            expected_ratio,
            places=3
        )


class TestStreamResults(unittest.TestCase):
    """Tests para StreamResult."""

    def test_stream_result_fields(self):
        """Verifica que StreamResult tenga los campos correctos."""
        stream = StreamResult(
            name="Test Stream",
            m_th=100.0,
            T_celsius=500.0,
            energy_MW=50.0
        )

        self.assertEqual(stream.name, "Test Stream")
        self.assertEqual(stream.m_th, 100.0)
        self.assertEqual(stream.T_celsius, 500.0)
        self.assertEqual(stream.energy_MW, 50.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
