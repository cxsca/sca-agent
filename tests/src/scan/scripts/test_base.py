import uuid
import requests
import unittest
import os
import time


class ScanBase(unittest.TestCase):
    __test__ = False

    await_time_in_secs = 15.0

    def __init__(self, f):
        super(ScanBase, self).__init__(f)

        port = os.environ.get("AGENT_PORT") or "80"
        protocol = os.environ.get("AGENT_PROTOCOL") or "http"

        self.localhost = f"{protocol}://localhost:{port}"

    def setUp(self):
        self.authorize()

    def tearDown(self):
        response = requests.delete(f"{self.localhost}/risk-management/projects/{self.project_id}",
                                   headers={"Authorization": f"bearer {self.access_token}"}, verify=False)
        self.assertEqual(response.status_code, 204)

    # Sign in
    def authorize(self):

        auth_body = {
            "grant_type": "password",
            "client_id": "sca_resource_owner",
            "scope": "sca_api",
            "acr_values": f"Tenant:{os.environ.get('TEST_SCA_TENANT')}",
            "username": f"{os.environ.get('TEST_SCA_USERNAME')}",
            "password": f"{os.environ.get('TEST_SCA_PASSWORD')}"
        }

        response = requests.post(f"{self.localhost}/identity/connect/token",
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             data=auth_body, verify=False)

        self.assertEqual(response.status_code, 200)
        self.access_token = response.json()["access_token"]

    def create_project(self, projectAlias):

        project_body = {
            "name": f"{projectAlias}-{uuid.uuid4().hex}"
        }

        response = requests.post(f"{self.localhost}/risk-management/projects",
                             headers={"Authorization": f"bearer {self.access_token}"},
                             json=project_body, verify=False)

        self.assertEqual(response.status_code, 201)
        self.project_id = response.json()["id"]
        print(f"Project Id: `{self.project_id}`")

    # Start Scan
    def start_scan_and_wait(self, type, url, num_of_checks=20):

        # Initiate a scan
        request_body = {
            "project": {
                "id": f"{self.project_id}",
                "type": f"{type}",
                "handler": {
                    "url": f"{url}"
                }
            }
        }
        response = requests.post(f"{self.localhost}/api/scans", headers={"Authorization": f"bearer {self.access_token}"}, json=request_body, verify=False)
        self.assertEqual(response.status_code, 201)
        scan_id = response.json()["id"]
        print(f"Scan Id: `{scan_id}`")

        for i in range(1, num_of_checks):

            print(f"Waiting for the scan to finish (attempt #{i}) ...")
            time.sleep(self.await_time_in_secs)

            response = requests.get(f"{self.localhost}/risk-management/scans/{scan_id}/status", headers={"Authorization": f"bearer {self.access_token}"}, verify=False)
            self.assertEqual(response.status_code, 200)
            scan_status = response.json()["name"].lower()

            if scan_status != "scanning":
                print(f"Scan finished with status `{scan_status}`")
                self.assertEqual(scan_status, "done")
                return True

        return False







