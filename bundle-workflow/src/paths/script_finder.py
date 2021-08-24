# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os


class ScriptFinder:
    """
    ScriptFinder is a helper that abstracts away the details of where to look for build, test and install scripts.

    For build.sh and integtest.sh scripts, given a component name and a checked-out Git repository,
    it will look in the following locations, in order:
      * Root of the Git repository
      * /scripts/<script-name> in the Git repository
      * <component_scripts_path>/<component_name>/<script-name>
      * <default_scripts_path>/<script-name>

    For install.sh scripts, given a component name, it will look in the following locations, in order:
      * <component_scripts_path>/<component_name>/<script-name>
      * <default_scripts_path>/<script-name>
    """

    def __init__(self):
        self.component_scripts_path = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "../../scripts/components"
            )
        )
        self.default_scripts_path = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "../../scripts/default"
            )
        )

    def find_build_script(self, component_name, git_dir):
        paths = [
            os.path.realpath(os.path.join(git_dir, "build.sh")),
            os.path.realpath(os.path.join(git_dir, "scripts/build.sh")),
            os.path.realpath(
                os.path.join(self.component_scripts_path, component_name, "build.sh")
            ),
            os.path.realpath(os.path.join(self.default_scripts_path, "build.sh")),
        ]

        build_script = next(filter(lambda path: os.path.exists(path), paths), None)
        if build_script is None:
            raise RuntimeError(f"Could not find build.sh script. Looked in {paths}")
        return build_script

    def find_integ_test_script(self, component_name, git_dir):
        paths = [
            os.path.realpath(os.path.join(git_dir, "integtest.sh")),
            os.path.realpath(os.path.join(git_dir, "scripts/integtest.sh")),
            os.path.realpath(
                os.path.join(
                    self.component_scripts_path, component_name, "integtest.sh"
                )
            ),
            os.path.realpath(os.path.join(self.default_scripts_path, "integtest.sh")),
        ]

        test_script = next(filter(lambda path: os.path.exists(path), paths), None)
        if test_script is None:
            raise RuntimeError(f"Could not find integtest.sh script. Looked in {paths}")
        return test_script

    def find_install_script(self, component_name):
        paths = [
            os.path.realpath(
                os.path.join(self.component_scripts_path, component_name, "install.sh")
            ),
            os.path.realpath(os.path.join(self.default_scripts_path, "install.sh")),
        ]

        install_script = next(filter(lambda path: os.path.exists(path), paths), None)
        if install_script is None:
            raise RuntimeError(f"Could not find install.sh script. Looked in {paths}")
        return install_script
