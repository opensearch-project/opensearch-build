# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from manifests.test_manifest import TestManifest


class TestTestManifest(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.manifest_filename = os.path.join(self.data_path, "opensearch-dashboards-test-1.3.0.yml")
        self.manifest = TestManifest.from_path(self.manifest_filename)

    def test_component(self) -> None:
        self.assertEqual(self.manifest.name, "OpenSearch Dashboards")
        self.assertEqual(self.manifest.ci.image.name, "opensearchstaging/ci-runner:ci-runner-rockylinux8-opensearch-dashboards-integtest-v1")
