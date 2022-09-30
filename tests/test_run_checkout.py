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
from unittest.mock import MagicMock, Mock, call, patch

import pytest

from run_checkout import main


class TestRunCheckout(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_checkout.py", "--help"])
    def test_usage(self) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "manifests",
            "templates",
            "opensearch",
            "1.x",
            "os-template-1.1.0.yml"
        )
    )

    @patch("argparse._sys.argv", ["run_checkout.py", OPENSEARCH_MANIFEST])
    @patch("run_checkout.GitRepository")
    @patch("run_checkout.TemporaryDirectory")
    def test_main(self, mock_temp: Mock, mock_repo: Mock) -> None:
        mock_temp.return_value.__enter__.return_value.name = tempfile.gettempdir()
        mock_repo.return_value.__enter__.return_value = MagicMock(working_directory="dummy")

        main()

        # each repository is checked out locally
        mock_repo.assert_has_calls(
            [
                call(
                    "https://github.com/opensearch-project/OpenSearch.git",
                    "tags/1.1.0",
                    os.path.join(tempfile.gettempdir(), "OpenSearch"),
                    None,
                ),
                call(
                    "https://github.com/opensearch-project/common-utils.git",
                    "tags/1.1.0.0",
                    os.path.join(tempfile.gettempdir(), "common-utils"),
                    None,
                ),
                call(
                    "https://github.com/opensearch-project/dashboards-reports.git",
                    "tags/1.1.0.0",
                    os.path.join(tempfile.gettempdir(), "dashboards-reports"),
                    "reports-scheduler",
                ),
            ],
            any_order=True,
        )

        self.assertNotEqual(mock_repo.call_count, 0)
