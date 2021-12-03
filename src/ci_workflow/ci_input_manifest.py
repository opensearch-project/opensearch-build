# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging

from ci_workflow.ci_check_lists import CiCheckLists
from ci_workflow.ci_manifest import CiManifest
from ci_workflow.ci_target import CiTarget
from manifests.input_manifest import InputManifest
from system.temporary_directory import TemporaryDirectory


class CiInputManifest(CiManifest):
    def __init__(self, keep, snapshot, component, file, component_command):
        self.keep = keep
        self.snapshot = snapshot
        self.component = component
        self.file = file
        self.component_command = component_command

    def __from_file(self):
        self.manifest = InputManifest.from_file(self.file)

    def check(self):
        self.__from_file()

        target = CiTarget(version=self.manifest.build.version, snapshot=self.snapshot)

        with TemporaryDirectory(keep=self.keep, chdir=True) as work_dir:
            logging.info(f"Sanity-testing in {work_dir.name}")

            logging.info(f"Sanity testing {self.manifest.build.name}")

            for component in self.manifest.components.select(focus=self.component):
                logging.info(f"Sanity testing {component.name}")

                try:
                    ci_check_list = CiCheckLists.from_component(component, target)
                    ci_check_list.checkout(work_dir.name)
                    ci_check_list.check()
                    logging.info("Done.")
                except:
                    logging.error(f"Error checking {component.name}, retry with: {self.component_command(component.name)}")
                    raise
