# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from manifests.input_manifest import InputManifest
from manifests_workflow.input_manifests import InputManifests


class TestInputManifests(unittest.TestCase):
    def test_manifests_path(self) -> None:
        path = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "manifests"))
        self.assertEqual(path, InputManifests.manifests_path())

    def test_workflows_path(self) -> None:
        path = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".github", "workflows"))
        self.assertEqual(path, InputManifests.workflows_path())

    def test_legacy_manifests_path(self) -> None:
        path = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "legacy-manifests"))
        self.assertEqual(path, InputManifests.legacy_manifests_path())

    def test_files(self) -> None:
        files = InputManifests.files("invalid")
        self.assertEqual(len(files), 0)

    def test_files_opensearch(self) -> None:
        files = InputManifests.files("opensearch")
        self.assertTrue(os.path.join(InputManifests.manifests_path(), os.path.join("3.0.0", "opensearch-3.0.0.yml")) in files)
        self.assertTrue(os.path.join(InputManifests.legacy_manifests_path(), os.path.join("1.2.1", "opensearch-1.2.1.yml")) in files)

    def test_files_opensearch_dashboards(self) -> None:
        files = InputManifests.files("opensearch-dashboards")
        self.assertTrue(os.path.join(InputManifests.manifests_path(), os.path.join("3.0.0", "opensearch-dashboards-3.0.0.yml")) in files)
        self.assertTrue(os.path.join(InputManifests.legacy_manifests_path(), os.path.join("1.2.1", "opensearch-dashboards-1.2.1.yml")) in files)

    def test_create_manifest_opensearch_template(self) -> None:
        input_manifests = InputManifests("OpenSearch")
        input_manifest = input_manifests.create_manifest("1.2.3", "1.x", [])
        self.assertEqual(
            input_manifest.to_dict(),
            {
                "schema-version": "1.0",
                "build": {"name": "OpenSearch", "version": "1.2.3"},
                "ci": {"image": {"name": "opensearchstaging/ci-runner:ci-runner-centos7-opensearch-build-v3",
                                 "args": "-e JAVA_HOME=/opt/java/openjdk-11"}},
                "components": [{"name": "OpenSearch",
                                "repository": "https://github.com/opensearch-project/OpenSearch.git",
                                "ref": "1.x",
                                "checks": ["gradle:publish", "gradle:properties:version"]}]
            }
        )

    def test_create_manifest_opensearch_default_template(self) -> None:
        input_manifests = InputManifests("OpenSearch")
        input_manifest = input_manifests.create_manifest("0.2.3", "0.x", [])
        self.assertEqual(
            input_manifest.to_dict(),
            {
                "schema-version": "1.1",
                "build": {"name": "OpenSearch", "version": "0.2.3"},
                "ci": {"image": {"name": "opensearchstaging/ci-runner:ci-runner-centos7-opensearch-build-v3",
                       "args": "-e JAVA_HOME=/opt/java/openjdk-21"}},
                "components": [{"name": "OpenSearch",
                                "repository": "https://github.com/opensearch-project/OpenSearch.git",
                                "ref": "0.x",
                                "checks": ["gradle:publish", "gradle:properties:version"]}]
            }
        )

    def test_create_manifest_opensearch_previous_base_version(self) -> None:
        input_manifests = InputManifests("OpenSearch")
        input_manifest = input_manifests.create_manifest("2.12.1000", "2.12", ["0.9.2", "1.3.1", "1.3.14", "2.12.0", "2.14.0", "3.0.0"])  # based on 2.12.0
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-2.12.1000.yml")
        input_manifest_compare = InputManifest.from_file(open(manifest_path))
        self.assertEqual(input_manifest.to_dict(), input_manifest_compare.to_dict())

    def test_create_manifest_opensearch_dashboards_template(self) -> None:
        input_manifests = InputManifests("OpenSearch Dashboards")
        input_manifest = input_manifests.create_manifest("1.2.3", "1.x", [])
        self.assertEqual(
            input_manifest.to_dict(),
            {
                "schema-version": "1.0",
                "build": {"name": "OpenSearch Dashboards", "version": "1.2.3"},
                "ci": {"image": {"name": "opensearchstaging/ci-runner:ci-runner-centos7-opensearch-dashboards-build-v4"}},
                "components": [{"name": "OpenSearch-Dashboards",
                                "repository": "https://github.com/opensearch-project/OpenSearch-Dashboards.git",
                                "ref": "1.x"}]
            }
        )

    def test_create_manifest_opensearch_dashboards_default_template(self) -> None:
        input_manifests = InputManifests("OpenSearch Dashboards")
        input_manifest = input_manifests.create_manifest("4.2.3", "4.x", [])
        self.assertEqual(
            input_manifest.to_dict(),
            {
                "schema-version": "1.1",
                "build": {"name": "OpenSearch Dashboards", "version": "4.2.3"},
                "ci": {"image": {"name": "opensearchstaging/ci-runner:ci-runner-almalinux8-opensearch-dashboards-build-v1"}},
                "components": [{"name": "OpenSearch-Dashboards",
                                "repository": "https://github.com/opensearch-project/OpenSearch-Dashboards.git",
                                "ref": "4.x",
                                "checks": ["npm:package:version"]}]
            }
        )

    def test_create_manifest_opensearch_dashboards_previous_base_version(self) -> None:
        input_manifests = InputManifests("OpenSearch-Dashboards")
        input_manifest = input_manifests.create_manifest("2.12.1000", "2.12", ["0.9.2", "1.3.1", "1.3.14", "2.12.0", "2.14.0", "3.0.0"])  # based on 2.12.0
        manifest_path = os.path.join(os.path.dirname(__file__), "data", "opensearch-dashboards-2.12.1000.yml")
        input_manifest_compare = InputManifest.from_file(open(manifest_path))
        self.assertEqual(input_manifest.to_dict(), input_manifest_compare.to_dict())

    @patch("os.makedirs")
    @patch("manifests_workflow.input_manifests.InputManifests.create_manifest")
    def test_write_manifest(self, mock_create_manifest: MagicMock, mock_makedirs: MagicMock) -> None:
        input_manifests = InputManifests("opensearch")
        input_manifests.write_manifest('0.1.2', '0.x', [])
        mock_create_manifest.assert_called_with('0.1.2', '0.x', [])
        mock_makedirs.assert_called_with(os.path.join(InputManifests.manifests_path(), '0.1.2'), exist_ok=True)
        mock_create_manifest.return_value.to_file.assert_called_with(
            os.path.join(InputManifests.manifests_path(), '0.1.2', 'opensearch-0.1.2.yml')
        )

    def test_jenkins_path(self) -> None:
        self.assertEqual(
            InputManifests.jenkins_path(),
            os.path.realpath(
                os.path.join(
                    os.path.dirname(__file__), "..", "..", "jenkins"
                )
            )
        )

    def test_cron_jenkinsfile(self) -> None:
        self.assertEqual(
            InputManifests.cron_jenkinsfile(),
            os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "jenkins", "check-for-build.jenkinsfile"))
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_add_to_cron(self, mock_open: MagicMock) -> None:
        mock_open().read.return_value = "parameterizedCron '''\n"
        input_manifests = InputManifests("test")
        input_manifests.add_to_cron('0.1.2')
        mock_open.assert_has_calls([call(InputManifests.cron_jenkinsfile(), 'w')])
        mock_open.assert_has_calls([call(InputManifests.cron_jenkinsfile(), 'r')])
        mock_open().write.assert_called_once_with(
            "parameterizedCron '''\n            H 1 * * * %INPUT_MANIFEST=0.1.2/test-0.1.2.yml;"
            "TARGET_JOB_NAME=distribution-build-test;BUILD_PLATFORM=linux;BUILD_DISTRIBUTION=tar;"
            "TEST_MANIFEST=0.1.2/test-0.1.2-test.yml;TEST_PLATFORM=linux;TEST_DISTRIBUTION=tar\n"
        )

    def test_os_versionincrement_workflow(self) -> None:
        self.assertEqual(
            InputManifests.os_versionincrement_workflow(),
            os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".github", "workflows", "os-increment-plugin-versions.yml"))
        )
        self.assertTrue(os.path.exists(InputManifests.os_versionincrement_workflow()))

    def test_osd_versionincrement_workflow(self) -> None:
        self.assertEqual(
            InputManifests.osd_versionincrement_workflow(),
            os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".github", "workflows", "osd-increment-plugin-versions.yml"))
        )
        self.assertTrue(os.path.exists(InputManifests.osd_versionincrement_workflow()))

    @patch("manifests_workflow.input_manifests.InputManifests.add_to_versionincrement_workflow")
    def test_add_to_versionincrement_workflow(self, mock_add_to_versionincrement_workflow: MagicMock) -> None:
        input_manifests = InputManifests("test")
        input_manifests.add_to_versionincrement_workflow('1.0.0')
        mock_add_to_versionincrement_workflow.assert_called_with("1.0.0")

    def test_create_manifest_with_components(self) -> None:
        pass
