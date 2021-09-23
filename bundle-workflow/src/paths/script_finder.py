# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os


class ScriptFinder:
    class ScriptNotFoundError(Exception):
        def __init__(self, kind, paths):
            self.kind = kind
            self.paths = paths
            super().__init__(f"Could not find {kind} script. Looked in {paths}.")

    component_scripts_path = os.path.realpath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../scripts/components"
        )
    )

    default_scripts_path = os.path.realpath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "../../scripts/default"
        )
    )

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

    @classmethod
    def __find_script(cls, name, paths):
        script = next(filter(lambda path: os.path.exists(path), paths), None)
        if script is None:
            raise ScriptFinder.ScriptNotFoundError(name, paths)
        return script

    @classmethod
    def find_build_script(cls, component_name, git_dir):
        paths = [
            os.path.realpath(os.path.join(git_dir, "build.sh")),
            os.path.realpath(os.path.join(git_dir, "scripts/build.sh")),
            os.path.realpath(
                os.path.join(cls.component_scripts_path, component_name, "build.sh")
            ),
            os.path.realpath(os.path.join(cls.default_scripts_path, "build.sh")),
        ]

        return cls.__find_script("build.sh", paths)

    @classmethod
    def find_integ_test_script(cls, component_name, git_dir):
        paths = [
            os.path.realpath(os.path.join(git_dir, "integtest.sh")),
            os.path.realpath(os.path.join(git_dir, "scripts/integtest.sh")),
            os.path.realpath(
                os.path.join(cls.component_scripts_path, component_name, "integtest.sh")
            ),
            os.path.realpath(os.path.join(cls.default_scripts_path, "integtest.sh")),
        ]

        return cls.__find_script("integtest.sh", paths)

    @classmethod
    def find_install_script(cls, component_name):
        paths = [
            os.path.realpath(
                os.path.join(cls.component_scripts_path, component_name, "install.sh")
            ),
            os.path.realpath(os.path.join(cls.default_scripts_path, "install.sh")),
        ]

        return cls.__find_script("install.sh", paths)

    @classmethod
    def find_bwc_test_script(cls, component_name, git_dir):
        paths = [
            os.path.realpath(os.path.join(git_dir, "bwctest.sh")),
            os.path.realpath(os.path.join(git_dir, "scripts/bwctest.sh")),
            os.path.realpath(
                os.path.join(cls.component_scripts_path, component_name, "bwctest.sh")
            ),
            os.path.realpath(os.path.join(cls.default_scripts_path, "bwctest.sh")),
        ]

        return cls.__find_script("bwctest.sh", paths)
