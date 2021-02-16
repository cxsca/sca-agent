import requests
import unittest
import sys


class CustomPortTests(unittest.TestCase):
    def __init__(self, f):
        super(CustomPortTests, self).__init__(f)

        self.localhost = "http://localhost:5001"

    def test_scan_runner_healthy(self):
        response = requests.get(f"{self.localhost}/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "available")

    def test_minio_with_custom_port_healthy(self):

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, '
                                 'like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        response = requests.get(f"{self.localhost}/minio/login", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)


# Make container properly exit, when tests fail
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(CustomPortTests))
    result.printErrors()
    sys.exit(not result.wasSuccessful())
