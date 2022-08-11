# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any
from unittest.mock import patch

import pytest

from run_releasenotes_check import main

gitLogDate = '2022-07-26'


class TestRunReleaseNotesCheck(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _capfd(self, capfd: Any) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_releasenotes_check.py", "--help"])
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
            "2.x",
            "manifest.yml"
        )
    )

    @patch("argparse._sys.argv", ["run_releasenotes_check.py", "check", OPENSEARCH_MANIFEST, "--date", gitLogDate])
    def test_main(self) -> None:
        assert main() == 0

    @patch("argparse._sys.argv", ["run_releasenotes_check.py", "check", OPENSEARCH_MANIFEST, "--date", gitLogDate, "--save"])
    def test_main_with_save(self) -> None:
        assert main() == 0
        assert os.path.exists("table.md") is True
