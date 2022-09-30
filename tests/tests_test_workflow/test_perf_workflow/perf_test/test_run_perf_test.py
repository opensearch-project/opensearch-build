# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any
from unittest.mock import Mock, patch

from run_perf_test import main


class TestRunPerfTest(unittest.TestCase):
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
    @patch("test_workflow.perf_test.perf_test_runners.PerfTestRunnerOpenSearchPlugins.run_tests")
    @patch("test_workflow.perf_test.perf_test_runners.PerfTestRunnerOpenSearch.run_tests")
    def test_run_perf_test(self, os_mock_runner: Mock, plugin_mock_runner: Mock, *mock: Any) -> None:
        main()
        self.assertEqual(1, os_mock_runner.call_count)
        self.assertEqual(0, plugin_mock_runner.call_count)

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
            "3",
            "--component",
            "abc"
        ],
    )
    @patch("test_workflow.perf_test.perf_test_runners.PerfTestRunnerOpenSearchPlugins.run_tests")
    @patch("test_workflow.perf_test.perf_test_runners.PerfTestRunnerOpenSearch.run_tests")
    def test_run_perf_test_plugins(self, os_mock_runner: Mock, plugin_mock_runner: Mock, *mock: Any) -> None:
        main()
        self.assertEqual(0, os_mock_runner.call_count)
        self.assertEqual(1, plugin_mock_runner.call_count)
