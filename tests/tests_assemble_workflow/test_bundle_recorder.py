# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

import yaml

from assemble_workflow.bundle_file_location import BundleFileLocation
from assemble_workflow.bundle_recorder import BundleRecorder
from assemble_workflow.bundle_url_location import BundleUrlLocation
from manifests.build_manifest import BuildComponent, BuildManifest
from manifests.bundle_manifest import BundleManifest
from system.temporary_directory import TemporaryDirectory


class TestBundleRecorder(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-linux-1.1.0.yml")
        self.manifest = BuildManifest.from_path(manifest_path)
        self.bundle_recorder = BundleRecorder(self.manifest.build, "output_dir", "artifacts_dir", BundleFileLocation("bundle_output_dir", "opensearch", "tar"))

        manifest_distribution_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-build-windows-1.3.0.yml")
        self.manifest_distribution = BuildManifest.from_path(manifest_distribution_path)
        self.bundle_recorder_distribution = BundleRecorder(self.manifest_distribution.build, "output_dir", "artifacts_dir", BundleFileLocation("bundle_output_dir", "opensearch", "tar"))

    def test_record_component(self) -> None:
        component = BuildComponent(
            {
                "name": "job_scheduler",
                "repository": "https://github.com/opensearch-project/job_scheduler",
                "ref": "main",
                "commit_id": "3913d7097934cbfe1fdcf919347f22a597d00b76",
                "artifacts": [],
                "version": "1.0",
            }
        )
        self.bundle_recorder.record_component(component, "plugins")

        self.assertEqual(
            self.bundle_recorder.get_manifest().to_dict(),
            {
                "build": {
                    "platform": "linux",
                    "architecture": "x64",
                    "distribution": "tar",
                    "id": "c3ff7a232d25403fa8cc14c97799c323",
                    "location": os.path.join("bundle_output_dir", "tar", "dist", "opensearch", "opensearch-1.1.0-linux-x64.tar.gz"),
                    "name": "OpenSearch",
                    "version": "1.1.0",
                },
                "components": [
                    {
                        "commit_id": "3913d7097934cbfe1fdcf919347f22a597d00b76",
                        "location": os.path.join("bundle_output_dir", "tar", "builds", "opensearch", "plugins"),
                        "name": component.name,
                        "ref": "main",
                        "repository": "https://github.com/opensearch-project/job_scheduler",
                    }
                ],
                "schema-version": "1.1",
            },
        )

    def test_get_manifest(self) -> None:
        manifest = self.bundle_recorder.get_manifest()
        self.assertIs(type(manifest), BundleManifest)
        self.assertEqual(
            manifest.to_dict(),
            {
                "build": {
                    "platform": "linux",
                    "architecture": "x64",
                    "distribution": "tar",
                    "id": "c3ff7a232d25403fa8cc14c97799c323",
                    "location": os.path.join("bundle_output_dir", "tar", "dist", "opensearch", "opensearch-1.1.0-linux-x64.tar.gz"),
                    "name": "OpenSearch",
                    "version": "1.1.0",
                },
                "schema-version": "1.1",
            },
        )

    def test_get_manifest_distribution(self) -> None:
        manifest = self.bundle_recorder_distribution.get_manifest()
        self.assertIs(type(manifest), BundleManifest)
        self.assertEqual(
            manifest.to_dict(),
            {
                "build": {
                    "platform": "windows",
                    "architecture": "x64",
                    "distribution": "zip",
                    "id": "c3ff7a232d25403fa8cc14c97799c323",
                    "location": os.path.join("bundle_output_dir", "tar", "dist", "opensearch", "opensearch-1.3.0-windows-x64.zip"),
                    "name": "OpenSearch",
                    "version": "1.3.0",
                },
                "schema-version": "1.1",
            },
        )

    def test_write_manifest(self) -> None:
        with TemporaryDirectory() as dest_dir:
            self.bundle_recorder.write_manifest(dest_dir.name)
            manifest_path = os.path.join(dest_dir.name, "manifest.yml")
            self.assertTrue(os.path.isfile(manifest_path))
            data = self.bundle_recorder.get_manifest().to_dict()
            with open(manifest_path) as f:
                self.assertEqual(yaml.safe_load(f), data)

    def test_record_component_public(self) -> None:
        self.bundle_recorder = BundleRecorder(
            self.manifest.build,
            "output_dir",
            "artifacts_dir",
            BundleUrlLocation(
                "https://ci.opensearch.org/ci/ci-env-prod/job-name-opensearch/1.2.0/build-123/platform-mac/arch-amd64/",
                "opensearch",
                "tar"
            )
        )

        component = BuildComponent(
            {
                "name": "job_scheduler",
                "repository": "https://github.com/opensearch-project/job_scheduler",
                "ref": "main",
                "commit_id": "3913d7097934cbfe1fdcf919347f22a597d00b76",
                "artifacts": [],
                "version": "1.0",
            }
        )

        self.bundle_recorder.record_component(component, "plugins")

        self.assertEqual(
            self.bundle_recorder.get_manifest().to_dict(),
            {
                "build": {
                    "platform": "linux",
                    "architecture": "x64",
                    "distribution": "tar",
                    "id": "c3ff7a232d25403fa8cc14c97799c323",
                    "location": ("https://ci.opensearch.org/ci/ci-env-prod/job-name-opensearch/1.2.0/build-123/platform-mac/arch-amd64/tar/"
                                 "dist/opensearch/opensearch-1.1.0-linux-x64.tar.gz"),
                    "name": "OpenSearch",
                    "version": "1.1.0",
                },
                "components": [
                    {
                        "commit_id": "3913d7097934cbfe1fdcf919347f22a597d00b76",
                        "location":
                            "https://ci.opensearch.org/ci/ci-env-prod/job-name-opensearch/1.2.0/build-123/platform-mac/arch-amd64/tar/builds/opensearch/plugins",
                        "name": component.name,
                        "ref": "main",
                        "repository": "https://github.com/opensearch-project/job_scheduler",
                    }
                ],
                "schema-version": "1.1",
            },
        )

    def test_package_name(self) -> None:
        self.assertEqual(self.bundle_recorder.package_name, "opensearch-1.1.0-linux-x64.tar.gz")


class TestBundleRecorderDashboards(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-dashboards-build-1.1.0.yml")
        self.manifest = BuildManifest.from_path(manifest_path)
        self.bundle_recorder = BundleRecorder(
            self.manifest.build,
            "output_dir",
            "artifacts_dir",
            BundleFileLocation("bundle_output_dir", "opensearch-dashboards", "tar")
        )

        manifest_distribution_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-dashboards-build-windows-1.3.0.yml")
        self.manifest_distribution = BuildManifest.from_path(manifest_distribution_path)
        self.bundle_recorder_distribution = BundleRecorder(
            self.manifest_distribution.build,
            "output_dir",
            "artifacts_dir",
            BundleFileLocation("bundle_output_dir", "opensearch-dashboards", "tar")
        )

    def test_record_component(self) -> None:
        component = BuildComponent(
            {
                "name": "alertingDashboards",
                "repository": "https://github.com/opensearch-project/alerting-dashboards-plugin",
                "ref": "main",
                "commit_id": "ae789280740d7000d1f13245019414abeedfc286",
                "artifacts": [],
                "version": "1.0",
            }
        )
        self.bundle_recorder.record_component(component, "plugins")

        self.assertEqual(
            self.bundle_recorder.get_manifest().to_dict(),
            {
                "build": {
                    "platform": "linux",
                    "architecture": "x64",
                    "distribution": "tar",
                    "id": "c94ebec444a94ada86a230c9297b1d73",
                    "location": os.path.join("bundle_output_dir", "tar", "dist", "opensearch-dashboards", "opensearch-dashboards-1.1.0-linux-x64.tar.gz"),
                    "name": "OpenSearch Dashboards",
                    "version": "1.1.0",
                },
                "components": [
                    {
                        "commit_id": "ae789280740d7000d1f13245019414abeedfc286",
                        "location": os.path.join("bundle_output_dir", "tar", "builds", "opensearch-dashboards", "plugins"),
                        "name": component.name,
                        "ref": "main",
                        "repository": "https://github.com/opensearch-project/alerting-dashboards-plugin",
                    }
                ],
                "schema-version": "1.1",
            },
        )

    def test_get_manifest(self) -> None:
        manifest = self.bundle_recorder.get_manifest()
        self.assertIs(type(manifest), BundleManifest)
        self.assertEqual(
            manifest.to_dict(),
            {
                "build": {
                    "platform": "linux",
                    "architecture": "x64",
                    "distribution": "tar",
                    "id": "c94ebec444a94ada86a230c9297b1d73",
                    "location": os.path.join("bundle_output_dir", "tar", "dist", "opensearch-dashboards", "opensearch-dashboards-1.1.0-linux-x64.tar.gz"),
                    "name": "OpenSearch Dashboards",
                    "version": "1.1.0",
                },
                "schema-version": "1.1",
            },
        )

    def test_get_manifest_distribution(self) -> None:
        manifest = self.bundle_recorder_distribution.get_manifest()
        self.assertIs(type(manifest), BundleManifest)
        self.assertEqual(
            manifest.to_dict(),
            {
                "build": {
                    "platform": "windows",
                    "architecture": "x64",
                    "distribution": "zip",
                    "id": "c94ebec444a94ada86a230c9297b1d73",
                    "location": os.path.join("bundle_output_dir", "tar", "dist", "opensearch-dashboards", "opensearch-dashboards-1.3.0-windows-x64.zip"),
                    "name": "OpenSearch Dashboards",
                    "version": "1.3.0",
                },
                "schema-version": "1.1",
            },
        )

    def test_write_manifest(self) -> None:
        with TemporaryDirectory() as dest_dir:
            self.bundle_recorder.write_manifest(dest_dir.name)
            manifest_path = os.path.join(dest_dir.name, "manifest.yml")
            self.assertTrue(os.path.isfile(manifest_path))
            data = self.bundle_recorder.get_manifest().to_dict()
            with open(manifest_path) as f:
                self.assertEqual(yaml.safe_load(f), data)

    def test_record_component_public(self) -> None:
        self.bundle_recorder = BundleRecorder(
            self.manifest.build,
            "output_dir",
            "artifacts_dir",
            BundleUrlLocation(
                "https://ci.opensearch.org/ci/ci-env-prod/job-name-dashboards/1.2.0/build-123/platform-mac/arch-amd64/",
                "opensearch-dashboards",
                "tar"
            )
        )

        component = BuildComponent(
            {
                "name": "alertingDashboards",
                "repository": "https://github.com/opensearch-project/alerting-dashboards-plugin",
                "ref": "main",
                "commit_id": "ae789280740d7000d1f13245019414abeedfc286",
                "artifacts": [],
                "version": "1.0",
            }
        )
        self.bundle_recorder.record_component(component, "plugins")

        self.assertEqual(
            self.bundle_recorder.get_manifest().to_dict(),
            {
                "build": {
                    "platform": "linux",
                    "architecture": "x64",
                    "distribution": "tar",
                    "id": "c94ebec444a94ada86a230c9297b1d73",
                    "location": ("https://ci.opensearch.org/ci/ci-env-prod/job-name-dashboards/1.2.0/build-123/platform-mac/arch-amd64/tar/"
                                 "dist/opensearch-dashboards/opensearch-dashboards-1.1.0-linux-x64.tar.gz"),
                    "name": "OpenSearch Dashboards",
                    "version": "1.1.0",
                },
                "components": [
                    {
                        "commit_id": "ae789280740d7000d1f13245019414abeedfc286",
                        "location":
                            ("https://ci.opensearch.org/ci/ci-env-prod/job-name-dashboards/1.2.0/build-123/platform-mac/arch-amd64/tar/"
                             "builds/opensearch-dashboards/plugins"),
                        "name": component.name,
                        "ref": "main",
                        "repository": "https://github.com/opensearch-project/alerting-dashboards-plugin",
                    }
                ],
                "schema-version": "1.1",
            },
        )

    def test_package_name(self) -> None:
        self.assertEqual(
            self.bundle_recorder.package_name,
            "opensearch-dashboards-1.1.0-linux-x64.tar.gz",
        )
