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

from run_validation import main


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

    @patch("argparse._sys.argv", ["run_validation.py", "--version", "2.1.0", "--distribution", "tar"])
    @patch('run_validation.ValidationTestRunner')
    def test_main(self, mock_tar: Mock, *mocks: Any) -> None:

        result = main()
        self.assertTrue(result)
