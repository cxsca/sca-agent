from test_base import ScanBase


class GoatScanTests(ScanBase):
    __test__ = True

    def test_goat_scan_small(self):
        scan_success = self.start_scan_and_wait(type="git", url="https://github.com/cxsca-sca-agent")
        self.assertTrue(scan_success)