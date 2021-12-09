# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from ci_workflow.ci_check_gradle_properties_version import CiCheckGradlePropertiesVersion
from ci_workflow.ci_target import CiTarget
from manifests.input_manifest import Component
from system.properties_file import PropertiesFile


class TestCiCheckGradlePropertiesVersion(unittest.TestCase):
    def __mock_check(self, props=None, component=None, snapshot=True):
        with patch.object(CiCheckGradlePropertiesVersion, "_CiCheckGradleProperties__get_properties") as mock_properties:
            mock_properties.return_value = PropertiesFile(props)
            return CiCheckGradlePropertiesVersion(
                component=component or MagicMock(),
                git_repo=MagicMock(),
                target=CiTarget(version="1.1.0", name="opensearch", snapshot=snapshot),
            )

    def test_has_version(self):
        self.__mock_check({"version": "1.1.0.0-SNAPSHOT"}).check()

    def test_missing_version(self):
        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            self.__mock_check().check()
        self.assertEqual(
            str(err.exception),
            "Expected to have version='1.1.0.0-SNAPSHOT', but none was found.",
        )

    def test_invalid_version(self):
        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            self.__mock_check({"version": "1.2.0-SNAPSHOT"}).check()
        self.assertEqual(
            str(err.exception),
            "Expected to have version='1.1.0.0-SNAPSHOT', but was '1.2.0-SNAPSHOT'.",
        )

    def test_component_version_opensearch(self):
        check = self.__mock_check(
            props={"version": "1.1.0.0-SNAPSHOT"},
            component=Component({"name": "OpenSearch", "repository": "", "ref": ""}),
        )

        self.assertEqual(check.checked_version, "1.1.0-SNAPSHOT")

        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            check.check()

        self.assertEqual(
            str(err.exception),
            "Expected to have version='1.1.0-SNAPSHOT', but was '1.1.0.0-SNAPSHOT'.",
        )

    def test_component_version(self):
        check = self.__mock_check(
            props={"version": "1.1.0-SNAPSHOT"},
            component=Component({"name": "Plugin", "repository": "", "ref": ""}),
        )

        self.assertEqual(check.checked_version, "1.1.0.0-SNAPSHOT")

        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            check.check()

        self.assertEqual(
            str(err.exception),
            "Expected to have version='1.1.0.0-SNAPSHOT', but was '1.1.0-SNAPSHOT'.",
        )
