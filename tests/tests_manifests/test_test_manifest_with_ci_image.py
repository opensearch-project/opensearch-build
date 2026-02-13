# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from manifests.test.test_manifest_1_0 import TestManifest_1_0
from manifests.test_manifest import TestManifest


class TestTestManifest(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.manifest_filename_schema_1_0 = os.path.join(self.data_path, "opensearch-dashboards-test-1.3.0.yml")
        self.manifest_filename_schema_1_1 = os.path.join(self.data_path, "opensearch-dashboards-test-3.2.0.yml")
        self.manifest_schema_1_0 = TestManifest_1_0.from_path(self.manifest_filename_schema_1_0)
        self.manifest_schema_1_1 = TestManifest.from_path(self.manifest_filename_schema_1_1)

    def test_component_schema_1_0(self) -> None:
        self.assertEqual(self.manifest_schema_1_0.name, "OpenSearch Dashboards")
        self.assertEqual(self.manifest_schema_1_0.ci.image.name, "opensearchstaging/ci-runner:ci-runner-rockylinux8-opensearch-dashboards-integtest-v1")
        self.assertEqual(self.manifest_schema_1_0.ci.image.args, None)

    def test_component_schema_1_1(self) -> None:
        self.assertEqual(self.manifest_schema_1_1.name, "OpenSearch Dashboards")
        self.assertEqual(self.manifest_schema_1_1.ci.image["linux"]["tar"].name, "opensearchstaging/ci-runner:ci-runner-almalinux9-opensearch-dashboards-integtest-v1")
        self.assertEqual(self.manifest_schema_1_1.ci.image["linux"]["tar"].args, "-u 1000 --cpus 4 -m 16g -e BROWSER_PATH=electron")
