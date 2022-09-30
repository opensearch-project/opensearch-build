# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock

from ci_workflow.ci_check_gradle_publish_to_maven_local import CiCheckGradlePublishToMavenLocal
from ci_workflow.ci_target import CiTarget


class TestCiCheckGradlePublishToMavenLocal(unittest.TestCase):
    def test_executes_gradle_command(self) -> None:
        check = CiCheckGradlePublishToMavenLocal(
            component=MagicMock(),
            git_repo=MagicMock(),
            target=CiTarget(version="1.1.0", name="opensearch", qualifier=None, snapshot=False),
        )
        check.check()
        exec_command = unittest.mock.create_autospec(check.git_repo.execute)
        exec_command.assert_called_once_with("./gradlew publishToMavenLocal -Dopensearch.version=1.1.0 -Dbuild.snapshot=false")

    def test_executes_gradle_command_snapshot(self) -> None:
        check = CiCheckGradlePublishToMavenLocal(
            component=MagicMock(),
            git_repo=MagicMock(),
            target=CiTarget(version="1.1.0", name="opensearch", qualifier=None, snapshot=True),
        )
        check.check()
        exec_command = unittest.mock.create_autospec(check.git_repo.execute)
        exec_command.assert_called_once_with("./gradlew publishToMavenLocal -Dopensearch.version=1.1.0-SNAPSHOT -Dbuild.snapshot=true")

    def test_executes_gradle_command_qualifier_snapshot(self) -> None:
        check = CiCheckGradlePublishToMavenLocal(
            component=MagicMock(),
            git_repo=MagicMock(),
            target=CiTarget(version="2.0.0", name="opensearch", qualifier="alpha1", snapshot=True),
        )
        check.check()
        exec_command = unittest.mock.create_autospec(check.git_repo.execute)
        exec_command.assert_called_once_with("./gradlew publishToMavenLocal -Dopensearch.version=2.0.0-alpha1-SNAPSHOT -Dbuild.snapshot=true -Dbuild.version_qualifier=alpha1")
