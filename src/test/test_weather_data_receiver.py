import requests

from unittest import TestCase
from unittest.mock import patch, Mock

from nose2.tools import params

from src.app.weather_data_receiver import get_weather_degree_days

example_weather_api_response = {
    "location": {
        "location": "Thames Valley (Heathrow)",
        "degreeDays": "2483",
        "groundTemp": "9",
        "postcode": "NE66",
        "lat": "55.424",
        "lng": "-1.583"
    }
}

error_weather_api_response = {
    "error": "404 not found"
}

error_weather_api_response_2 = {
    "location": "404 not found"
}

error_weather_api_response_3 = {
    "location": {"error": "test"}
}

error_weather_api_response_4 = {
    "location": {"degreeDays": "error"}
}


class TestWeatherDataReceiver(TestCase):

    @patch.object(requests, "get")
    def test_success_response(self, mock_request):
        mock_response = Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = example_weather_api_response
        actual_degree_days = get_weather_degree_days("Thames Valley (Heathrow)")
        self.assertEqual(2483, actual_degree_days)

    @params(error_weather_api_response, error_weather_api_response_2, error_weather_api_response_3,
            error_weather_api_response_4)
    @patch.object(requests, "get")
    def test_exceptions(self, api_response, mock_request):
        # TODO - create separate exceptions for each scenario and unit test each separately
        mock_response = Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = api_response
        with self.assertRaises(Exception) as e:
            get_weather_degree_days("Thames Valley (Heathrow)")
