# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from ci_workflow.ci_check_gradle_dependencies_opensearch import (
    CiCheckGradleDependenciesOpenSearchVersion,
    CiCheckGradlePluginDependenciesOpenSearchVersion)
from ci_workflow.ci_target import CiTarget
from system.properties_file import PropertiesFile


class TestCiCheckGradleDependenciesOpenSearchVersion(unittest.TestCase):
    def __mock_check(self, props=None):
        with patch.object(
            CiCheckGradleDependenciesOpenSearchVersion,
            "_CiCheckGradleDependencies__get_dependencies",
        ) as mock_dependencies:
            mock_dependencies.return_value = PropertiesFile(props)
            return CiCheckGradleDependenciesOpenSearchVersion(
                component=MagicMock(),
                git_repo=MagicMock(),
                target=CiTarget(version="1.1.0", snapshot=True),
            )

    def test_gradle_project(self):
        self.assertIsNone(self.__mock_check().gradle_project)

    def test_has_version(self):
        self.__mock_check({"org.opensearch:opensearch": "1.1.0-SNAPSHOT"}).check()

    def test_missing_version(self):
        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            self.__mock_check({}).check()
        self.assertEqual(
            str(err.exception),
            "Expected to have org.opensearch:opensearch='1.1.0-SNAPSHOT', but none was found.",
        )

    def test_invalid_version(self):
        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            self.__mock_check({"org.opensearch:opensearch": "1.2.0-SNAPSHOT"}).check()
        self.assertEqual(
            str(err.exception),
            "Expected to have org.opensearch:opensearch='1.1.0-SNAPSHOT', but was '1.2.0-SNAPSHOT'.",
        )

    def test_executes_gradle_command(self):
        check = CiCheckGradleDependenciesOpenSearchVersion(
            component=MagicMock(),
            git_repo=MagicMock(),
            target=CiTarget(version="1.1.0", snapshot=True),
        )
        check.git_repo.output.assert_called_once_with(
            './gradlew :dependencies -Dopensearch.version=1.1.0-SNAPSHOT -Dbuild.snapshot=true | grep -e "---"'
        )


class TestCheckGradlePluginDependenciesOpenSearchVersion(unittest.TestCase):
    def test_executes_gradle_plugin_command(self):
        check = CiCheckGradlePluginDependenciesOpenSearchVersion(
            component=MagicMock(),
            git_repo=MagicMock(),
            target=CiTarget(version="1.1.0", snapshot=True),
        )
        self.assertEqual(check.gradle_project, "plugin")
        check.git_repo.output.assert_called_once_with(
            './gradlew plugin:dependencies -Dopensearch.version=1.1.0-SNAPSHOT -Dbuild.snapshot=true | grep -e "---"'
        )
