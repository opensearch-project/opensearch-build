# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, patch

from paths.script_finder import ScriptFinder


class TestScriptFinder(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        # use root of this repo as the default git checkout directory
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))
        self.component_with_scripts = os.path.join(self.data_path, "git", "component-with-scripts")
        self.component_with_scripts_folder = os.path.join(self.data_path, "git", "component-with-scripts-folder")
        self.component_without_scripts = os.path.join(self.data_path, "git", "component-without-scripts")

    # find_build_script

    def test_find_build_script_opensearch_default(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.default_scripts_path, "opensearch", "build.sh"),
            ScriptFinder.find_build_script("OpenSearch", "invalid", self.component_without_scripts),
            msg="A component without an override resolves to a default.",
        )

    def test_find_build_script_opensearch_dashboards_default(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.default_scripts_path, "opensearch-dashboards", "build.sh"),
            ScriptFinder.find_build_script("OpenSearch-Dashboards", "invalid", self.component_without_scripts),
            msg="A component without an override resolves to a default.",
        )

    def test_find_build_script_component_override(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.component_scripts_path, "OpenSearch", "build.sh"),
            ScriptFinder.find_build_script("OpenSearch", "OpenSearch", self.component_without_scripts),
            msg="A component without scripts resolves to a component override.",
        )

    def test_find_build_script_component_script(self) -> None:
        self.assertEqual(
            os.path.join(self.component_with_scripts, "build.sh"),
            ScriptFinder.find_build_script("OpenSearch", "foobar", self.component_with_scripts),
            msg="A component with a script resolves to the script at the root.",
        )

    def test_find_build_script_component_script_in_folder(self) -> None:
        self.assertEqual(
            os.path.join(self.component_with_scripts_folder, "scripts", "build.sh"),
            ScriptFinder.find_build_script("OpenSearch", "foobar", self.component_with_scripts_folder),
            msg="A component with a scripts folder resolves to a script in that folder.",
        )

    def test_find_build_script_component_script_in_folder_with_default(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.component_scripts_path, "OpenSearch", "build.sh"),
            ScriptFinder.find_build_script("OpenSearch", "OpenSearch", self.component_with_scripts_folder),
            msg="A component with a scripts folder resolves to the override.",
        )

    @patch("os.path.exists", return_value=False)
    def test_find_build_script_does_not_exist(self, *mocks: MagicMock) -> None:
        with self.assertRaisesRegex(
            ScriptFinder.ScriptNotFoundError,
            "Could not find build.sh script. Looked in .*",
        ):
            ScriptFinder.find_build_script("OpenSearch", "anything", self.component_without_scripts)

    # find_integ_test_script

    def test_find_integ_test_script_default(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.default_scripts_path, "integtest.sh"),
            ScriptFinder.find_integ_test_script("invalid", self.component_without_scripts),
            msg="A component without an override resolves to a default.",
        )

    def test_find_integ_test_script_component_override(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.component_scripts_path, "OpenSearch", "integtest.sh"),
            ScriptFinder.find_integ_test_script("OpenSearch", self.component_without_scripts),
            msg="A component without scripts resolves to a component override.",
        )

    def test_find_integ_test_script_component_script(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.component_scripts_path, "OpenSearch", "integtest.sh"),
            ScriptFinder.find_integ_test_script("OpenSearch", self.component_with_scripts),
            msg="A component with a script resolves to the script at the root.",
        )

    def test_find_integ_test_script_component_script_in_folder(self) -> None:
        self.assertEqual(
            os.path.join(self.component_with_scripts_folder, "scripts", "integtest.sh"),
            ScriptFinder.find_integ_test_script("foobar", self.component_with_scripts_folder),
            msg="A component with a scripts folder resolves to an override.",
        )

    def test_find_integ_test_script_component_script_in_folder_with_default(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.component_scripts_path, "OpenSearch", "integtest.sh"),
            ScriptFinder.find_integ_test_script("OpenSearch", self.component_with_scripts_folder),
            msg="A component with a scripts folder resolves to a script in that folder.",
        )

    @patch("os.path.exists", return_value=False)
    def test_find_integ_test_script_does_not_exist(self, *mocks: MagicMock) -> None:
        with self.assertRaisesRegex(
            ScriptFinder.ScriptNotFoundError,
            "Could not find integtest.sh script. Looked in .*",
        ):
            ScriptFinder.find_integ_test_script("anything", self.component_without_scripts)

    # find_install_script

    def test_find_install_script_default(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.default_scripts_path, "install.sh"),
            ScriptFinder.find_install_script("invalid"),
            msg="A component without an override resolves to a default.",
        )

    def test_find_install_script_component_override(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.component_scripts_path, "performance-analyzer", "install.sh"),
            ScriptFinder.find_install_script("performance-analyzer"),
            msg="A component without scripts resolves to a component override.",
        )

    @patch("os.path.exists", return_value=False)
    def test_find_install_script_does_not_exist(self, *mocks: MagicMock) -> None:
        with self.assertRaisesRegex(
            ScriptFinder.ScriptNotFoundError,
            "Could not find install.sh script. Looked in .*",
        ):
            ScriptFinder.find_install_script("anything")

    # find_bwc_test_script

    def test_find_bwc_test_script_default(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.default_scripts_path, "bwctest.sh"),
            ScriptFinder.find_bwc_test_script("invalid", self.component_without_scripts),
            msg="A component without an override resolves to a default.",
        )

    def test_find_bwc_test_script_component_override(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.component_scripts_path, "OpenSearch", "bwctest.sh"),
            ScriptFinder.find_bwc_test_script("OpenSearch", self.component_without_scripts),
            msg="A component without scripts resolves to a component override.",
        )

    def test_find_bwc_test_script_component_script(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.component_scripts_path, "OpenSearch", "bwctest.sh"),
            ScriptFinder.find_bwc_test_script("OpenSearch", self.component_with_scripts),
            msg="A component with a script resolves to the script at the root.",
        )

    def test_find_bwc_test_script_component_script_in_folder(self) -> None:
        self.assertEqual(
            os.path.join(self.component_with_scripts_folder, "scripts", "bwctest.sh"),
            ScriptFinder.find_bwc_test_script("foobar", self.component_with_scripts_folder),
            msg="A component with a scripts folder resolves to an override.",
        )

    def test_find_bwc_test_script_component_script_in_folder_with_default(self) -> None:
        self.assertEqual(
            os.path.join(ScriptFinder.component_scripts_path, "OpenSearch", "bwctest.sh"),
            ScriptFinder.find_bwc_test_script("OpenSearch", self.component_with_scripts_folder),
            msg="A component with a scripts folder resolves to a script in that folder.",
        )

    @patch("os.path.exists", return_value=False)
    def test_find_bwc_test_script_does_not_exist(self, *mocks: MagicMock) -> None:
        with self.assertRaisesRegex(
            ScriptFinder.ScriptNotFoundError,
            "Could not find bwctest.sh script. Looked in .*",
        ):
            ScriptFinder.find_bwc_test_script("anything", self.component_without_scripts)
