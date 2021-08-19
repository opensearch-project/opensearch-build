# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
from dataclasses import dataclass

@dataclass
class ScriptFinder:
    '''
    ScriptFinder is a helper that abstracts away the details of where to look for build and test scripts.
    Given a component name and a checked-out Git repository, it will look in the following locations, in order, for either "build.sh" or "integtest.sh", depending on the use case:
      * Root of the Git repository
      * /scripts/<script-name> in the Git repository
      * <component_scripts_path>/<component_name>/<script-name>
      * <default_scripts_path>/<script-name>
    '''

    component_scripts_path: str
    default_scripts_path: str

    def find_build_script(self, component_name, git_dir):
        paths = [
            os.path.realpath(os.path.join(git_dir, 'build.sh')),
            os.path.realpath(os.path.join(git_dir, 'scripts/build.sh')),
            os.path.realpath(os.path.join(self.component_scripts_path, component_name, 'build.sh')),
            os.path.realpath(os.path.join(self.default_scripts_path, 'build.sh'))
        ]

        build_script = next(filter(lambda path: os.path.exists(path), paths), None)
        if build_script is None:
            raise RuntimeError(f'Could not find build.sh script. Looked in {paths}')
        return build_script

    def find_integ_test_script(self, component_name, git_dir):
        paths = [
            os.path.realpath(os.path.join(git_dir, 'integtest.sh')),
            os.path.realpath(os.path.join(git_dir, 'scripts/integtest.sh')),
            os.path.realpath(os.path.join(self.component_scripts_path, component_name, 'integtest.sh')),
            os.path.realpath(os.path.join(self.default_scripts_path, 'integtest.sh'))
        ]

        test_script = next(filter(lambda path: os.path.exists(path), paths), None)
        if test_script is None:
            raise RuntimeError(f'Could not find integtest.sh script. Looked in {paths}')
        return test_script

    def find_install_script(self, component_name):
        paths = [
            os.path.realpath(os.path.join(self.component_scripts_path, component_name, 'install.sh')),
            os.path.realpath(os.path.join(self.default_scripts_path, 'install.sh'))
        ]

        install_script = next(filter(lambda path: os.path.exists(path), paths), None)
        if install_script is None:
            raise RuntimeError(f'Could not find install.sh script. Looked in {paths}')
        return install_script