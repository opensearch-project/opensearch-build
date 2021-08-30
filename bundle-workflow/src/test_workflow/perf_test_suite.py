import os
import subprocess


class PerformanceTestSuite:
    """
    Represents a performance test suite. This class runs rally test on the deployed cluster with the provided IP.
    """

    def __init__(self, bundle_manifest, endpoint, security):
        self.manifest = bundle_manifest
        self.work_dir = 'tools/cdk/mensor/mensor_tests'
        self.endpoint = endpoint
        self.security = security
        self.command = f'python test_config.py -i {self.endpoint} -b {self.manifest.build.id}'\
                       f' -a {self.manifest.build.architecture} '

    def execute(self):
        os.chdir(self.work_dir)
        dir = os.getcwd()
        # Install the depedencies for the private repo
        # TODO Move the installation to the repo itself
        subprocess.check_call('pip install boto3 requests setuptools retry dataclasses_json', cwd=dir, shell=True)

        if self.security:
            subprocess.check_call(f'{self.command} -s', cwd=dir, shell=True)
        else:
            subprocess.check_call(f'{self.command}', cwd=dir, shell=True)
