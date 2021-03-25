import requests
import time
from test_base import ConnectivityBase


class CxFlowTests(ConnectivityBase):
    __test__ = True

    def test_cxflow_connectivity(self):
        # Wait for CxFlow to wake up correctly - about that time for secure startup
        time.sleep(60)

        webhook_url = f"{self.localhost}/webhook"
        github_hook_id = 288470543

        f = open("assets/cxflowtestbody.json", "r", encoding='utf-8')
        payload = f.read()
        f.close()

        cx_flow_headers = {
            'Host' : 'ScaAgent',
            'User-Agent': 'GitHub-Hookshot/2cd6345',
            'Content-Length': f"{len(payload)}",
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'X-Forwarded-For': '140.82.115.144',
            'X-Forwarded-Proto': 'https',
            'X-Github-Delivery': '07dc5e70-8d4b-11eb-9006-f76f3478eaf3',
            'X-Github-Event': 'push',
            'X-Github-Hook-Id': str(github_hook_id),
            'X-Github-Hook-Installation-Target-Id': '346297126',
            'X-Github-Hook-Installation-Target-Type': 'repository',
            'X-Hub-Signature': f'{self.make_sha1(payload)}',
            'X-Hub-Signature-256': f'{self.make_sha256(payload)}',
            'Accept-Encoding': 'gzip'
        }

        result = requests.post(url=webhook_url, data=payload, headers=cx_flow_headers, verify=False)

        self.assertEqual(result.status_code, 200)
