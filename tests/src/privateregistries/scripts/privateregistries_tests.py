import os
import time
import uuid
import requests

import unittest


class PrivateRegistriesTests(unittest.TestCase):
    __test__ = True

    await_time_in_secs = 15.0

    artifactory_base_url = 'http://localhost:8081/artifactory'
    artifactory_ui_url = 'http://localhost:8082/ui'

    def __init__(self, f):
        super(PrivateRegistriesTests, self).__init__(f)

        port = os.environ.get("AGENT_PORT") or "80"
        protocol = os.environ.get("AGENT_PROTOCOL") or "http"

        self.localhost = f"{protocol}://localhost:{port}"

        self.access_token = None
        self.project_id = None

    def setUp(self):
        print("Waiting for Artifactory ...")
        time.sleep(self.await_time_in_secs)
        for i in range(1, 20):
            try:
                response = requests.get(f"{self.artifactory_base_url}/api/system/ping", verify=False)
                if response.status_code == 200:
                    response = requests.get(f"{self.artifactory_ui_url}/api/v1/ui/auth/login", verify=False)
                    if response.status_code != 404 and response.status_code != 503:
                        print(f"Artifactory is ON")
                        break
                print(f"Artifactory is starting (check #{i} returned {response.status_code} status). Waiting ...")
                time.sleep(self.await_time_in_secs)
            except requests.exceptions.RequestException as e:
                print(f"Artifactory is still down (check #{i} thrown error with message '{str(e)}'). Waiting ...")
                time.sleep(self.await_time_in_secs)

        # Set artifactory up
        print("Set artifactory up ...")
        time.sleep(self.await_time_in_secs)

        session = requests.session()
        response = session.post(f"{self.artifactory_ui_url}/api/v1/ui/auth/login", headers={"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}, json={"user": "admin", "password": "password", "type": "login"}, verify=False)
        print(f"Artifactory log-in result: `{response.status_code}`")
        self.assertEqual(response.status_code, 200)

        response = session.put(f"{self.artifactory_ui_url}/api/v1/ui/securityconfig", headers={"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}, json={"anonAccessEnabled": True}, verify=False)
        print(f"Artifactory security-config result: `{response.status_code}`")
        self.assertEqual(response.status_code, 200)

        # Publish to artifactory
        print("Publish to artifactory ...")

        with open("assets/parent-project-1.0.0.jar", "rb") as file_to_send:
            response = requests.put(f"{self.artifactory_base_url}/example-repo-local/com/checkmarx/parent-project/1.0.0/parent-project-1.0.0.jar", data=file_to_send, auth=('admin', 'password'), verify=False)
            print(f"Artifactory push jar result: `{response.status_code}`")
            self.assertEqual(response.status_code, 201)

        with open("assets/parent-project-1.0.0.pom", "rb") as file_to_send:
            response = requests.put(f"{self.artifactory_base_url}/example-repo-local/com/checkmarx/parent-project/1.0.0/parent-project-1.0.0.pom", data=file_to_send, auth=('admin', 'password'), verify=False)
            print(f"Artifactory push pom result: `{response.status_code}`")
            self.assertEqual(response.status_code, 201)

        # Sign in
        request_body = {
            "grant_type": "password",
            "client_id": "sca_resource_owner",
            "scope": "sca_api",
            "acr_values": f"Tenant:{os.environ.get('TEST_SCA_TENANT')}",
            "username": f"{os.environ.get('TEST_SCA_USERNAME')}",
            "password": f"{os.environ.get('TEST_SCA_PASSWORD')}"
        }
        response = requests.post(f"{self.localhost}/identity/connect/token", headers={"Content-Type": "application/x-www-form-urlencoded"}, data=request_body, verify=False)
        self.assertEqual(response.status_code, 200)
        self.access_token = response.json()["access_token"]

        # Create a project
        request_body = {
            "name": f"ScaAgentTest-{uuid.uuid4().hex}"
        }
        response = requests.post(f"{self.localhost}/risk-management/projects", headers={"Authorization": f"bearer {self.access_token}"}, json=request_body, verify=False)
        self.assertEqual(response.status_code, 201)
        self.project_id = response.json()["id"]
        print(f"Project Id: `{self.project_id}`")

    def tearDown(self):
        response = requests.delete(f"{self.localhost}/risk-management/projects/{self.project_id}", headers={"Authorization": f"bearer {self.access_token}"}, verify=False)
        self.assertEqual(response.status_code, 204)

    def test_private_registries(self):
        # Get pre-signed url
        response = requests.post(f"{self.localhost}/api/uploads", headers={"Authorization": f"bearer {self.access_token}"}, verify=False)
        self.assertEqual(response.status_code, 200)
        pre_signed_url = response.json()["url"]

        # Upload child-project.zip to bucket
        with open("assets/child-project.zip", "rb") as file_to_send:
            response = requests.put(pre_signed_url, data=file_to_send, verify=False)
            self.assertEqual(response.status_code, 200)

        # Initiate a scan
        request_body = {
            "project": {
                "id": f"{self.project_id}",
                "type": "upload",
                "handler": {
                    "url": f"{pre_signed_url}"
                }
            }
        }
        response = requests.post(f"{self.localhost}/api/scans", headers={"Authorization": f"bearer {self.access_token}"}, json=request_body, verify=False)
        self.assertEqual(response.status_code, 201)
        scan_id = response.json()["id"]
        print(f"Scan Id: `{scan_id}`")

        # Wait for the scan
        num_of_checks = 20
        scan_completed = False
        for i in range(1, num_of_checks):
            print(f"Waiting for the scan to finish (attempt #{i}) ...")
            time.sleep(self.await_time_in_secs)

            response = requests.get(f"{self.localhost}/risk-management/scans/{scan_id}/status", headers={"Authorization": f"bearer {self.access_token}"}, verify=False)
            self.assertEqual(response.status_code, 200)
            scan_status = response.json()["name"].lower()
            if scan_status != "scanning":
                print(f"Scan finished with status `{scan_status}`")
                self.assertEqual(scan_status, "done")
                scan_completed = True
                break

        if not scan_completed:
            self.fail(f"Scan has not finished after {num_of_checks} checks")

        response = requests.get(f"{self.localhost}/risk-management/risk-reports/{scan_id}/packages", headers={"Authorization": f"bearer {self.access_token}"}, verify=False)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(any(any(nested_dp["name"] == "com.checkmarx:parent-project" for nested_dp in dp) for dp in p["dependencyPaths"]) for p in response.json()))
