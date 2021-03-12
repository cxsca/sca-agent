from test_base import ScanBase


class GoatScanTests(ScanBase):
    __test__ = True

    def test_goat_scan_small(self):
        self.create_project("SCAAgent-Small-Goat")
        scan_success = self.start_scan_and_wait(type="git", url="https://github.com/cxsca/sca-small-goat")
        self.assertTrue(scan_success)

    def test_goat_scan(self):
        self.create_project("SCAAgent-Goat")
        scan_success = self.start_scan_and_wait(type="git", url="https://github.com/sca-small-goat", num_of_checks=30)
        self.assertTrue(scan_success)

    def test_goat_scan_big(self):
        self.create_project("SCAAgent-Big-Goat")
        scan_success = self.start_scan_and_wait(type="git", url="https://github.com/sca-big-goat", num_of_checks=60)
        self.assertTrue(scan_success)