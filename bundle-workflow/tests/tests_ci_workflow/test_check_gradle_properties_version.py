# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from ci_workflow.check_gradle_properties_version import \
    CheckGradlePropertiesVersion
from system.properties_file import PropertiesFile


class TestCheckGradlePropertiesVersion(unittest.TestCase):
    def __mock_check(self, props=None):
        with patch.object(
            CheckGradlePropertiesVersion, "_CheckGradleProperties__get_properties"
        ) as mock_properties:
            mock_properties.return_value = PropertiesFile(props)
            return CheckGradlePropertiesVersion(
                component=MagicMock(),
                git_repo=MagicMock(),
                version="1.1.0",
                arch="x86",
                snapshot=True,
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
