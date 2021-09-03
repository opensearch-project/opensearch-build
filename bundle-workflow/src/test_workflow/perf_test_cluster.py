import json
import os
import subprocess
from contextlib import contextmanager

from test_workflow.test_cluster import TestCluster


class Cluster:
    @contextmanager
    def create(manifest, config, stack_name, security):
        perf_test_cluster = PerfTestCluster(manifest, config, stack_name, security)
        try:
            perf_test_cluster.create()
            yield perf_test_cluster.endpoint()
        finally:
            perf_test_cluster.destroy()


class PerfTestCluster(TestCluster):
    """
    Represents a performance test cluster. This class deploys the opensearch bundle with CDK and returns the private IP.
    """

    def __init__(self, bundle_manifest, config, stack_name, security):
        self.manifest = bundle_manifest
        self.work_dir = 'tools/cdk/mensor/single-node/'
        self.stack_name = stack_name
        self.cluster_endpoint = None
        self.cluster_port = None
        self.output_file = 'output.json'
        self.ip_address = None
        self.security = 'enable' if security else 'disable'
        role = config['Constants']['Role']
        params_dict = {
            'url': self.manifest.build.location,
            'security_group_id': config['Constants']['SecurityGroupId'],
            'vpc_id': config['Constants']['VpcId'],
            'account_id': config['Constants']['AccountId'],
            'region': config['Constants']['Region'],
            'stack_name': self.stack_name,
            'security': self.security,
            'architecture': self.manifest.build.architecture,
        }
        params_list = []
        for key, value in params_dict.items():
            params_list.append(f' -c {key}={value}')
        role_params = f' --require-approval=never --plugin cdk-assume-role-credential-plugin'\
                      f' -c assume-role-credentials:writeIamRoleName={role} -c assume-role-credentials:readIamRoleName={role} '
        self.params = ''.join(params_list) + role_params

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
        self.cluster_endpoint = self.ip_address
        return self.cluster_endpoint

    def port(self):
        self.cluster_port = 443 if self.security == 'enable' else 9200
        return self.cluster_port

    def destroy(self):
        os.chdir(self.work_dir)
        command = f'cdk destroy {self.params} --force'
        print(f'Executing "{command}" in {os.getcwd()}')
        subprocess.check_call(command, cwd=os.getcwd(), shell=True)
