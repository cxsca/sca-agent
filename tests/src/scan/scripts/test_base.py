import unittest
import os


class ScanBase(unittest.TestCase):
    __test__ = False

    def __init__(self, f):
        super(ScanBase, self).__init__(f)

        port = os.environ.get("AGENT_PORT") or "80"
        protocol = os.environ.get("AGENT_PROTOCOL") or "http"

        self.CXAccount = os.environ.get("SCATENANT")
        self.CXUser = os.environ.get("SCAUSERNAME")
        self.CXPasswordSecret = os.environ.get("SCAPASSWORDSECRET")

        self.localhost = f"{protocol}://localhost:{port}"

    def start_scan(self, project_name, url, location_folder):
        return os.system(f"CLI/runCxConsole.sh scascan "
                         f"-scaapiurl {self.localhost} "
                         f"-projectname {project_name} "
                         f"-scaUsername {self.CXUser} "
                         f"-scaPassword {self.CXPasswordSecret} "
                         f"-scaAccount {self.CXAccount} "
                         f"{location_argument}")

