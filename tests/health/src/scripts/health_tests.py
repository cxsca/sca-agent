import requests
import unittest


class HealthCheckTests(unittest.TestCase):
    def __init__(self, f):
        super(HealthCheckTests, self).__init__(f)

    def test_health(self):
        route_to_test = "http://localhost/health"

        response = requests.get(route_to_test)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "available")
