# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

import yaml

from manifests.test_report_manifest import TestReportManifest


class TestTestReportManifest(unittest.TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.manifest_filename = os.path.join(self.data_path, "test-run.yml")
        self.manifest = TestReportManifest.from_path(self.manifest_filename)

    def test_test_run(self) -> None:
        self.assertEqual(self.manifest.name, "OpenSearch")
        test_run = self.manifest.test_run
        self.assertEqual(test_run.command, "./test.sh integ-test manifests/2.8.0/opensearch-2.8.0-test.yml "
                                           "--paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.8.0/7935/linux/x64/tar")
        self.assertEqual(test_run.test_type, "integ-test")
        self.assertEqual(test_run.test_manifest, "manifests/2.8.0/opensearch-2.8.0-test.yml")
        self.assertEqual(test_run.distribution_manifest, "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.8.0/7935/linux/x64/tar/dist/opensearch/manifest.yml")
        self.assertEqual(test_run.test_id, "5109")

    def test_component(self) -> None:
        component = self.manifest.components["alerting"]
        self.assertEqual(component.name, "alerting")
        self.assertEqual(component.command, "./test.sh integ-test manifests/2.8.0/opensearch-2.8.0-test.yml "
                                            "--paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.8.0/7935/linux/x64/tar --component alerting")
        self.assertEqual(component.configs.configs[0]["name"], "with-security")
        self.assertEqual(component.configs.configs[0]["status"], "FAIL")
        self.assertEqual(component.configs.configs[0]["yml"],
                         "https://ci.opensearch.org/ci/dbc/integ-test/2.8.0/7935/linux/x64/tar/test-results/5109/integ-test/alerting/with-security/alerting.yml")
        self.assertEqual(component.configs.configs[1]["name"], "without-security")
        self.assertEqual(component.configs.configs[1]["status"], "PASS")
        self.assertEqual(component.configs.configs[1]["yml"],
                         "https://ci.opensearch.org/ci/dbc/integ-test/2.8.0/7935/linux/x64/tar/test-results/5109/integ-test/alerting/without-security/alerting.yml")

    def test_to_dict(self) -> None:
        data = self.manifest.to_dict()
        with open(self.manifest_filename) as f:
            self.assertEqual(yaml.safe_load(f), data)
