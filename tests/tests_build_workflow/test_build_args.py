# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import unittest
from unittest.mock import patch

from build_workflow.build_args import BuildArgs


class TestBuildArgs(unittest.TestCase):

    BUILD_PY = "./src/run_build.py"

    BUILD_SH = "./build.sh"

    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "manifests",
            "templates",
            "opensearch",
            "1.x",
            "os-template-1.1.0.yml",
        )
    )

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_manifest(self) -> None:
        self.assertEqual(BuildArgs().manifest.name, TestBuildArgs.OPENSEARCH_MANIFEST)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_keep_default(self) -> None:
        self.assertFalse(BuildArgs().keep)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--keep"])
    def test_keep_true(self) -> None:
        self.assertTrue(BuildArgs().keep)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_snapshot_default(self) -> None:
        self.assertFalse(BuildArgs().snapshot)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--snapshot"])
    def test_snapshot_true(self) -> None:
        self.assertTrue(BuildArgs().snapshot)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_verbose_default(self) -> None:
        self.assertEqual(BuildArgs().logging_level, logging.INFO)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--verbose"])
    def test_verbose_true(self) -> None:
        self.assertTrue(BuildArgs().logging_level, logging.DEBUG)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_component_default(self) -> None:
        self.assertIsNone(BuildArgs().components)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--component", "xyz"])
    def test_component(self) -> None:
        self.assertEqual(BuildArgs().components, ["xyz"])

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--component", "foo", "bar"])
    def test_components(self) -> None:
        self.assertEqual(BuildArgs().components, ["foo", "bar"])

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_platform_default(self) -> None:
        self.assertIsNone(BuildArgs().platform)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--platform", "linux"])
    def test_platform(self) -> None:
        self.assertEqual(BuildArgs().platform, "linux")

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_architecture_default(self) -> None:
        self.assertIsNone(BuildArgs().architecture)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--architecture", "arm64"])
    def test_architecture(self) -> None:
        self.assertEqual(BuildArgs().architecture, "arm64")

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_distribution_default(self) -> None:
        self.assertEqual(BuildArgs().distribution, "tar")

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--distribution", "rpm"])
    def test_distribution(self) -> None:
        self.assertEqual(BuildArgs().distribution, "rpm")

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--component", "xyz"])
    def test_script_path(self) -> None:
        self.assertEqual(BuildArgs().script_path, self.BUILD_SH)

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_component_command(self) -> None:
        self.assertEqual(
            BuildArgs().component_command("component"),
            f"{self.BUILD_SH} {self.OPENSEARCH_MANIFEST} --component component",
        )

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--snapshot"])
    def test_component_command_with_snapshot(self) -> None:
        self.assertEqual(
            BuildArgs().component_command("component"),
            f"{self.BUILD_SH} {self.OPENSEARCH_MANIFEST} --component component --snapshot",
        )

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST, "--lock"])
    def test_manifest_lock(self) -> None:
        self.assertEqual(BuildArgs().ref_manifest, TestBuildArgs.OPENSEARCH_MANIFEST + ".lock")

    @patch("argparse._sys.argv", [BUILD_PY, OPENSEARCH_MANIFEST])
    def test_manifest_no_lock(self) -> None:
        self.assertIsNone(BuildArgs().ref_manifest)
