# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess
import unittest
from unittest.mock import patch

import yaml

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test_cluster import PerformanceTestCluster


class TestPerformanceCluster(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))
        manifest_file_handle = open("data/test_manifest.yaml", "r")
        self.manifest = BundleManifest.from_file(manifest_file_handle)
        config_file_handle = open("data/config.yml", "r")
        config = yaml.load(config_file_handle, Loader=yaml.FullLoader)
        self.stack_name = None
        self.security = 'disable'
        self.perf_test_cluster = PerformanceTestCluster(
            bundle_manifest=self.manifest, config=config, stack_name=self.stack_name, security=self.security
        )
        self.security_id = config['Constants']['SecurityGroupId']
        self.vpc_id = config['Constants']['VpcId']
        self.account_id = config['Constants']['AccountId']
        self.region = config['Constants']['Region']
        self.role = config['Constants']['Role']
        manifest_file_handle.close()
        config_file_handle.close()

    @patch('test_workflow.perf_test_cluster.os.chdir')
    def test_create(self, mock_chdir):
        with self.assertRaises(subprocess.CalledProcessError) as process_ret:
            self.perf_test_cluster.create()
            mock_chdir.assert_called_once_with('tools/cdk/mensor/single-node/')

        self.assertEqual(process_ret.exception.returncode, 127)
        command = f'cdk deploy -c url={self.manifest.build.location} -c security_group_id={self.security_id} -c vpc_id={self.vpc_id}'\
                  f' -c account_id={self.account_id} -c region={self.region} -c stack_name={self.stack_name} -c security=enable'\
                  f' -c architecture={self.manifest.build.architecture} --require-approval=never --plugin cdk-assume-role-credential-plugin'\
                  f' -c assume-role-credentials:writeIamRoleName={self.role} -c assume-role-credentials:readIamRoleName={self.role} --outputs-file output.json'
        self.assertEqual(process_ret.exception.cmd, command)

    def test_endpoint(self):
        self.assertEqual(self.perf_test_cluster.endpoint(), None)

    def test_port(self):
        self.assertEqual(self.perf_test_cluster.port(), 443)

    @patch('test_workflow.perf_test_cluster.os.chdir')
    def test_destroy(self, mock_chdir):
        with self.assertRaises(subprocess.CalledProcessError) as process_ret:
            self.perf_test_cluster.destroy()
            mock_chdir.assert_called_once_with('tools/cdk/mensor/single-node/')

        self.assertEqual(process_ret.exception.returncode, 1)
        command = f'cdk destroy -c url={self.manifest.build.location} -c security_group_id={self.security_id} -c vpc_id={self.vpc_id}'\
                  f' -c account_id={self.account_id} -c region={self.region} -c stack_name={self.stack_name} -c security=enable'\
                  f' -c architecture={self.manifest.build.architecture} --require-approval=never --plugin cdk-assume-role-credential-plugin'\
                  f' -c assume-role-credentials:writeIamRoleName={self.role} -c assume-role-credentials:readIamRoleName={self.role} --force'
        self.assertEqual(process_ret.exception.cmd, command)
