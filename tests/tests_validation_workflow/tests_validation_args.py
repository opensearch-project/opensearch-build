# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import unittest
from unittest.mock import patch

from validation_workflow.validation_args import ValidationArgs


class TestValidationArgs(unittest.TestCase):

    VALIDATION_PY = "./src/run_validation.py" \


    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "2.3.0"])
    def test_version(self) -> None:
        self.assertTrue(ValidationArgs().version)
        self.assertEqual(ValidationArgs().version, "2.3.0")
        self.assertNotEqual(ValidationArgs().version, "2.1.0")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "2.1.0", "--distribution", "rpm"])
    def test_distribution(self) -> None:
        self.assertEqual(ValidationArgs().distribution, "rpm")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "1.3.6", "--platform", "linux"])
    def test_platform_default(self) -> None:
        self.assertEqual(ValidationArgs().platform, "linux")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "1.3.0"])
    def test_verbose_default(self) -> None:
        self.assertEqual(ValidationArgs().logging_level, logging.INFO)

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "1.3.0", "--verbose"])
    def test_verbose_true(self) -> None:
        self.assertTrue(ValidationArgs().logging_level, logging.DEBUG)
