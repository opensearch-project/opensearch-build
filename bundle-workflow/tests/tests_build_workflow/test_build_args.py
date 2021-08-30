# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import patch

from build_workflow.build_args import BuildArgs


class TestBuildArgs(unittest.TestCase):

    BUILD_PY = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "../../src/build.py")
    )

    BUILD_SH = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "../../build.sh")
    )

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__), "../../../manifests/opensearch-1.1.0.yml"
        )
    )

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_manifest(self):
        self.assertEqual(BuildArgs().manifest.name, TestBuildArgs.OPENSEARCH_MANIFEST)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_keep_default(self):
        self.assertFalse(BuildArgs().keep)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--keep"])
    def test_keep_true(self):
        self.assertTrue(BuildArgs().keep)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_snapshot_default(self):
        self.assertFalse(BuildArgs().snapshot)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--snapshot"])
    def test_snapshot_true(self):
        self.assertTrue(BuildArgs().snapshot)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_component_default(self):
        self.assertIsNone(BuildArgs().component)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--component", "xyz"])
    def test_component(self):
        self.assertEqual(BuildArgs().component, "xyz")

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--component", "xyz"])
    def test_script_path(self):
        self.assertTrue(os.path.isfile(self.BUILD_PY))
        self.assertTrue(os.path.isfile(self.BUILD_SH))
        self.assertEqual(BuildArgs().script_path, self.BUILD_SH)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_component_command(self):
        self.assertEqual(
            BuildArgs().component_command("component"),
            f"{self.BUILD_SH} {self.OPENSEARCH_MANIFEST} --component component",
        )

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--snapshot"])
    def test_component_command_with_snapshot(self):
        self.assertEqual(
            BuildArgs().component_command("component"),
            f"{self.BUILD_SH} {self.OPENSEARCH_MANIFEST} --component component --snapshot",
        )
