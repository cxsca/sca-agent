from test_base import ScanBase
import os


class GoatScanTests(ScanBase):
    __test__ = True

    def test_goat_scan_small(self):
        exit_code = self.start_scan(project_name="ScaAgentSmallGoatScan", url="http://github.com/cxsca/sca-small-goat"
                                    , location_folder=f"{os.getcwd()}/assets/small")
        self.assertEqual(exit_code, 0)

    # def test_goat_scan(self):
    #     exit_code = self.start_scan("ScaAgentSmallGoatScan", "http://github.com/cxsca/sca-goat")
    #     self.assertEqual(exit_code, 0)
    #
    # def test_goat_scan_big(self):
    #     exit_code = self.start_scan("ScaAgentSmallGoatScan", "http://github.com/cxsca/sca-big-goat")
    #     self.assertEqual(exit_code, 0)
