import requests
import unittest


class IdentityTests(unittest.TestCase):
    def __init__(self, f):
        super(IdentityTests, self).__init__(f)

    def test_health(self):
        route_to_test = "http://localhost/identity/.well-known/openid-configuration"

        response = requests.get(route_to_test)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

