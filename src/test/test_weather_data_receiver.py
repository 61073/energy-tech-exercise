from unittest import TestCase
from unittest.mock import patch, Mock

import requests

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


class TestWeatherDataReceiver(TestCase):

    @patch.object(requests, "get")
    def test_success_response(self, mock_request):
        mock_response = Mock()
        mock_request.return_value = mock_response
        mock_response.json.return_value = example_weather_api_response
        actual_degree_days = get_weather_degree_days("Thames Valley (Heathrow)")
        self.assertEqual("2483", actual_degree_days)
