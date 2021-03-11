import requests
import time

from test_base import ConnectivityBase


class PrivateRegistriesTests(ConnectivityBase):
    __test__ = True

    def test_private_registries(self):
        await_time_in_secs = 15.0
        artifactory_base_url = 'http://localhost:8081/artifactory'
        artifactory_ui_url = 'http://localhost:8082/ui'

        print("Waiting for Artifactory ...")
        time.sleep(await_time_in_secs)
        for i in range(1, 20):
            try:
                response = requests.get(f"{artifactory_base_url}/api/system/ping", verify=False)
                if response.status_code == 200:
                    response = requests.get(f"{artifactory_ui_url}/api/v1/ui/auth/login", verify=False)
                    if response.status_code != 404 and response.status_code != 503:
                        print(f"Artifactory is ON")
                        break
                print(f"Artifactory is starting (check #{i} returned {response.status_code} status). Waiting ...")
                time.sleep(await_time_in_secs)
            except requests.exceptions.RequestException as e:
                print(f"Artifactory is still down (check #{i} thrown error with message '{str(e)}'). Waiting ...")
                time.sleep(await_time_in_secs)

        # Set artifactory up
        print("Set artifactory up ...")
        time.sleep(await_time_in_secs)

        session = requests.session()
        response = session.post(f"{artifactory_ui_url}/api/v1/ui/auth/login", headers={"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}, json={"user": "admin", "password": "password", "type": "login"}, verify=False)
        print(f"Artifactory log-in result: `{response.status_code}`")
        self.assertEqual(response.status_code, 200)

        response = session.put(f"{artifactory_ui_url}/api/v1/ui/securityconfig", headers={"Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest"}, json={"anonAccessEnabled": True}, verify=False)
        print(f"Artifactory security-config result: `{response.status_code}`")
        self.assertEqual(response.status_code, 200)

        # Publish to artifactory
        print("Publish to artifactory ...")

        with open("assets/parent-project-1.0.0.jar", "rb") as file_to_send:
            response = requests.put(f"{artifactory_base_url}/example-repo-local/com/checkmarx/parent-project/1.0.0/parent-project-1.0.0.jar", data=file_to_send, auth=('admin', 'password'), verify=False)
            print(f"Artifactory push jar result: `{response.status_code}`")
            self.assertEqual(response.status_code, 201)

        with open("assets/parent-project-1.0.0.pom", "rb") as file_to_send:
            response = requests.put(f"{artifactory_base_url}/example-repo-local/com/checkmarx/parent-project/1.0.0/parent-project-1.0.0.pom", data=file_to_send, auth=('admin', 'password'), verify=False)
            print(f"Artifactory push pom result: `{response.status_code}`")
            self.assertEqual(response.status_code, 201)

        # Test Scan
