import requests
from test_base import ConnectivityBase


class IdentityTests(ConnectivityBase):
    __test__ = True

    def test_some_check(self):
        response = requests.get(f"{self.localhost}/identity/.well-known/openid-configuration", verify=False)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())