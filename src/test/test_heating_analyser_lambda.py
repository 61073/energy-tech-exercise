import os
import requests
import json

from unittest import TestCase
from unittest.mock import patch
from nose2.tools import params
from src.app.heating_analyser_lambda import lambda_handler


class TestHouseHeatingAnalyser(TestCase):

    @params(None, {}, 123, "123")
    def test_exception_event_input_error(self, event_input):
        with self.assertRaises(Exception) as e:
            lambda_handler(event_input, None)

    @patch.object(requests, "get")
    def test_success_response(self, mock_request):
        # Use OS path join method in order to work on both Windows and Linux as was developed on Windows machine
        test_file_location = os.path.join("src", "test", "test_example_files", "test_houses.json")
        with open(test_file_location) as houses_file:
            success_event_input = json.load(houses_file)
            houses_file.close()
        actual_response = lambda_handler(success_event_input, None)
        self.assertEqual(200, actual_response.get("statusCode"))
        actual_body = json.loads(actual_response["body"])
        actual_event_body = actual_body.get("body")
        self.assertEqual(success_event_input, actual_event_body)
        self.assertEqual("Successfully processed 2 house heat details", actual_body.get("message"))
