import requests
from test_base import ConnectivityBase


class HealthCheckTests(ConnectivityBase):
    __test__ = True

    def test_status_code(self):
        response = requests.get(f"{self.localhost}/api/health", verify=False)

        self.assertEqual(response.status_code, 200)
        response_object = response.json()
        self.assertEqual(response_object["status"], "available")
        self.assertIsNotNone(response_object["version"])
        self.assertEqual(len(response_object["notes"]), 3)

    def test_minio_healthy(self):

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        response = requests.get(f"{self.localhost}/minio/login", headers=headers, verify=False)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
