# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import os
import tempfile
import unittest
from typing import Any
from unittest.mock import Mock, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_args import PerfArgs
from test_workflow.perf_test.perf_test_runners import PerfTestRunners


class TestPerfTestRunnerOpenSearch(unittest.TestCase):

    @patch(
        "argparse._sys.argv",
        [
            "run_perf_test.py",
            "--bundle-manifest",
            os.path.join(os.path.dirname(__file__), "data", "bundle_manifest.yml"),
            "--config",
            os.path.join(os.path.dirname(__file__), "data", "cluster_config.yml"),
            "--workload",
            "nyc_taxis",
            "--workload-options",
            "{\"workload-params\":\"number_of_shards:5,number_of_replicas:0,bulk_size:2500\"}",
            "--warmup-iters",
            "2",
            "--test-iters",
            "3"
        ],
    )
    @patch("os.chdir")
    @patch("test_workflow.perf_test.perf_test_runner_opensearch.TemporaryDirectory")
    @patch("test_workflow.perf_test.perf_test_runner_opensearch.GitRepository")
    @patch("test_workflow.perf_test.perf_test_runner_opensearch.PerfSingleNodeCluster.create")
    @patch("test_workflow.perf_test.perf_test_runner_opensearch.PerfTestSuite")
    def test_run(self, mock_suite: Mock, mock_cluster: Mock, mock_git: Mock, mock_temp_directory: Mock, *mocks: Any) -> None:
        mock_temp_directory.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_cluster.return_value.__enter__.return_value = mock_cluster

        perf_args = PerfArgs()
        test_manifest = BundleManifest.from_file(perf_args.bundle_manifest)
        runner = PerfTestRunners.from_args(perf_args, test_manifest)
        runner.run()

        mock_git.assert_called_with("https://github.com/opensearch-project/opensearch-infra.git", "main",
                                    os.path.join(tempfile.gettempdir(), "infra"))
        self.assertEqual(mock_suite.call_count, 1)
        self.assertEqual(mock_cluster.call_count, 1)
        self.assertEqual(mock_git.call_count, 1)
        self.assertEqual(mock_temp_directory.call_count, 1)
