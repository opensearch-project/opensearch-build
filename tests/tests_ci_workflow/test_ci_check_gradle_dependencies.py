# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock

from ci_workflow.ci_check_gradle_dependencies import CiCheckGradleDependencies
from ci_workflow.ci_target import CiTarget


class TestCiCheckGradleDependencies(unittest.TestCase):
    class DummyDependencies(CiCheckGradleDependencies):
        def check(self):
            pass

    def __mock_dependencies(self, props="", snapshot=False, gradle_project=None):
        git_repo = MagicMock()
        git_repo.output.return_value = props

        return TestCiCheckGradleDependencies.DummyDependencies(
            component=MagicMock(),
            git_repo=git_repo,
            target=CiTarget(version="1.1.0", name="opensearch", snapshot=snapshot),
            args=gradle_project,
        )

    def test_executes_gradle_dependencies(self):
        check = self.__mock_dependencies()
        check.git_repo.output.assert_called_once_with(
            './gradlew :dependencies -Dopensearch.version=1.1.0 -Dbuild.snapshot=false --configuration compileOnly | grep -e "---"'
        )

    def test_executes_gradle_dependencies_snapshot(self):
        check = self.__mock_dependencies(snapshot=True)
        check.git_repo.output.assert_called_once_with(
            './gradlew :dependencies -Dopensearch.version=1.1.0-SNAPSHOT -Dbuild.snapshot=true --configuration compileOnly | grep -e "---"'
        )

    def test_executes_gradle_dependencies_project(self):
        check = self.__mock_dependencies(snapshot=True, gradle_project="project")
        check.git_repo.output.assert_called_once_with(
            './gradlew project:dependencies -Dopensearch.version=1.1.0-SNAPSHOT -Dbuild.snapshot=true --configuration compileOnly | grep -e "---"'
        )

    def test_loads_tree(self):
        data_path = os.path.join(os.path.dirname(__file__), "data", "job_scheduler_dependencies.txt")
        with open(data_path) as f:
            check = self.__mock_dependencies(props=f.read())
            self.assertEqual(
                check.dependencies.get_value("org.opensearch:opensearch"),
                "1.1.0-SNAPSHOT",
            )
            self.assertEqual(
                check.dependencies.get_value("org.opensearch:opensearch/org.opensearch:opensearch-core"),
                "1.1.0-SNAPSHOT",
            )
            self.assertEqual(check.dependencies.get_value("com.puppycrawl.tools:checkstyle"), "8.29")
            self.assertEqual(
                check.dependencies.get_value("com.puppycrawl.tools:checkstyle/antlr:antlr"),
                "2.7.7",
            )
            self.assertEqual(
                check.dependencies.get_value("com.puppycrawl.tools:checkstyle/commons-beanutils:commons-beanutils/commons-collections:commons-collections"),
                "3.2.2",
            )
