# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import patch

from build_workflow.build_target import BuildTarget


class TestBuildTarget(unittest.TestCase):
    def test_output_dir(self):
        self.assertEqual(BuildTarget(version="1.1.0", architecture="x86").output_dir, "artifacts")

    def test_build_id_hex(self):
        self.assertEqual(len(BuildTarget(version="1.1.0", architecture="x86").build_id), 32)

    @patch.dict(os.environ, {"BUILD_NUMBER": "id"})
    def test_build_id_from_env(self):
        self.assertEqual(BuildTarget(version="1.1.0", architecture="x86").build_id, "id")

    def test_build_id_from_arg(self):
        self.assertEqual(BuildTarget(version="1.1.0", architecture="x86", build_id="id").build_id, "id")

    def test_opensearch_version(self):
        self.assertEqual(
            BuildTarget(version="1.1.0", architecture="x86", snapshot=False).opensearch_version,
            "1.1.0",
        )

    def test_compatible_opensearch_versions(self):
        self.assertEqual(
            BuildTarget(version="1.1.2", architecture="x86", patches=["1.1.0", "1.1.1"], snapshot=False).compatible_opensearch_versions,
            ['1.1.2', '1.1.0', '1.1.1', '1.1.0-SNAPSHOT', '1.1.1-SNAPSHOT'],
        )

    def test_compatible_opensearch_versions_snapshot(self):
        self.assertEqual(
            BuildTarget(version="1.1.2", architecture="x86", patches=["1.1.0", "1.1.1"], snapshot=True).compatible_opensearch_versions,
            ['1.1.2-SNAPSHOT', '1.1.0', '1.1.1', '1.1.0-SNAPSHOT', '1.1.1-SNAPSHOT'],
        )

    def test_opensearch_version_snapshot(self):
        self.assertEqual(
            BuildTarget(version="1.1.0", architecture="x86", snapshot=True).opensearch_version,
            "1.1.0-SNAPSHOT",
        )

    def test_component_version(self):
        self.assertEqual(
            BuildTarget(version="1.1.0", architecture="x86", snapshot=False).component_version,
            "1.1.0.0",
        )

    def test_compatible_component_versions(self):
        self.assertEqual(
            BuildTarget(version="1.1.2", architecture="x86", patches=["1.1.0", "1.1.1"], snapshot=False).compatible_component_versions,
            ['1.1.2.0', '1.1.0.0', '1.1.1.0', '1.1.0.0-SNAPSHOT', '1.1.1.0-SNAPSHOT'],
        )

    def test_compatible_component_versions_snapshot(self):
        self.assertEqual(
            BuildTarget(version="1.1.2", architecture="x86", patches=["1.1.0", "1.1.1"], snapshot=True).compatible_component_versions,
            ['1.1.2.0-SNAPSHOT', '1.1.0.0', '1.1.1.0', '1.1.0.0-SNAPSHOT', '1.1.1.0-SNAPSHOT'],
        )

    def test_component_version_snapshot(self):
        self.assertEqual(
            BuildTarget(version="1.1.0", architecture="x86", snapshot=True).component_version,
            "1.1.0.0-SNAPSHOT",
        )

    @patch("build_workflow.build_target.current_platform", return_value="value")
    def test_platform(self, *mock):
        self.assertEqual(BuildTarget(version="1.1.0", snapshot=False).platform, "value")

    def test_platform_value(self):
        self.assertEqual(BuildTarget(version="1.1.0", platform="value", snapshot=False).platform, "value")

    @patch("build_workflow.build_target.current_architecture", return_value="value")
    def test_arch(self, *mock):
        self.assertEqual(BuildTarget(version="1.1.0", snapshot=False).architecture, "value")

    def test_arch_value(self):
        self.assertEqual(BuildTarget(version="1.1.0", architecture="value", snapshot=False).architecture, "value")
