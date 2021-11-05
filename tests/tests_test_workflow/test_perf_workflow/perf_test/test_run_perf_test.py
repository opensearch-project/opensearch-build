# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from unittest.mock import patch

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
        ],
    )
    @patch("os.chdir")
    @patch("run_perf_test.TemporaryDirectory")
    @patch("run_perf_test.GitRepository")
    @patch("run_perf_test.PerfTestCluster.create")
    @patch("run_perf_test.PerfTestSuite")
    def test_run_perf_test(self, mock_perf_suite, mock_perf_test_cluster, mock_git_repo, mock_temp_drectory, *mock):
        mock_temp_drectory.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_perf_test_cluster.return_value.__enter__.return_value = ["endpoint", 1234]
        main()
        mock_git_repo.assert_called_with("https://github.com/opensearch-project/opensearch-infra.git", "main", os.path.join(tempfile.gettempdir(), "infra"))
        self.assertEqual(mock_perf_suite.return_value.execute.call_count, 1)
