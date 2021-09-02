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

from test_workflow.test_component import TestComponent


class BwcTestSuite:
    manifest: str
    component: str
    work_dir: str

    def __init__(self, manifest, component, work_dir):
        self.manifest = manifest
        self.component = component
        self.work_dir = work_dir

    def run_tests(self, work_dir):
        run_bwctests = f"./bwctest.sh"
        output = subprocess.check_output(run_bwctests, cwd=work_dir, shell=True)
        return output

    def component_bwc_tests(self):
        test_component = TestComponent(
            self.component.repository, self.component.commit_id
        )
        test_component.checkout(os.path.join(self.work_dir, self.component.name))
        try:
            console_output = self.run_tests(self.work_dir + "/" + self.component.name)
            return console_output
        except:
            # TODO: Store and report test failures for {component}
            print(f"Exception while running BWC tests for {self.component.name}")
