# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import os
import subprocess

from system.temporary_directory import TemporaryDirectory
from test_workflow.test_component import TestComponent


class BwcTestSuite:
    manifest: str
    component: str
    keep: bool

    def __init__(self, manifest, component, keep):
        self.manifest = manifest
        self.component = component
        self.keep = keep

    def run_tests(self, work_dir):
        bwc_script = "bwctest.sh"
        run_bwctests = f"./{bwc_script}"
        output = subprocess.check_output(run_bwctests, cwd=work_dir, shell=True)
        return output

    def component_bwc_tests(self, component, work_dir):
        test_component = TestComponent(component.repository, component.commit_id)
        test_component.checkout(os.path.join(work_dir, component.name))
        try:
            console_output = self.run_tests(work_dir + "/" + component.name)
            return console_output
        except:
            # TODO: Store and report test failures for {component}
            print(f"Exception while running BWC tests for {component.name}")

    def execute(self):
        # TODO copy all maven dependencies from S3 to local
        with TemporaryDirectory(keep=self.keep) as work_dir:
            os.chdir(work_dir)
            # For each component, check out the git repo and run `bwctest.sh`
            for component in self.manifest.components:
                if self.component is None or self.component == component.name:
                    # TODO: Store and report test results, send notification via {console_output}
                    self.component_bwc_tests(component, work_dir)
