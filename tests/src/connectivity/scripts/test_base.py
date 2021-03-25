import hmac
import os
import unittest
import hashlib


class ConnectivityBase(unittest.TestCase):
    __test__ = False

    def __init__(self, f):
        super(ConnectivityBase, self).__init__(f)
        port = os.environ.get("AGENT_PORT") or "80"
        protocol = os.environ.get("AGENT_PROTOCOL") or "http"

        self.localhost = f"{protocol}://localhost:{port}"
        self.salt = os.environ.get("WEBHOOK_SECRET")

    def make_sha1(self, input):
        return 'sha1=' + hmac.new(self.salt.encode('utf-8'), input.encode('utf-8'), hashlib.sha1).hexdigest()

    def make_sha256(self, input):
        return 'sha256=' + hmac.new(self.salt.encode('utf-8'), input.encode('utf-8'), hashlib.sha256).hexdigest()