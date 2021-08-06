from unittest import TestCase
from unittest.mock import patch, Mock

import requests
from nose2.tools import params
from src.app.data_calculator import DataCalculator, calculate_heat_loss, calculate_power_heat_loss, get_heat_pump_data

example_house_data = {
    "submissionId": "abc123",
    "designRegion": "Severn Valley (Filton)",
    "floorArea": 150,
    "age": "1967 - 1975",
    "heatingFactor": 100,
    "insulationFactor": 1.1
}

example_heat_pump_5kw = {
    "label": "5kW Package",
    "outputCapacity": 5,
    "costs": [
        {"label": "Design & Supply of your Air Source Heat Pump System Components (5kW)", "cost": 3947},
        {"label": "Installation of your Air Source Heat Pump and Hot Water Cylinder", "cost":  2900},
        {"label": "Supply & Installation of your Homely Smart Thermostat", "cost": 150},
        {"label": "Supply & Installation of a new Consumer Unit", "cost": 300},
        {"label": "MCS System Commissioning & HIES Insurance-backed Warranty", "cost": 1648}
    ]
}

example_heat_pump_12kw = {
    "label": "12kW Package",
    "outputCapacity": 12,
    "costs": [
        {"label": "Design & Supply of your Air Source Heat Pump System Components (12kW)", "cost": 5138},
        {"label": "Installation of your Air Source Heat Pump and Hot Water Cylinder", "cost": 2900},
        {"label": "Supply & Installation of your Homely Smart Thermostat", "cost": 150},
        {"label": "Supply & Installation of a new Consumer Unit", "cost": 300},
        {"label": "MCS System Commissioning & HIES Insurance-backed Warranty", "cost": 1648}
    ]
}

success_example = """--------------------------------------
abc123
--------------------------------------
Estimated Heat Loss = 16500
Design Region = Severn Valley (Filton)
Power Heat Loss = 10
Recommended Heat Pump = 12kW Package
Cost Breakdown:
 Design & Supply of your Air Source Heat Pump System Components (12kW), 5138.00
 Installation of your Air Source Heat Pump and Hot Water Cylinder, 2900.00
 Supply & Installation of your Homely Smart Thermostat, 150.00
 Supply & Installation of a new Consumer Unit, 300.00
 MCS System Commissioning & HIES Insurance-backed Warranty, 1648.00
Total Cost, including VAT = 10642.80"""

error_example = """--------------------------------------
abc123
--------------------------------------
Heating Loss: 16500
Warning: Could not find design region"""

example_weather_api_response = {
    "location": {
        "location": "Severn Valley (Filton)",
        "degreeDays": "1650",
        "groundTemp": "9",
        "postcode": "NE66",
        "lat": "55.424",
        "lng": "-1.583"
    }
}


def raise_exception():
    raise Exception


class TestDataCalculator(TestCase):

    def test_success_init(self):
        calculator_obj = DataCalculator(example_house_data)
        self.assertEqual(100, calculator_obj.heating_factor)
        self.assertEqual(1.1, calculator_obj.insulation_factor)
        self.assertEqual(150, calculator_obj.floor_area)
        self.assertEqual("abc123", calculator_obj.id)
        self.assertEqual("Severn Valley (Filton)", calculator_obj.location)

    @patch.object(requests, "get")
    def test_process_results(self, mock_request):
        mock_response = Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = example_weather_api_response
        calculator_obj = DataCalculator(example_house_data)
        actual_results = calculator_obj.process_results()
        self.assertEqual(success_example, actual_results)

    @patch.object(requests, "get", side_effect=raise_exception)
    def test_process_results_error(self, mock_request):
        mock_response = Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = example_weather_api_response
        calculator_obj = DataCalculator(example_house_data)
        actual_results = calculator_obj.process_results()
        self.assertEqual(error_example, actual_results)

    @params((100, 50, 1.5, 7500.0), (80, 75, 1.0, 6000.0))
    def test_calculate_heat_loss(self, floor_area, heating_factor, insulation_factor, expected_heat_loss):
        actual_heat_loss = calculate_heat_loss(floor_area, heating_factor, insulation_factor)
        self.assertEqual(expected_heat_loss, actual_heat_loss)

    @params((20000, 2000, 10.0), (7000, 2500, 2.8))
    def test_calculate_power_heat_loss(self, heat_loss, degree_days, expected_power_heat_loss):
        actual_power_heat_loss = calculate_power_heat_loss(heat_loss, degree_days)
        self.assertEqual(expected_power_heat_loss, actual_power_heat_loss)

    @params((10.0, example_heat_pump_12kw), (2.8, example_heat_pump_5kw))
    def test_get_heat_pump_data(self, power_heat_loss, expected_output):
        actual_output = get_heat_pump_data(power_heat_loss)
        self.assertEqual(expected_output, actual_output)