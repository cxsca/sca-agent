import requests
from test_base import ConnectivityBase


class CxFlowTests(ConnectivityBase):
    __test__ = True

    def test_cxflow_connectivity(self):
        webhook_url = f"{self.localhost}/webhook"
        cxflow_data = None
        cxflow_headers = None

        result = requests.post(url=webhook_url, data=cxflow_data, headers=cxflow_headers, verify=False)

        self.assertEqual(result.status_code, 200)
