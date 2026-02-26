"""
Tests Unitarios - Módulo de Termodinámica
==========================================
Pruebas para validar los cálculos de propiedades termodinámicas
del agua y vapor utilizando IAPWS-97.

DML INGENIEROS CONSULTORES S.A.S.
"""

import unittest
import sys
import os

# Agregar el path del backend al sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from thermodynamics import (
    get_steam_properties,
    get_feedwater_properties,
    get_saturated_liquid_properties,
    get_saturation_temperature,
    calculate_stream_energy,
    calculate_stream_energy_from_tons,
    SteamProperties,
    WaterProperties
)


class TestSteamProperties(unittest.TestCase):
    """Tests para propiedades de vapor sobrecalentado."""

    def test_get_steam_properties_returns_tuple(self):
        """Verifica que retorna un SteamProperties con todos los campos."""
        result = get_steam_properties(106, 545)
        self.assertIsInstance(result, SteamProperties)
        self.assertTrue(hasattr(result, 'h'))
        self.assertTrue(hasattr(result, 's'))
        self.assertTrue(hasattr(result, 'rho'))
        self.assertTrue(hasattr(result, 'T'))
        self.assertTrue(hasattr(result, 'P'))

    def test_steam_enthalpy_base_case(self):
        """Valida entalpía de vapor contra datos base (106 barg, 545°C)."""
        result = get_steam_properties(106, 545)
        # Esperado: 3482.23 kJ/kg
        expected_h = 3482.23
        tolerance = 1.0  # kJ/kg
        self.assertAlmostEqual(result.h, expected_h, delta=tolerance,
                              msg=f"Entalpía vapor: {result.h} kJ/kg, "
                                  f"esperado: {expected_h} kJ/kg")

    def test_steam_density_reasonable(self):
        """Verifica que la densidad del vapor esté en rango razonable."""
        result = get_steam_properties(106, 545)
        # Densidad de vapor a alta presión: ~30-35 kg/m³
        self.assertGreater(result.rho, 20)
        self.assertLess(result.rho, 50)

    def test_steam_entropy_positive(self):
        """Verifica que la entropía sea positiva."""
        result = get_steam_properties(106, 545)
        self.assertGreater(result.s, 0)

    def test_steam_temperature_preserved(self):
        """Verifica que la temperatura de entrada se preserve."""
        T_input = 545.0
        result = get_steam_properties(106, T_input)
        self.assertEqual(result.T, T_input)

    def test_steam_pressure_preserved(self):
        """Verifica que la presión de entrada se preserve."""
        P_input = 106.0
        result = get_steam_properties(P_input, 545)
        self.assertEqual(result.P, P_input)


class TestFeedwaterProperties(unittest.TestCase):
    """Tests para propiedades de agua de alimentación."""

    def test_get_feedwater_properties_returns_tuple(self):
        """Verifica que retorna un WaterProperties."""
        result = get_feedwater_properties(270, 106)
        self.assertIsInstance(result, WaterProperties)

    def test_feedwater_enthalpy_base_case(self):
        """Valida entalpía de agua de alimentación contra datos base."""
        result = get_feedwater_properties(270, 106)
        # Esperado: ~1183.44 kJ/kg
        expected_h = 1183.44
        tolerance = 2.0  # kJ/kg
        self.assertAlmostEqual(result.h, expected_h, delta=tolerance,
                              msg=f"Entalpía agua alim: {result.h} kJ/kg")

    def test_feedwater_enthalpy_increases_with_temperature(self):
        """Verifica que la entalpía aumente con la temperatura."""
        h1 = get_feedwater_properties(200, 100).h
        h2 = get_feedwater_properties(250, 100).h
        self.assertGreater(h2, h1)


class TestSaturatedLiquid(unittest.TestCase):
    """Tests para propiedades de líquido saturado."""

    def test_saturated_liquid_enthalpy_base_case(self):
        """Valida entalpía de líquido saturado a 106 barg."""
        result = get_saturated_liquid_properties(106)
        # Valor IAPWS97 real: ~1437.77 kJ/kg (líquido saturado a ~107 bar abs)
        expected_h = 1437.77
        tolerance = 2.0  # kJ/kg
        self.assertAlmostEqual(result.h, expected_h, delta=tolerance,
                              msg=f"Entalpía líquido saturado: {result.h} kJ/kg")

    def test_saturated_liquid_temperature(self):
        """Verifica que la temperatura de saturación sea razonable."""
        result = get_saturated_liquid_properties(106)
        # Temperatura de saturación a ~107 bar abs: ~311-314°C
        self.assertGreater(result.T, 310)
        self.assertLess(result.T, 320)


class TestSaturationTemperature(unittest.TestCase):
    """Tests para temperatura de saturación."""

    def test_saturation_temperature_increases_with_pressure(self):
        """Verifica que T_sat aumente con la presión."""
        T1 = get_saturation_temperature(50)
        T2 = get_saturation_temperature(100)
        self.assertGreater(T2, T1)

    def test_saturation_temperature_reasonable(self):
        """Verifica valor razonable de T_sat a 100 barg."""
        T_sat = get_saturation_temperature(100)
        # ~311°C a 101 bar abs
        self.assertGreater(T_sat, 300)
        self.assertLess(T_sat, 320)


class TestEnergyCalculations(unittest.TestCase):
    """Tests para cálculos de energía."""

    def test_calculate_stream_energy_returns_mw(self):
        """Verifica que el cálculo de energía retorne MW."""
        # 100,000 kg/h * 1000 kJ/kg = 100,000,000 kJ/h
        # = 27.78 MW
        result = calculate_stream_energy(100000, 1000)
        self.assertAlmostEqual(result, 27.78, places=2)

    def test_calculate_stream_energy_from_tons(self):
        """Verifica cálculo de energía con flujo en t/h."""
        # 100 t/h = 100,000 kg/h
        result = calculate_stream_energy_from_tons(100, 1000)
        expected = calculate_stream_energy(100000, 1000)
        self.assertAlmostEqual(result, expected, places=2)

    def test_energy_proportional_to_flow(self):
        """Verifica que la energía sea proporcional al flujo."""
        E1 = calculate_stream_energy(50000, 1000)
        E2 = calculate_stream_energy(100000, 1000)
        self.assertAlmostEqual(E2, 2 * E1, places=2)

    def test_energy_proportional_to_enthalpy(self):
        """Verifica que la energía sea proporcional a la entalpía."""
        E1 = calculate_stream_energy(100000, 500)
        E2 = calculate_stream_energy(100000, 1000)
        self.assertAlmostEqual(E2, 2 * E1, places=2)


class TestValidationBaseCase(unittest.TestCase):
    """Tests de validación contra datos base del proyecto."""

    def test_complete_base_case_validation(self):
        """
        Valida todos los cálculos contra los datos base.

        Datos base (documentación):
        - Vapor: 100 t/h, 106 barg, 545 °C
        - Resultado esperado: h = 3482.23 kJ/kg
        """
        # Vapor sobrecalentado
        steam = get_steam_properties(106, 545)
        self.assertAlmostEqual(steam.h, 3482.23, delta=1.0)

        # Agua de alimentación (270 °C)
        fw = get_feedwater_properties(270, 106)
        self.assertAlmostEqual(fw.h, 1183.44, delta=2.0)

        # Purga (líquido saturado a 106 barg)
        blowdown = get_saturated_liquid_properties(106)
        self.assertAlmostEqual(blowdown.h, 1437.77, delta=2.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
