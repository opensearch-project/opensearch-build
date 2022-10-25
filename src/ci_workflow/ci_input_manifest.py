# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
from io import TextIOWrapper

from ci_workflow.ci_args import CiArgs
from ci_workflow.ci_check_lists import CiCheckLists
from ci_workflow.ci_manifest import CiManifest
from ci_workflow.ci_target import CiTarget
from manifests.input_manifest import InputManifest
from system.temporary_directory import TemporaryDirectory


class CiInputManifest(CiManifest):
    def __init__(self, file: TextIOWrapper, args: CiArgs) -> None:
        super().__init__(InputManifest.from_file(file), args)

    def __check__(self) -> None:

        target = CiTarget(
            version=self.manifest.build.version,
            name=self.manifest.build.filename,
            qualifier=self.manifest.build.qualifier if self.manifest.build.qualifier else None,
            snapshot=self.args.snapshot
        )

        with TemporaryDirectory(keep=self.args.keep, chdir=True) as work_dir:
            logging.info(f"Sanity-testing in {work_dir.name}")

            logging.info(f"Sanity testing {self.manifest.build.name}")

            for component in self.manifest.components.select(focus=self.args.components):
                logging.info(f"Sanity testing {component.name}")

                ci_check_list = CiCheckLists.from_component(component, target)
                ci_check_list.checkout(work_dir.name)
                ci_check_list.check()
                logging.info("Done.")
