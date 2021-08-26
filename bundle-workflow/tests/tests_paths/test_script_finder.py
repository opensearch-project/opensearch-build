# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from paths.script_finder import ScriptFinder


class TestScriptFinder(unittest.TestCase):
    def setUp(self):
        self.script_finder = ScriptFinder()
        # use root of this repo as the default git checkout directory
        self.data_path = os.path.realpath(
            os.path.join(os.path.dirname(__file__), "data")
        )
        self.component_with_scripts = os.path.join(
            self.data_path, "git/component-with-scripts"
        )
        self.component_with_scripts_folder = os.path.join(
            self.data_path, "git/component-with-scripts-folder"
        )
        self.component_without_scripts = os.path.join(
            self.data_path, "git/component-without-scripts"
        )

    # find_build_script

    def test_find_build_script_default(self):
        self.assertEqual(
            os.path.join(self.script_finder.default_scripts_path, "build.sh"),
            self.script_finder.find_build_script(
                "invalid", self.component_without_scripts
            ),
            msg="A component without an override resolves to a default.",
        )

    def test_find_build_script_component_override(self):
        self.assertEqual(
            os.path.join(
                self.script_finder.component_scripts_path, "OpenSearch/build.sh"
            ),
            self.script_finder.find_build_script(
                "OpenSearch", self.component_without_scripts
            ),
            msg="A component without scripts resolves to a component override.",
        )

    def test_find_build_script_component_script(self):
        self.assertEqual(
            os.path.join(self.component_with_scripts, "build.sh"),
            self.script_finder.find_build_script(
                "OpenSearch", self.component_with_scripts
            ),
            msg="A component with a script resolves to the script at the root.",
        )

    def test_find_build_script_component_script_in_folder(self):
        self.assertEqual(
            os.path.join(self.component_with_scripts_folder, "scripts/build.sh"),
            self.script_finder.find_build_script(
                "OpenSearch", self.component_with_scripts_folder
            ),
            msg="A component with a scripts folder resolves to a script in that folder.",
        )

    # find_integ_test_script

    def test_find_integ_test_script_default(self):
        self.assertEqual(
            os.path.join(self.script_finder.default_scripts_path, "integtest.sh"),
            self.script_finder.find_integ_test_script(
                "invalid", self.component_without_scripts
            ),
            msg="A component without an override resolves to a default.",
        )

    def test_find_integ_test_script_component_override(self):
        self.assertEqual(
            os.path.join(
                self.script_finder.component_scripts_path, "OpenSearch/integtest.sh"
            ),
            self.script_finder.find_integ_test_script(
                "OpenSearch", self.component_without_scripts
            ),
            msg="A component without scripts resolves to a component override.",
        )

    def test_find_integ_test_script_component_script(self):
        self.assertEqual(
            os.path.join(self.component_with_scripts, "integtest.sh"),
            self.script_finder.find_integ_test_script(
                "OpenSearch", self.component_with_scripts
            ),
            msg="A component with a script resolves to the script at the root.",
        )

    def test_find_integ_test_script_component_script_in_folder(self):
        self.assertEqual(
            os.path.join(self.component_with_scripts_folder, "scripts/integtest.sh"),
            self.script_finder.find_integ_test_script(
                "OpenSearch", self.component_with_scripts_folder
            ),
            msg="A component with a scripts folder resolves to a script in that folder.",
        )

    # find_install_script

    def test_find_install_script_default(self):
        self.assertEqual(
            os.path.join(self.script_finder.default_scripts_path, "install.sh"),
            self.script_finder.find_install_script("invalid"),
            msg="A component without an override resolves to a default.",
        )

    def test_find_install_script_component_override(self):
        self.assertEqual(
            os.path.join(self.script_finder.component_scripts_path, "k-NN/install.sh"),
            self.script_finder.find_install_script("k-NN"),
            msg="A component without scripts resolves to a component override.",
        )
