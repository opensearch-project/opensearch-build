# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from unittest.mock import MagicMock, call, patch

import pytest

from run_perf_test import main


class TestRunPerfTest(unittest.TestCase):
    # @pytest.fixture(autouse=True)
    # def capfd(self, capfd):
    #     self.capfd = capfd

    # @patch("argparse._sys.argv", ["run_perf_test.py", "-h"])
    # def test_usage(self):
    #     with self.assertRaises(SystemExit):
    #         main()

    #     out, _ = self.capfd.readouterr()
    #     self.assertTrue(out.startswith("usage:"))

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__), "../../manifests/1.1.0/opensearch-1.1.0.yml"
        )
    )

    CONFIG_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__), "../tests/test_perf_workflow/perf_test/data/config.yml"
        )
    )

    #@patch("os.chdir")
    @patch(
        "run_perf_test.GitRepository", return_value=MagicMock(working_directory="dummy")
    )
    @patch(
        "argparse._sys.argv",
        [
            "run_perf_test.py",
            "--bundle-manifest",
            OPENSEARCH_MANIFEST,
            "--stack",
            "xyz",
            "--config",
            CONFIG_MANIFEST,
            "--keep"
        ],
    )
    @patch("run_perf_test.TemporaryDirectory")
    #@patch("run_perf_test.WorkingDirectory")
    #@patch("run_perf_test.PerfTestCluster")
    #@patch("run_perf_test.PerfTestSuite")
    def test_main(self, mock_temp, mock_repo):
        mock_temp.return_value.__enter__.return_value = tempfile.gettempdir()
        main()

        mock_repo.assert_has_calls(
            [
                call(
                    "https://github.com/opensearch-project/OpenSearch.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "OpenSearch"),
                    None,
                )
            ]
        )
