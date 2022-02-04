# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, mock_open, patch

from manifests_workflow.input_manifests import InputManifests


class TestInputManifests(unittest.TestCase):
    def test_manifests_path(self) -> None:
        path = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "manifests"))
        self.assertEqual(path, InputManifests.manifests_path())

    def test_create_manifest(self) -> None:
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

    @patch("os.makedirs")
    @patch("manifests_workflow.input_manifests.InputManifests.create_manifest")
    def test_write_manifest(self, mock_create_manifest: MagicMock, mock_makedirs: MagicMock) -> None:
        input_manifests = InputManifests("test")
        input_manifests.write_manifest('0.1.2', [])
        mock_create_manifest.assert_called_with('0.1.2', [])
        mock_makedirs.assert_called_with(os.path.join(InputManifests.manifests_path(), '0.1.2'), exist_ok=True)
        mock_create_manifest.return_value.to_file.assert_called_with(
            os.path.join(InputManifests.manifests_path(), '0.1.2', 'test-0.1.2.yml')
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
            f"parameterizedCron '''\n{' ' * 12}H/10 * * * * %INPUT_MANIFEST=0.1.2/test-0.1.2.yml;TARGET_JOB_NAME=distribution-build-test\n"
        )

    def test_create_manifest_with_components(self) -> None:
        pass
