import requests
from test_base import ConnectivityBase


class PreSignedUrlTests(ConnectivityBase):
    __test__ = True

    def test_pre_signed(self):

        # Get pre-signed url
        response = requests.post(f"{self.localhost}/api/uploads")
        pre_signed_url = response.json()["url"]

        # upload the file to bucket
        with open("assets/test_upload.txt", "rb") as file_to_send:
            upload_response = requests.put(pre_signed_url, data=file_to_send)
            self.assertEqual(upload_response.status_code, 200)