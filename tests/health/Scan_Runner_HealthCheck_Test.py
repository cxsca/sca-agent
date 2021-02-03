from tests.base.tests_base import TestsBase


class Scan_Runner_HealthCheck_Test(TestsBase):

    def __init__(self):
        super().__init__(test_name="ScanRunnerHealthCheck")

    def run_test(self):
        # Run the agent
        super(Scan_Runner_HealthCheck_Test, self).agent_run()

        # Stop the agent
        super(Scan_Runner_HealthCheck_Test, self).agent_stop()
