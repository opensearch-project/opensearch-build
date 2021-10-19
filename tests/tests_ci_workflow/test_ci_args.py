# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import patch

from ci_workflow.ci_args import CiArgs


class TestCiArgs(unittest.TestCase):

    CI_PY = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "run_ci.py"))

    CI_SH = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "ci.sh"))

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "manifests",
            "1.1.0",
            "opensearch-1.1.0.yml",
        )
    )

    @patch("argparse._sys.argv", [CI_PY, OPENSEARCH_MANIFEST])
    def test_manifest(self):
        self.assertEqual(CiArgs().manifest.name, TestCiArgs.OPENSEARCH_MANIFEST)

    @patch("argparse._sys.argv", [CI_PY, OPENSEARCH_MANIFEST])
    def test_keep_default(self):
        self.assertFalse(CiArgs().keep)

    @patch("argparse._sys.argv", [CI_PY, OPENSEARCH_MANIFEST, "--keep"])
    def test_keep_true(self):
        self.assertTrue(CiArgs().keep)

    @patch("argparse._sys.argv", [CI_PY, OPENSEARCH_MANIFEST])
    def test_snapshot_default(self):
        self.assertFalse(CiArgs().snapshot)

    @patch("argparse._sys.argv", [CI_PY, OPENSEARCH_MANIFEST, "--snapshot"])
    def test_snapshot_true(self):
        self.assertTrue(CiArgs().snapshot)

    @patch("argparse._sys.argv", [CI_PY, OPENSEARCH_MANIFEST])
    def test_component_default(self):
        self.assertIsNone(CiArgs().component)

    @patch("argparse._sys.argv", [CI_PY, OPENSEARCH_MANIFEST, "--component", "xyz"])
    def test_component(self):
        self.assertEqual(CiArgs().component, "xyz")

    @patch("argparse._sys.argv", [CI_PY, OPENSEARCH_MANIFEST, "--component", "xyz"])
    def test_script_path(self):
        self.assertTrue(os.path.isfile(self.CI_PY))
        self.assertTrue(os.path.isfile(self.CI_SH))
        self.assertEqual(CiArgs().script_path, self.CI_SH)

    @patch("argparse._sys.argv", [CI_PY, OPENSEARCH_MANIFEST])
    def test_component_command(self):
        self.assertEqual(
            CiArgs().component_command("component"),
            f"{self.CI_SH} {self.OPENSEARCH_MANIFEST} --component component",
        )

    @patch("argparse._sys.argv", [CI_PY, OPENSEARCH_MANIFEST, "--snapshot"])
    def test_component_command_with_snapshot(self):
        self.assertEqual(
            CiArgs().component_command("component"),
            f"{self.CI_SH} {self.OPENSEARCH_MANIFEST} --component component --snapshot",
        )
