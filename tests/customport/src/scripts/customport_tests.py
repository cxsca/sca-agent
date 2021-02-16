import requests
import unittest
import sys


class CustomPortTests(unittest.TestCase):
    def __init__(self, f):
        super(CustomPortTests, self).__init__(f)

        self.route_to_test = "http://localhost:5001/api/health"

    def test_status_code(self):
        response = requests.get(self.route_to_test)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "available")


# Make container properly exit, when tests fail
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(CustomPortTests))
    result.printErrors()
    sys.exit(not result.wasSuccessful())
