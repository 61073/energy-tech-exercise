import os
import requests
import json

from unittest import TestCase
from unittest.mock import patch, Mock
from nose2.tools import params
from src.app.heating_analyser_lambda import lambda_handler


example_weather_api_response = {
    "location": {
        "location": "W Pennines (Ringway)",
        "degreeDays": "2500",
        "groundTemp": "9",
        "postcode": "NE66",
        "lat": "55.424",
        "lng": "-1.583"
    }
}

expected_success_string_output = """--------------------------------------
4cb3820a-7bf6-47f9-8afc-3adcac8752cd
--------------------------------------
Estimated Heat Loss = 16412
Design Region = W Pennines (Ringway)
Power Heat Loss = 7
Recommended Heat Pump = 8kW Package
Cost Breakdown:
 Design & Supply of your Air Source Heat Pump System Components (8kW), 4216.00
 Installation of your Air Source Heat Pump and Hot Water Cylinder, 2900.00
 Supply & Installation of your Homely Smart Thermostat, 150.00
 Supply & Installation of a new Consumer Unit, 300.00
 MCS System Commissioning & HIES Insurance-backed Warranty, 1648.00
Total Cost, including VAT = 9674.70
--------------------------------------
e21a3149-b88c-40e9-86fd-c94a6b93cb78
--------------------------------------
Estimated Heat Loss = 8906
Design Region = W Pennines (Ringway)
Power Heat Loss = 4
Recommended Heat Pump = 5kW Package
Cost Breakdown:
 Design & Supply of your Air Source Heat Pump System Components (5kW), 3947.00
 Installation of your Air Source Heat Pump and Hot Water Cylinder, 2900.00
 Supply & Installation of your Homely Smart Thermostat, 150.00
 Supply & Installation of a new Consumer Unit, 300.00
 MCS System Commissioning & HIES Insurance-backed Warranty, 1648.00
Total Cost, including VAT = 9392.25\n"""


class TestHouseHeatingAnalyser(TestCase):

    @params(None, {}, 123, "123")
    def test_exception_event_input_error(self, event_input):
        with self.assertRaises(Exception) as e:
            lambda_handler(event_input, None)

    @patch.object(requests, "get")
    def test_success_response(self, mock_request):
        mock_response = Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = example_weather_api_response
        # Use OS path join method in order to work on both Windows and Linux as was developed on Windows machine
        test_file_location = os.path.join("src", "test", "test_example_files", "test_houses.json")
        with open(test_file_location) as houses_file:
            success_event_input = json.load(houses_file)
            houses_file.close()
        actual_response = lambda_handler(success_event_input, None)
        self.assertEqual(200, actual_response.get("statusCode"))
        actual_body = json.loads(actual_response["body"])
        actual_output_body = actual_body.get("body")
        self.assertEqual(expected_success_string_output, actual_output_body)
        self.assertEqual("Successfully processed 2 house heat details", actual_body.get("message"))
