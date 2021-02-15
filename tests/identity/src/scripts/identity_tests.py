import requests
import unittest
import sys


class IdentityTests(unittest.TestCase):
    def __init__(self, f):
        super(IdentityTests, self).__init__(f)

        self.route_to_test = "http://localhost/identity/.well-known/openid-configuration"

    def test_identity(self):

        response = requests.get(self.route_to_test)

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())


# Make container properly exit, when tests fail
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    result = runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(IdentityTests))
    result.printErrors()
    sys.exit(not result.wasSuccessful())
