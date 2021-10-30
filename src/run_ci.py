#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import sys

from ci_workflow.ci_args import CiArgs
from ci_workflow.ci_check_lists import CiCheckLists
from ci_workflow.ci_target import CiTarget
from manifests.input_manifest import InputManifest
from system import console
from system.temporary_directory import TemporaryDirectory


def main():
    args = CiArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)

    target = CiTarget(version=manifest.build.version, snapshot=args.snapshot)

    with TemporaryDirectory(keep=args.keep, chdir=True) as work_dir:
        logging.info(f"Sanity-testing in {work_dir.name}")

        logging.info(f"Sanity testing {manifest.build.name}")

        for component in manifest.components.select(focus=args.component):
            logging.info(f"Sanity testing {component.name}")

            try:
                ci_check_list = CiCheckLists.from_component(component, target)
                ci_check_list.checkout(work_dir.name)
                ci_check_list.check()
            except:
                logging.error(f"Error checking {component.name}, retry with: {args.component_command(component.name)}")
                raise

    logging.info("Done.")


if __name__ == "__main__":
    sys.exit(main())
