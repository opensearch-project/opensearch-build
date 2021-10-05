#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import sys

from ci_workflow.ci import Ci
from ci_workflow.ci_args import CiArgs
from ci_workflow.ci_target import CiTarget
from git.git_repository import GitRepository
from manifests.input_manifest import InputManifest
from system import console
from system.temporary_directory import TemporaryDirectory


def main():
    args = CiArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)

    target = CiTarget(version=manifest.build.version, snapshot=args.snapshot)

    with TemporaryDirectory(keep=args.keep) as work_dir:
        logging.info(f"Sanity-testing in {work_dir}")

        os.chdir(work_dir)

        logging.info(f"Sanity testing {manifest.build.name}")

        for component in manifest.components:

            if args.component and args.component != component.name:
                logging.info(f"Skipping {component.name}")
                continue

            logging.info(f"Sanity checking {component.name}")
            repo = GitRepository(
                component.repository,
                component.ref,
                os.path.join(work_dir, component.name),
                component.working_directory,
            )

            try:
                ci = Ci(component, repo, target)
                ci.check()
            except:
                logging.error(
                    f"Error checking {component.name}, retry with: {args.component_command(component.name)}"
                )
                raise

    logging.info("Done.")


if __name__ == "__main__":
    sys.exit(main())
