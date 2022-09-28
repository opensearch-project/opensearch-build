# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_test_suite import PerfTestSuite


class TestPerfTestSuite(unittest.TestCase):
    def setUp(self) -> None:
        self.args = Mock()
        self.args.workload = "nyc_taxis"
        self.args.workload_options = "{}"
        self.args.warmup_iters = 0
        self.args.test_iters = 1
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.manifest_filename = os.path.join(self.data_path, "bundle_manifest.yml")
        self.manifest = BundleManifest.from_path(self.manifest_filename)
        self.endpoint = "abc.com"

        self.perf_test_suite = PerfTestSuite(bundle_manifest=self.manifest, endpoint=self.endpoint, security=False,
                                             current_workspace="current_workspace", test_results_path="test/results/",
                                             args=self.args)

    def test_execute_default(self) -> None:
        perf_test_suite = PerfTestSuite(bundle_manifest=self.manifest, endpoint=self.endpoint, security=False,
                                        current_workspace="current_workspace", test_results_path="test/results/", args=self.args)
        with patch("test_workflow.perf_test.perf_test_suite.os.chdir"):
            with patch("subprocess.check_call") as mock_check_call:
                perf_test_suite.execute()
                self.assertEqual(mock_check_call.call_count, 2)
                self.assertEqual(
                    perf_test_suite.command, "pipenv run python test_config.py -e abc.com"
                    " -b 41d5ae25183d4e699e92debfbe3f83bd -a x64 -p test/results/ --workload nyc_taxis"
                    " --workload-options '{}' --warmup-iters 0 --test-iters 1 --scenario-type DEFAULT --owner opensearch-devops")

    def test_execute_different_owner_and_scenario(self) -> None:
        perf_test_suite = PerfTestSuite(bundle_manifest=self.manifest, endpoint=self.endpoint, security=False,
                                        current_workspace="current_workspace", test_results_path="test/results/", args=self.args,
                                        owner="test-owner", scenario="CROSS_CLUSTER_REPLICATION")
        with patch("test_workflow.perf_test.perf_test_suite.os.chdir"):
            with patch("subprocess.check_call") as mock_check_call:
                perf_test_suite.execute()
                self.assertEqual(mock_check_call.call_count, 2)
                self.assertEqual(
                    perf_test_suite.command, "pipenv run python test_config.py -e abc.com"
                    " -b 41d5ae25183d4e699e92debfbe3f83bd -a x64 -p test/results/ --workload nyc_taxis"
                    " --workload-options '{}' --warmup-iters 0 --test-iters 1 --scenario-type CROSS_CLUSTER_REPLICATION"
                    " --owner test-owner")

    def test_execute_with_dict_endpoint(self) -> None:
        endpoint = {
            "default": ["cluster-1"],
            "second_cluster": ["cluster-2"]
        }

        perf_test_suite = PerfTestSuite(
            bundle_manifest=self.manifest,
            endpoint=endpoint,
            security=False,
            current_workspace="current_workspace",
            test_results_path="test/results/",
            args=self.args
        )

        with patch("test_workflow.perf_test.perf_test_suite.os.chdir"):
            with patch("subprocess.check_call") as mock_check_call:
                perf_test_suite.execute()
                self.assertEqual(mock_check_call.call_count, 2)
                self.assertEqual(
                    perf_test_suite.command, "pipenv run python test_config.py -t '{\"default\": [\"cluster-1\"], \"second_cluster\": [\"cluster-2\"]}'"
                    " -b 41d5ae25183d4e699e92debfbe3f83bd -a x64 -p test/results/ --workload nyc_taxis"
                    " --workload-options '{}' --warmup-iters 0 --test-iters 1 --scenario-type DEFAULT --owner opensearch-devops")
