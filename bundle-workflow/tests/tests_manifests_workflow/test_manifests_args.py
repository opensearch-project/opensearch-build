# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import unittest
from unittest.mock import patch

from manifests_workflow.manifests_args import ManifestsArgs


class TestManifestsArgs(unittest.TestCase):

    MANIFESTS_PY = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "../../src/manifests.py")
    )

    @patch("argparse._sys.argv", [MANIFESTS_PY, "list"])
    def test_action_list(self):
        self.assertEqual(ManifestsArgs().action, "list")

    @patch("argparse._sys.argv", [MANIFESTS_PY, "update"])
    def test_action_update(self):
        self.assertEqual(ManifestsArgs().action, "update")

    @patch("argparse._sys.argv", [MANIFESTS_PY, "invalid"])
    def test_action_invalid(self):
        with self.assertRaises(SystemExit):
            self.assertEqual(ManifestsArgs().action, "invalid")

    @patch("argparse._sys.argv", [MANIFESTS_PY, "list", "--verbose"])
    def test_verbose_true(self):
        self.assertTrue(ManifestsArgs().logging_level, logging.DEBUG)
