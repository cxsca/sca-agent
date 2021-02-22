import unittest
import sys

import health_tests
import identity_tests
import presignedurl_tests

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(health_tests))
suite.addTest(loader.loadTestsFromModule(identity_tests))
suite.addTest(loader.loadTestsFromModule(presignedurl_tests))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
result.printErrors()

# Make container properly exit, when tests fail
sys.exit(not result.wasSuccessful())
