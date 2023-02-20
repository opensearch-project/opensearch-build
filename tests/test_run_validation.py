# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import unittest
from typing import Any
from unittest.mock import Mock, patch

import pytest
from pytest import CaptureFixture

from src.run_validation import main
from src.validation_workflow.validation_args import ValidationArgs


class TestRunValidation(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def getCapfd(self, capfd: CaptureFixture) -> None:
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_validation.py", "--help"])
    def test_usage(self, *mocks: Any) -> None:
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    @patch("argparse._sys.argv", ["run_validation.py", "--version", "1.3.6"])
    @patch("src.validation_workflow.validation_tar.ValidationTar.download_artifacts", return_value=True)
    @patch("run_validation.main", return_value=0)
    def test_main_default(self, mock_tar: Mock, *mocks: Any) -> None:
        self.assertEqual(ValidationArgs().version, "1.3.6")
        self.assertEqual(ValidationArgs().distribution, "tar")
        self.assertNotEqual(ValidationArgs().distribution, "rpm")

    @patch("argparse._sys.argv", ["run_validation.py", "--version", "2.1.0", "--distribution", "rpm"])
    @patch("src.validation_workflow.validation_rpm.ValidationRpm.download_artifacts", return_value=True)
    @patch("run_validation.main", return_value=0)
    def test_main_rpm(self, mock_tar: Mock, *mocks: Any) -> None:
        self.assertEqual(ValidationArgs().version, "2.1.0")
        self.assertEqual(ValidationArgs().distribution, "rpm")
        self.assertNotEqual(ValidationArgs().distribution, "tar")

    @patch("argparse._sys.argv", ["run_validation.py", "--version", "2.1.0", "--distribution", "yum"])
    @patch("src.validation_workflow.validation_yum.ValidationYum.download_artifacts", return_value=True)
    @patch("run_validation.main", return_value=0)
    def test_main_yum(self, mock_tar: Mock, *mocks: Any) -> None:
        self.assertEqual(ValidationArgs().version, "2.1.0")
        self.assertEqual(ValidationArgs().distribution, "yum")
        self.assertNotEqual(ValidationArgs().distribution, "tar")
