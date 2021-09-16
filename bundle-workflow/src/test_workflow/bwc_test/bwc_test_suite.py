# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import logging
import os

from paths.script_finder import ScriptFinder
from system.execute import execute
from test_workflow.test_component import TestComponent


class BwcTestSuite:
    manifest: str
    work_dir: str
    component: str
    keep: bool

    def __init__(self, manifest, work_dir, component=None, keep=False):
        self.manifest = manifest
        self.work_dir = work_dir
        self.script_finder = ScriptFinder()
        self.component = component
        self.keep = keep

    def run_tests(self, work_dir, component_name):
        script = self.script_finder.find_bwc_test_script(
            component_name, work_dir
        )
        if os.path.exists(script):
            cmd = f"{script}"
            (status, stdout, stderr) = execute(cmd, work_dir, True, False)
            return (status, stdout, stderr)
        else:
            logging.info(
                f"{script} does not exist. Skipping bwc tests for {component_name}"
            )

    def component_bwc_tests(self, component):
        test_component = TestComponent(component.repository, component.commit_id)
        test_component.checkout(os.path.join(self.work_dir, component.name))
        try:
            console_output = self.run_tests(self.work_dir + "/" + component.name, component.name)
            return console_output
        except:
            # TODO: Store and report test failures for {component}
            logging.info(f"Exception while running BWC tests for {component.name}")

    def execute(self):
        # For each component, check out the git repo and run `bwctest.sh`
        for component in self.manifest.components:
            if self.component is None or self.component == component.name:
                # TODO: Store and report test results, send notification via {console_output}
                self.component_bwc_tests(component)
