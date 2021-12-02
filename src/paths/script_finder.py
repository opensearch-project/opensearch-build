# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from typing import Callable, List


class ScriptFinder:
    class ScriptNotFoundError(Exception):
        def __init__(self, kind: str, paths: List[str]) -> None:
            self.kind = kind
            self.paths = paths
            super().__init__(f"Could not find {kind} script. Looked in {paths}.")

    component_scripts_path = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join("..", "..", "scripts", "components")))

    default_scripts_path = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.join("..", "..", "scripts", "default")))

    """
    ScriptFinder is a helper that abstracts away the details of where to look for build, test and install scripts.

    For build.sh and integtest.sh scripts, given a component name and a checked-out Git repository,
    it will look in the following locations, in order:
      * <component_scripts_path>/<component_name>/<script-name>
      * root of the component's Git repository
      * /scripts/<script-name> in the component's Git repository
      * <default_scripts_path>/<script-name>

    For install.sh scripts, given a component name, it will look in the following locations, in order:
      * <component_scripts_path>/<component_name>/<script-name>
      * <default_scripts_path>/<script-name>
    """

    @classmethod
    def __find_script(cls, name: str, paths: List[str]) -> str:
        exists: Callable[[str], bool] = lambda path: os.path.exists(path)
        script = next(filter(exists, paths), None)
        if script is None:
            raise ScriptFinder.ScriptNotFoundError(name, paths)

        return script

    @classmethod
    def __find_named_script(cls, script_name: str, component_name: str, git_dir: str) -> str:
        paths = [
            os.path.realpath(os.path.join(cls.component_scripts_path, component_name, script_name)),
            os.path.realpath(os.path.join(git_dir, script_name)),
            os.path.realpath(os.path.join(git_dir, "scripts", script_name)),
            os.path.realpath(os.path.join(cls.default_scripts_path, script_name)),
        ]

        return cls.__find_script(script_name, paths)

    @classmethod
    def find_build_script(cls, project: str, component_name: str, git_dir: str) -> str:
        paths = [
            os.path.realpath(os.path.join(cls.component_scripts_path, component_name, "build.sh")),
            os.path.realpath(os.path.join(git_dir, "build.sh")),
            os.path.realpath(os.path.join(git_dir, "scripts", "build.sh")),
            os.path.realpath(
                os.path.join(
                    cls.default_scripts_path,
                    project.replace(" ", "-").lower(),
                    "build.sh",
                )
            ),
        ]

        return cls.__find_script("build.sh", paths)

    @classmethod
    def find_install_script(cls, component_name: str) -> str:
        paths = [
            os.path.realpath(os.path.join(cls.component_scripts_path, component_name, "install.sh")),
            os.path.realpath(os.path.join(cls.default_scripts_path, "install.sh")),
        ]

        return cls.__find_script("install.sh", paths)

    @classmethod
    def find_integ_test_script(cls, component_name: str, git_dir: str) -> str:
        return cls.__find_named_script("integtest.sh", component_name, git_dir)

    @classmethod
    def find_bwc_test_script(cls, component_name: str, git_dir: str) -> str:
        return cls.__find_named_script("bwctest.sh", component_name, git_dir)
