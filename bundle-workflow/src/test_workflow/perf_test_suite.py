import os
import subprocess


class PerformanceTestSuite:
    def __init__(self, bundle_manifest, endpoint, security):
        self.manifest = bundle_manifest
        self.work_dir = 'tools/cdk/mensor/mensor_tests'
        self.endpoint = endpoint
        self.security = security

    
    def execute(self):
        
        os.chdir(self.work_dir)
        dir = os.getcwd()
       
        #Install the depedencies for the private repo
        subprocess.check_call('pip3 install boto3 requests setuptools retry dataclasses_json', cwd=dir, shell=True)

        if self.security:
            subprocess.check_call(f'python3 test_config.py -i {self.endpoint} -b {self.manifest.build.id} -a {self.manifest.build.architecture} -s', cwd=dir, shell=True)
        else:
            subprocess.check_call(f'python3 test_config.py -i {self.endpoint} -b {self.manifest.build.id} -a {self.manifest.build.architecture}', cwd=dir, shell=True)
        