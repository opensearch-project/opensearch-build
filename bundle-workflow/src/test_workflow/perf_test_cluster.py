import json
import os
import subprocess

from test_workflow.test_cluster import TestCluster


class PerformanceTestCluster(TestCluster):
    def __init__(self, bundle_manifest, config, stack_name, security):
        self.manifest = bundle_manifest
        self.security_id = config['Constants']['SecurityGroupId']
        self.vpc_id = config['Constants']['VpcId']
        self.account_id = config['Constants']['AccountId']
        self.region = config['Constants']['Region']
        self.work_dir = 'tools/cdk/mensor/single-node/'
        self.stack_name = stack_name
        self.output_file = 'output.json'
        self.ip_address = None
        self.security = security

    def create(self):
        os.chdir(self.work_dir)
        dir = os.getcwd()

        security = 'disable'
        if self.security:
            security = 'enable'

        command = f'cdk deploy -c url={self.manifest.build.location} -c security_group_id={self.security_id} -c vpc_id={self.vpc_id} '\
                  f'-c account_id={self.account_id} -c region={self.region} -c stack_name={self.stack_name} -c security={security} '\
                  f'-c architecture={self.manifest.build.architecture} --require-approval=never -c assume-role-credentials:writeIamRoleName=cfn-set-up '\
                  f'-c assume-role-credentials:readIamRoleName=cfn-set-up --outputs-file {self.output_file}'
        print(f'Executing "{command}" in {dir}')
        subprocess.check_call(command, cwd=dir, shell=True)
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
        security = 'disable'
        if self.security:
            security = 'enable'

        command = f'cdk destroy -c url={self.manifest.build.location} -c security_group_id={self.security_id} -c vpc_id={self.vpc_id} '\
                  f'-c account_id={self.account_id} -c region={self.region} -c stack_name={self.stack_name} -c security={security} '\
                  f'-c architecture={self.manifest.build.architecture} --require-approval=never -c assume-role-credentials:writeIamRoleName=cfn-set-up '\
                  f'-c assume-role-credentials:readIamRoleName=cfn-set-up'
        print(f'Executing "{command}" in {dir}')
        subprocess.check_call(command, cwd=dir, shell=True)
