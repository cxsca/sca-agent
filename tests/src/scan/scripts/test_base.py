import uuid
import requests
import unittest
import os
import time


class ScanBase(unittest.TestCase):
    """
        A base class for tests, where scanning in SCA must be performed
    """

    __test__ = False

    await_time_in_secs = 15.0

    def __init__(self, f):
        super(ScanBase, self).__init__(f)

        port = os.environ.get("AGENT_PORT") or "80"
        protocol = os.environ.get("AGENT_PROTOCOL") or "http"

        self.localhost = f"{protocol}://localhost:{port}"

        self.access_token = None
        self.project_id = None

    def setUp(self):
        """
            Default setup for the Tests
        """
        self.authorize()

    def tearDown(self):
        """
            Exists from the tests and deletes the project in SCA, that was temporarily produced for the test
        """
        response = requests.delete(f"{self.localhost}/risk-management/projects/{self.project_id}",
                                   headers={"Authorization": f"bearer {self.access_token}"}, verify=False)
        self.assertEqual(response.status_code, 204)
        self.project_id = None

    def authorize(self):
        """
            Get access token to authorize in SCA web application
        """
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

    def create_project(self, project_alias):
        """
            Creates a project in SCA for the particular Scan
        :param project_alias: Name for the project to be used
        :return: The SCA project with hex postfix. Format {projectAlias}-{random_hex}
        """
        project_body = {
            "name": f"{project_alias}-{uuid.uuid4().hex}"
        }

        response = requests.post(f"{self.localhost}/risk-management/projects",
                                 headers={"Authorization": f"bearer {self.access_token}"},
                                 json=project_body, verify=False)

        self.assertEqual(response.status_code, 201)
        self.project_id = response.json()["id"]
        print(f"Project Id: `{self.project_id}`")

    # Start Scan
    def start_scan_and_wait(self, scan_type, url, num_of_checks=20):
        """
            Starts the SCA scan to find vulnerabilities in 3rd parties
        :param scan_type: `upload` or `git`
        :param url: for `upload` url must be a pre-signed url, generated sca api and with downloaded asset.
                    for `git` url must be a public! repository url
        :param num_of_checks: Number of checks for scan to wait for. One check is 15 sec await time. In case the scan
                              was not on time - the test will fail.
        :return: exit code zero if everything is ok
        :raise: unittest.fail in case the scan was not on time
        """
        request_body = {
            "project": {
                "id": f"{self.project_id}",
                "type": f"{scan_type}",
                "handler": {
                    "url": f"{url}"
                }
            }
        }
        response = requests.post(f"{self.localhost}/api/scans",
                                 headers={"Authorization": f"bearer {self.access_token}"},
                                 json=request_body, verify=False)
        self.assertEqual(response.status_code, 201)
        self.scan_id = response.json()["id"]
        print(f"Scan Id: `{self.scan_id}`")

        scan_completed = False
        for i in range(1, num_of_checks):

            print(f"Waiting for the scan to finish (attempt #{i}) ...")
            time.sleep(self.await_time_in_secs)

            response = requests.get(f"{self.localhost}/risk-management/scans/{self.scan_id}/status",
                                    headers={"Authorization": f"bearer {self.access_token}"}, verify=False)
            self.assertEqual(response.status_code, 200)
            scan_status = response.json()["name"].lower()

            if scan_status != "scanning":
                print(f"Scan finished with status `{scan_status}`")
                self.assertEqual(scan_status, "done")
                scan_completed = True
                break

        if not scan_completed:
            self.fail(f"Scan has not finished after {num_of_checks} checks")

        return scan_completed
