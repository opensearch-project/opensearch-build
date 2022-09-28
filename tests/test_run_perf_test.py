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

import pytest

from run_perf_test import main


class TestRunPerfTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_perf_test.py", "--help"])
    def test_usage(self) -> None:
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
    @patch("run_perf_test.PerfTestRunners.from_args")
    def test_default_execute_perf_test(self, mock_runner: Mock, *mocks: Any) -> None:
        main()
        self.assertEqual(1, mock_runner.call_count)
