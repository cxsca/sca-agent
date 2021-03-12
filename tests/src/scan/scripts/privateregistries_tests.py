import time
import requests

from test_base import ScanBase


class PrivateRegistriesTests(ScanBase):
    __test__ = True

    artifactory_base_url = 'http://localhost:8081/artifactory'
    artifactory_ui_url = 'http://localhost:8082/ui'

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
        response = session.post(f"{self.artifactory_ui_url}/api/v1/ui/auth/login",
                                headers={"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"},
                                json={"user": "admin", "password": "password", "type": "login"}, verify=False)
        print(f"Artifactory log-in result: `{response.status_code}`")
        self.assertEqual(response.status_code, 200)

        response = session.put(f"{self.artifactory_ui_url}/api/v1/ui/securityconfig",
                               headers={"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"},
                               json={"anonAccessEnabled": True}, verify=False)
        print(f"Artifactory security-config result: `{response.status_code}`")
        self.assertEqual(response.status_code, 200)

        # Publish to artifactory
        print("Publish to artifactory ...")

        with open("assets/parent-project-1.0.0.jar", "rb") as file_to_send:
            response = requests.put(f"{self.artifactory_base_url}/example-repo-local/com/checkmarx/parent-project/1.0.0/parent-project-1.0.0.jar",
                                    data=file_to_send, auth=('admin', 'password'), verify=False)
            print(f"Artifactory push jar result: `{response.status_code}`")
            self.assertEqual(response.status_code, 201)

        with open("assets/parent-project-1.0.0.pom", "rb") as file_to_send:
            response = requests.put(f"{self.artifactory_base_url}/example-repo-local/com/checkmarx/parent-project/1.0.0/parent-project-1.0.0.pom",
                                    data=file_to_send, auth=('admin', 'password'), verify=False)
            print(f"Artifactory push pom result: `{response.status_code}`")
            self.assertEqual(response.status_code, 201)

        self.authorize()
        self.create_project(projectAlias="ScaAgentTest-Private-Artifactory")

    def test_private_registries(self):
        # Get pre-signed url
        response = requests.post(f"{self.localhost}/api/uploads",
                                 headers={"Authorization": f"bearer {self.access_token}"}, verify=False)
        self.assertEqual(response.status_code, 200)
        pre_signed_url = response.json()["url"]

        # Upload child-project.zip to bucket
        with open("assets/child-project.zip", "rb") as file_to_send:
            response = requests.put(pre_signed_url, data=file_to_send, verify=False)
            self.assertEqual(response.status_code, 200)

        # Initiate a scan
        self.start_scan_and_wait(type="upload", url=pre_signed_url)

        # Handle the response
        response = requests.get(f"{self.localhost}/risk-management/risk-reports/{self.scan_id}/packages",
                                headers={"Authorization": f"bearer {self.access_token}"}, verify=False)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(any(any(nested_dp["name"] == "com.checkmarx:parent-project" for nested_dp in dp)
                                for dp in p["dependencyPaths"]) for p in response.json()))
