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

from run_checkout import main


class TestRunChecout(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capfd(self, capfd):
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_checkout.py", "--help"])
    def test_usage(self):
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__), "../../manifests/1.1.0/opensearch-1.1.0.yml"
        )
    )

    @patch("argparse._sys.argv", ["run_checkout.py", OPENSEARCH_MANIFEST])
    @patch(
        "run_checkout.GitRepository", return_value=MagicMock(working_directory="dummy")
    )
    @patch("run_checkout.TemporaryDirectory")
    def test_main(self, mock_temp, mock_repo):
        mock_temp.return_value.__enter__.return_value = tempfile.gettempdir()

        main()

        # each repository is checked out locally
        mock_repo.assert_has_calls(
            [
                call(
                    "https://github.com/opensearch-project/OpenSearch.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "OpenSearch"),
                    None,
                ),
                call(
                    "https://github.com/opensearch-project/common-utils.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "common-utils"),
                    None,
                ),
                call(
                    "https://github.com/opensearch-project/dashboards-reports.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "dashboards-reports"),
                    "reports-scheduler",
                ),
            ],
            any_order=True,
        )

        self.assertEqual(mock_repo.call_count, 14)
