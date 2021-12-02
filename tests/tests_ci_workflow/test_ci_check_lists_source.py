# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from ci_workflow.ci_check_list_source import CiCheckListSource
from manifests.input_manifest import InputManifest


class TestCiCheckListsSource(unittest.TestCase):
    @patch("ci_workflow.ci_check_list_source.GitRepository")
    def test_checkout(self, mock_git_repo):
        component = InputManifest.ComponentFromSource({
            "name": "common-utils",
            "repository": "url",
            "ref": "ref"
        })
        list = CiCheckListSource(component, MagicMock())
        list.checkout("path")
        mock_git_repo.assert_called()

    @patch("ci_workflow.ci_check_list_source.GitRepository")
    @patch("ci_workflow.ci_check_gradle_properties.PropertiesFile")
    def test_check(self, mock_properties_file, mock_check, *mocks):
        component = InputManifest.ComponentFromSource({
            "name": "common-utils",
            "repository": "url",
            "ref": "ref",
            "checks": ["gradle:properties:version"]
        })
        list = CiCheckListSource(component, MagicMock())
        list.checkout("path")
        list.check()
        # patching ci_workflow.ci_check_list_source.CiCheckGradlePropertiesVersion#check doesn't work
        # but it creates an instance of PropertiesFile
        mock_properties_file.assert_called()

    @patch("ci_workflow.ci_check_list_source.GitRepository")
    def test_invalid_check(self, *mocks):
        component = InputManifest.ComponentFromSource({
            "name": "common-utils",
            "repository": "url",
            "ref": "ref",
            "checks": ["invalid:check"]
        })
        list = CiCheckListSource(component, MagicMock())
        list.checkout("path")
        with self.assertRaises(CiCheckListSource.InvalidCheckError) as ctx:
            list.check()
        self.assertTrue(str(ctx.exception).startswith("Invalid check: invalid:check"))
