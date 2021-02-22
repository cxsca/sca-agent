import os
import unittest


class ConnectivityBase(unittest.TestCase):
    __test__ = False

    def __init__(self, f):
        super(ConnectivityBase, self).__init__(f)
        port = os.environ.get("AGENT-PORT") or "80"
        protocol = os.environ.get("AGENT-PROTOCOL") or "http"

        self.localhost = f"{protocol}://localhost:{port}"