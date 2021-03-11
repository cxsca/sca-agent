from test_base import ScanBase
import os


class GoatScanTests(ScanBase):
    __test__ = True

    def test_goat_scan_small(self):
        exit_code = self.start_scan(project_name="ScaAgentSmallGoatScan",
                                    location_directory=f"{os.getcwd()}/assets/small")
        self.assertEqual(exit_code, 0)

    def test_goat_scan(self):
         exit_code = self.start_scan(project_name="ScaAgentGoatScan",
                                     location_directory=f"{os.getcwd()}/assets/normal")
         self.assertEqual(exit_code, 0)

    def test_goat_scan_big(self):
        exit_code = self.start_scan(project_name="ScaAgentBigGoatScan",
                                    location_directory=f"{os.getcwd()}/assets/big")
        self.assertEqual(exit_code, 0)
