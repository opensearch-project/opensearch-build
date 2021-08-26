import json
import os
import subprocess

from test_workflow.test_cluster import TestCluster


class PerformanceTestCluster(TestCluster):
    """
    Represents a performance test cluster. This class deploys the opensearch bundle with CDK and returns the private IP.
    """

    def __init__(self, bundle_manifest, config, stack_name, security):
        self.manifest = bundle_manifest
        self.security_id = config['Constants']['SecurityGroupId']
        self.vpc_id = config['Constants']['VpcId']
        self.account_id = config['Constants']['AccountId']
        self.region = config['Constants']['Region']
        self.role = config['Constants']['Role']
        self.work_dir = 'tools/cdk/mensor/single-node/'
        self.stack_name = stack_name
        self.output_file = 'output.json'
        self.ip_address = None
        self.security = 'enable' if security else 'disable'
        self.params = f'-c url={self.manifest.build.location} -c security_group_id={self.security_id} -c vpc_id={self.vpc_id}'\
                      f' -c account_id={self.account_id} -c region={self.region} -c stack_name={self.stack_name} -c security={self.security}'\
                      f' -c architecture={self.manifest.build.architecture} --require-approval=never --plugin cdk-assume-role-credential-plugin'\
                      f' -c assume-role-credentials:writeIamRoleName={self.role} -c assume-role-credentials:readIamRoleName={self.role}'

    def create(self):
        os.chdir(self.work_dir)
        command = f'cdk deploy {self.params} --outputs-file {self.output_file}'
        print(f'Executing "{command}" in {os.getcwd()}')
        subprocess.check_call(command, cwd=os.getcwd(), shell=True)
        with open(self.output_file, 'r') as read_file:
            load_output = json.load(read_file)
        self.ip_address = load_output[self.stack_name]['PrivateIp']
        print('Private IP:', self.ip_address)

    def endpoint(self):
        return self.ip_address

    def port(self):
        if self.security:
            return 443
        return 9200

    def destroy(self):
        os.chdir(self.work_dir)
        command = f'cdk destroy {self.params} --force'
        print(f'Executing "{command}" in {os.getcwd()}')
        subprocess.check_call(command, cwd=os.getcwd(), shell=True)
