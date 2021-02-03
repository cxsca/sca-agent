from tests.base.tests_base import TestsBase


class ScanRunnerHealthcheckTest(TestsBase):

    def __init__(self):
        super().__init__(test_name="ScanRunnerHealthCheck")

    def run_test(self):
        # Run the agent
        super(ScanRunnerHealthcheckTest, self).agent_run()

        # Stop the agent
        super(ScanRunnerHealthcheckTest, self).agent_stop()
