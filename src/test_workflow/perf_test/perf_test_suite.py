import os
import subprocess

from system.working_directory import WorkingDirectory


class PerfTestSuite:
    """
    Represents a performance test suite. This class runs rally test on the deployed cluster with the provided IP.
    """

    def __init__(self, bundle_manifest, endpoint, security, current_workspace):
        self.manifest = bundle_manifest
        self.work_dir = "mensor/"
        self.endpoint = endpoint
        self.security = security
        self.current_workspace = current_workspace
        self.command = (
            f"pipenv run python test_config.py -i {self.endpoint} -b {self.manifest.build.id}"
            f" -a {self.manifest.build.architecture} -p {self.current_workspace}"
        )

    def execute(self):
        try:
            with WorkingDirectory(self.work_dir):
                dir = os.getcwd()
                subprocess.check_call("python3 -m pipenv install", cwd=dir, shell=True)
                subprocess.check_call("pipenv install", cwd=dir, shell=True)

                if self.security:
                    subprocess.check_call(f"{self.command} -s", cwd=dir, shell=True)
                else:
                    subprocess.check_call(f"{self.command}", cwd=dir, shell=True)
        finally:
            os.chdir(self.current_workspace)
