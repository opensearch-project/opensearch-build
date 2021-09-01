# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from unittest.mock import MagicMock

import yaml

from assemble_workflow.bundle_recorder import BundleRecorder
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest


class TestBundleRecorder(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        with open(
            os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml")
        ) as f:
            manifest = BuildManifest.from_file(f)
            self.bundle_recorder = BundleRecorder(
                manifest.build, "output_dir", "artifacts_dir"
            )

    def test_record_component(self):
        component = MagicMock(
            name="job_scheduler",
            repository="https://github.com/opensearch-project/job_scheduler",
            ref="main",
            commit_id="3913d7097934cbfe1fdcf919347f22a597d00b76",
        )
        self.bundle_recorder.record_component(component, "plugins")

        self.assertEqual(
            self.bundle_recorder.get_manifest().to_dict(),
            {
                "build": {
                    "architecture": "x64",
                    "id": "f39b2d68f8b74389a0037f3e8d6ba0b0",
                    "location": "output_dir/opensearch-1.1.0-linux-x64.tar.gz",
                    "name": "OpenSearch",
                    "version": "1.1.0",
                },
                "components": [
                    {
                        "commit_id": "3913d7097934cbfe1fdcf919347f22a597d00b76",
                        "location": "artifacts_dir/plugins",
                        "name": component.name,
                        "ref": "main",
                        "repository": "https://github.com/opensearch-project/job_scheduler",
                    }
                ],
                "schema-version": "1.0",
            },
        )

    def test_get_manifest(self):
        manifest = self.bundle_recorder.get_manifest()
        self.assertIs(type(manifest), BundleManifest)
        self.assertEqual(
            manifest.to_dict(),
            {
                "build": {
                    "architecture": "x64",
                    "id": "f39b2d68f8b74389a0037f3e8d6ba0b0",
                    "location": "output_dir/opensearch-1.1.0-linux-x64.tar.gz",
                    "name": "OpenSearch",
                    "version": "1.1.0",
                },
                "components": [],
                "schema-version": "1.0",
            },
        )

    def test_write_manifest(self):
        with tempfile.TemporaryDirectory() as dest_dir:
            self.bundle_recorder.write_manifest(dest_dir)
            manifest_path = os.path.join(dest_dir, "manifest.yml")
            self.assertTrue(os.path.isfile(manifest_path))
            data = self.bundle_recorder.get_manifest().to_dict()
            with open(manifest_path) as f:
                self.assertEqual(yaml.safe_load(f), data)
