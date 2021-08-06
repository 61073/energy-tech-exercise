from unittest import TestCase
from nose2.tools import params
from src.app.utils import generate_response


class TestUtils(TestCase):

    @params((200, 200, "test", ["1", "2"], {"statusCode": 200, "headers": {"Content-Type": "application/json"},
                                            "body": '{"status": 200, "message": "test", "body": ["1", "2"]}'}),
            (400, 404, "error", None, {"statusCode": 400, "headers": {"Content-Type": "application/json"},
                                            "body": '{"status": 404, "message": "error", "body": null}'})
            )
    def test_generate_response(self, status_code, status, message, body, expected_response):
        actual_response = generate_response(status_code, status, message, body)
        self.assertEqual(expected_response, actual_response)
