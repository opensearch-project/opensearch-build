# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from typing import Any
from unittest.mock import MagicMock, patch

from ci_workflow.ci_check_npm_package_version import CiCheckNpmPackageVersion
from ci_workflow.ci_target import CiTarget
from manifests.input_manifest import Component
from system.properties_file import PropertiesFile


class TestCiCheckNpmPackageVersion(unittest.TestCase):
    def __mock_check(self, props: Any = None, component: Component = None, snapshot: bool = True) -> CiCheckNpmPackageVersion:
        with patch.object(CiCheckNpmPackageVersion, "_CiCheckPackage__get_properties") as mock_properties:
            mock_properties.return_value = PropertiesFile(props)
            return CiCheckNpmPackageVersion(
                component=component or MagicMock(),
                git_repo=MagicMock(),
                target=CiTarget(version="1.1.0", name="dashboards-plugin", qualifier=None, snapshot=snapshot),
            )

    def test_has_version(self) -> None:
        self.__mock_check({"version": "1.1.0.0"}).check()

    def test_missing_version(self) -> None:
        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            self.__mock_check().check()
        self.assertEqual(
            str(err.exception),
            "Expected to have version='1.1.0.0', but none was found.",
        )

    def test_invalid_version(self) -> None:
        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            self.__mock_check({"version": "1.2.0"}, component=None, snapshot=False).check()
        self.assertEqual(
            str(err.exception),
            "Expected to have version='1.1.0.0', but was '1.2.0'.",
        )

    def test_invalid_version_snapshot(self) -> None:
        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            self.__mock_check({"version": "1.2.0"}, component=None, snapshot=True).check()
        self.assertEqual(
            str(err.exception),
            "Expected to have version='1.1.0.0', but was '1.2.0'.",
        )

    def test_component_version_opensearch_dashboards(self) -> None:
        check = self.__mock_check(
            props={"version": "1.1.0.0"},
            component=Component({"name": "OpenSearch-Dashboards", "repository": "", "ref": ""}),
        )

        self.assertEqual(check.checked_version, "1.1.0")

        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            check.check()

        self.assertEqual(
            str(err.exception),
            "Expected to have version='1.1.0', but was '1.1.0.0'.",
        )

    def test_component_version(self) -> None:
        check = self.__mock_check(
            props={"version": "1.1.0"},
            component=Component({"name": "Plugin", "repository": "", "ref": ""}),
        )

        self.assertEqual(check.checked_version, "1.1.0.0")

        with self.assertRaises(PropertiesFile.UnexpectedKeyValueError) as err:
            check.check()

        self.assertEqual(
            str(err.exception),
            "Expected to have version='1.1.0.0', but was '1.1.0'.",
        )
