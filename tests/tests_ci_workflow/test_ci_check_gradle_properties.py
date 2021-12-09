# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock

from ci_workflow.ci_check_gradle_properties import CiCheckGradleProperties
from ci_workflow.ci_target import CiTarget


class TestCiCheckGradleProperties(unittest.TestCase):
    class DummyProperties(CiCheckGradleProperties):
        def check(self):
            pass

    def test_executes_gradle_properties(self):
        git_repo = MagicMock()
        git_repo.output.return_value = ""

        TestCiCheckGradleProperties.DummyProperties(
            component=MagicMock(),
            git_repo=git_repo,
            target=CiTarget(version="1.1.0", name="opensearch", snapshot=False),
        )

        git_repo.output.assert_called_once_with("./gradlew properties -Dopensearch.version=1.1.0 -Dbuild.snapshot=false")

    def test_executes_gradle_properties_snapshot(self):
        git_repo = MagicMock()
        git_repo.output.return_value = ""

        TestCiCheckGradleProperties.DummyProperties(
            component=MagicMock(),
            git_repo=git_repo,
            target=CiTarget(version="1.1.0", name="opensearch", snapshot=True),
        )

        git_repo.output.assert_called_once_with("./gradlew properties -Dopensearch.version=1.1.0-SNAPSHOT -Dbuild.snapshot=true")
