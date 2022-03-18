# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from unittest.mock import Mock, patch

import pytest

from run_perf_test import main


class TestRunPerfTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capfd(self, capfd):
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_perf_test.py", "--help"])
    def test_usage(self):
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    BUNDLE_MANIFEST_PATH = os.path.join(
        os.path.dirname(__file__),
        "jenkins",
        "data",
    )

    CONFIG_ROOT_PATH = os.path.join(
        os.path.dirname(__file__),
        "data",
    )

    OPENSEARCH_BUNDLE_MANIFEST = os.path.realpath(os.path.join(BUNDLE_MANIFEST_PATH, "opensearch-1.3.0-bundle.yml"))
    PERF_TEST_CONFIG = os.path.realpath(os.path.join(CONFIG_ROOT_PATH, "perf-test-config.yml"))

    @patch("argparse._sys.argv", ["run_perf_test.py", "--bundle-manifest", OPENSEARCH_BUNDLE_MANIFEST,
                                  "--stack", "test-stack", "--config", PERF_TEST_CONFIG])
    @patch("run_perf_test.PerfTestCluster.create")
    @patch("run_perf_test.PerfTestSuite")
    @patch("run_perf_test.WorkingDirectory")
    @patch("run_perf_test.TemporaryDirectory")
    @patch("run_perf_test.GitRepository")
    def test_default_execute_perf_test(self, mock_git, mock_temp, mock_working_dir, mock_suite, mock_cluster, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_create = Mock()
        mock_create.__enter__ = Mock(return_value=('test-endpoint', 1234))
        mock_create.__exit__ = Mock(return_value=None)
        mock_cluster.return_value = mock_create

        mock_execute = Mock()
        mock_suite.return_value.execute = mock_execute

        main()
        self.assertEqual(1, mock_cluster.call_count)
        self.assertEqual(1, mock_suite.call_count)
        self.assertEqual(1, mock_git.call_count)
        self.assertEqual(1, mock_execute.call_count)
        self.assertEqual([], mock_execute.call_args)
        self.assertIn(True, mock_suite.call_args[0])

    @patch("argparse._sys.argv", ["run_perf_test.py", "--bundle-manifest", OPENSEARCH_BUNDLE_MANIFEST,
                                  "--stack", "test-stack", "--config", PERF_TEST_CONFIG, "--force-insecure-mode"])
    @patch("run_perf_test.PerfTestCluster.create")
    @patch("run_perf_test.PerfTestSuite")
    @patch("run_perf_test.WorkingDirectory")
    @patch("run_perf_test.TemporaryDirectory")
    @patch("run_perf_test.GitRepository")
    def test_with_security_execute_perf_test(self, mock_git, mock_temp, mock_working_dir, mock_suite, mock_cluster, *mocks):
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_create = Mock()
        mock_create.__enter__ = Mock(return_value=('test-endpoint', 1234))
        mock_create.__exit__ = Mock(return_value=None)
        mock_cluster.return_value = mock_create

        mock_execute = Mock()
        mock_suite.return_value.execute = mock_execute

        main()
        self.assertEqual(1, mock_cluster.call_count)
        self.assertEqual(1, mock_suite.call_count)
        self.assertEqual(1, mock_git.call_count)
        self.assertEqual(1, mock_execute.call_count)
        self.assertEqual([], mock_execute.call_args)
        self.assertIn(False, mock_suite.call_args[0])
