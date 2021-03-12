import unittest
import sys
import os
import importlib

suite = unittest.TestSuite()
loader = unittest.TestLoader()

env_run_test_modules = os.environ.get("RUN_TEST_MODULES")

if not env_run_test_modules:
    print("No tests were specified in docker-compose.yml for current scenario. \n"
          "Please add comma separated list of tests to be run with Environment Variable `RUN_TEST_MODULES` \n"
          "Example (Modules) : RUN_TEST_MODULES: health_tests")
    sys.exit(1)

test_modules_to_run = [x.strip() for x in env_run_test_modules.split(',')]


for env_test_module in test_modules_to_run:
    test_module = importlib.import_module(env_test_module)

    if not test_module:
        print(f"Module `{env_test_module}` was not found. Please make sure you specified the name correctly "
              f"and the tests class exists")
        sys.exit(1)

    suite.addTests(loader.loadTestsFromModule(test_module))


runner = unittest.TextTestRunner()
result = runner.run(suite)
result.printErrors()

# Make container properly exit, when tests fail
sys.exit(not result.wasSuccessful())
