# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from typing import Any
from unittest.mock import MagicMock, call, mock_open, patch

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
        self.assertTrue(os.path.join(InputManifests.manifests_path(), os.path.join("1.3.0", "opensearch-1.3.0.yml")) in files)
        self.assertTrue(os.path.join(InputManifests.legacy_manifests_path(), os.path.join("1.2.1", "opensearch-1.2.1.yml")) in files)

    def test_files_opensearch_dashboards(self) -> None:
        files = InputManifests.files("opensearch-dashboards")
        self.assertTrue(os.path.join(InputManifests.manifests_path(), os.path.join("1.3.3", "opensearch-dashboards-1.3.3.yml")) in files)
        self.assertTrue(os.path.join(InputManifests.legacy_manifests_path(), os.path.join("1.2.1", "opensearch-dashboards-1.2.1.yml")) in files)

    def test_create_manifest_opensearch(self) -> None:
        input_manifests = InputManifests("OpenSearch")
        input_manifest = input_manifests.create_manifest("1.2.3", [])
        self.assertEqual(
            input_manifest.to_dict(),
            {
                "schema-version": "1.0",
                "build": {"name": "OpenSearch", "version": "1.2.3"},
                "ci": {"image": {"name": "opensearchstaging/ci-runner:ci-runner-centos7-opensearch-build-v2",
                                 "args": "-e JAVA_HOME=/opt/java/openjdk-11"}},
            },
        )

    def test_create_manifest_opensearch_from_default(self) -> None:
        input_manifests = InputManifests("OpenSearch")
        input_manifest = input_manifests.create_manifest("0.2.3", [])
        self.assertEqual(
            input_manifest.to_dict(),
            {
                "schema-version": "1.0",
                "build": {"name": "OpenSearch", "version": "0.2.3"},
                "ci": {"image": {"name": "opensearchstaging/ci-runner:ci-runner-centos7-opensearch-build-v2",
                                 "args": "-e JAVA_HOME=/opt/java/openjdk-17"}},
            },
        )

    def test_create_manifest_opensearch_dashboards(self) -> None:
        input_manifests = InputManifests("OpenSearch Dashboards")
        input_manifest = input_manifests.create_manifest("1.2.3", [])
        self.assertEqual(
            input_manifest.to_dict(),
            {
                "schema-version": "1.0",
                "build": {"name": "OpenSearch Dashboards", "version": "1.2.3"},
                "ci": {"image": {"name": "opensearchstaging/ci-runner:ci-runner-centos7-opensearch-dashboards-build-v2", }},
            },
        )

    def test_create_manifest_opensearch_dashboards_from_default(self) -> None:
        input_manifests = InputManifests("OpenSearch Dashboards")
        input_manifest = input_manifests.create_manifest("4.2.3", [])
        self.assertEqual(
            input_manifest.to_dict(),
            {
                "schema-version": "1.0",
                "build": {"name": "OpenSearch Dashboards", "version": "4.2.3"},
                "ci": {"image": {"name": "opensearchstaging/ci-runner:ci-runner-centos7-opensearch-dashboards-build-v2", }},
            },
        )

    @patch("os.makedirs")
    @patch("manifests_workflow.input_manifests.InputManifests.create_manifest")
    def test_write_manifest(self, mock_create_manifest: MagicMock, mock_makedirs: MagicMock) -> None:
        input_manifests = InputManifests("opensearch")
        input_manifests.write_manifest('0.1.2', [])
        mock_create_manifest.assert_called_with('0.1.2', [])
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
            f"parameterizedCron '''\n{' ' * 12}H 1 * * * %INPUT_MANIFEST=0.1.2/test-0.1.2.yml;TARGET_JOB_NAME=distribution-build-test\n"
        )

    def test_versionincrement_workflow(self) -> None:
        self.assertEqual(
            InputManifests.versionincrement_workflow(),
            os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".github", "workflows", "increment-plugin-versions.yml"))
        )

    @patch("builtins.open", new_callable=mock_open)
    @patch("manifests_workflow.input_manifests.InputManifests.add_to_versionincrement_workflow")
    def test_add_to_versionincrement_workflow(self, *mocks: Any) -> None:
        input_manifests = InputManifests("test")
        input_manifests.add_to_versionincrement_workflow('0.1.2')

    def test_create_manifest_with_components(self) -> None:
        pass
