# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from manifests_workflow.input_manifests import InputManifests


class TestInputManifests(unittest.TestCase):
    def test_manifests_path(self):
        path = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "manifests"))
        self.assertEqual(path, InputManifests.manifests_path())

    def test_create_manifest(self):
        input_manifests = InputManifests("test")
        input_manifest = input_manifests.create_manifest("1.2.3", [])
        self.assertEqual(
            input_manifest.to_dict(),
            {
                "schema-version": "1.0",
                "build": {"name": "test", "version": "1.2.3"},
                "ci": {"image": {"name": "opensearchstaging/ci-runner:centos7-x64-arm64-jdkmulti-node10.24.1-cypress6.9.1-20211028"}},
            },
        )

    def test_create_manifest_with_components(self):
        pass
