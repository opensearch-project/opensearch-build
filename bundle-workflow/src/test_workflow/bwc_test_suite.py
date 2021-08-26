# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

#!/usr/bin/env python

import os
import sys
import subprocess

from manifests.bundle_manifest import BundleManifest
from system.shell_executor import ShellExecutor
from git.git_repository import GitRepository
from system.temporary_directory import TemporaryDirectory
from test_workflow.test_args import TestArgs

class BwcTestSuite:
    manifest: str
    component: str
    keep: bool
    def __init__(self, manifest, component, keep):
        self.manifest = manifest
        self.component = component
        self.keep = keep

    def pull_component(self, component, work_dir):
        GitRepository(component.repository, component.commit_id, os.path.join(work_dir, component.name))

    def run_tests(self, work_dir):
        bwc_script = "bwctest.sh"
        run_bwctests = f"./{bwc_script}"
        output = ShellExecutor.check_output(run_bwctests, work_dir, True)
        return output

    def component_bwc_tests(self, component, work_dir):
        self.pull_component(component, work_dir)
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
                    console_output = self.component_bwc_tests(component, work_dir)
            # TODO: Store and report test results, send notification via {console_output}