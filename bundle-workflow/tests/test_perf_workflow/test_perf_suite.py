# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess
import unittest
from unittest.mock import patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test_suite import PerformanceTestSuite


class TestPerformanceSuite(unittest.TestCase):
    def setUp(self):
        os.chdir(os.path.dirname(__file__))
        manifest_file_handle = open("data/test_manifest.yaml", "r")
        self.manifest = BundleManifest.from_file(manifest_file_handle)
        self.endpoint = None
        self.perf_test_suite = PerformanceTestSuite(
            bundle_manifest=self.manifest, endpoint=None, security=False
        )
        manifest_file_handle.close()

    @patch('test_workflow.perf_test_suite.os.chdir')
    def test_execute(self, mock_chdir):
        with self.assertRaises(subprocess.CalledProcessError) as process_ret:
            self.perf_test_suite.execute()
            mock_chdir.assert_called_once_with('tools/cdk/mensor/single-node/')

        command = f'pipenv run python test_config.py -i {self.endpoint} -b {self.manifest.build.id}'\
                  f' -a {self.manifest.build.architecture} '
        self.assertEqual(process_ret.exception.cmd, command)
