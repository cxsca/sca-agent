import os
import tempfile
import shutil

directories_to_copy = ["volumes"]
assets_to_copy = ["docker-compose.yml",
                  "create_env_file.py",
                  "setup.sh",
                  ".env.defaults"]


class TestsBase:

    def __init__(self, test_name, custom_compose_file=None, custom_env_file=None, verbose_mode=False):

        self.TEST_NAME = test_name
        self.TEST_FOLDER = os.path.dirname(os.path.realpath(__file__))
        self.BASE_FOLDER = os.path.abspath(os.path.join(self.TEST_FOLDER, '../..'))
        self.TEMP_DIR = tempfile.TemporaryDirectory()

        self.custom_compose_file = custom_compose_file
        self.custom_env_file = custom_env_file
        self.verbose_mode = "--verbose" if verbose_mode else ""

    def _copy_assets(self):

        # Copy directories
        for directory in directories_to_copy:
            shutil.copytree(os.path.join(self.BASE_FOLDER, directory), os.path.join(self.TEMP_DIR.name, directory))

        # Copy files
        for asset_file in assets_to_copy:
            shutil.copy(os.path.join(self.BASE_FOLDER, asset_file), os.path.join(self.TEMP_DIR.name, asset_file))

        os.system(f"cd {self.TEMP_DIR.name} | sed -i \"s/\\${{AGENT_VERSION}}/Test-Version/g\" docker-compose.yml")

    def agent_run(self):
        self._copy_assets()

        print("Setting up the agent")

        # Run setup
        os.system(f"cd {self.TEMP_DIR.name} | ./setup.sh")

        # Run docker compose
        os.system(f"docker-compose -p {self.TEST_NAME} up -d")

    def agent_stop(self):
        os.system(f"cd {self.TEMP_DIR.name} | docker-compose -p {self.TEST_NAME} down")

    def run_test(self):
        pass

    def __del__(self):
        self.TEMP_DIR.cleanup()
