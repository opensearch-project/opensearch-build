#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from ci_workflow.ci import Ci
from ci_workflow.ci_args import CiArgs
from git.git_repository import GitRepository
from manifests.input_manifest import InputManifest
from system import console
from system.arch import current_arch
from system.temporary_directory import TemporaryDirectory

args = CiArgs()
console.configure(level=args.logging_level)
arch = current_arch()
manifest = InputManifest.from_file(args.manifest)

with TemporaryDirectory(keep=args.keep) as work_dir:
    logging.info(f"Sanity-testing in {work_dir}")

    os.chdir(work_dir)

    logging.info(f"Sanity testing {manifest.build.name} ({arch})")

    for component in manifest.components:

        if args.component and args.component != component.name:
            logging.info(f"Skipping {component.name}")
            continue

        logging.info(f"Sanity checking {component.name}")
        repo = GitRepository(
            component.repository, component.ref, os.path.join(work_dir, component.name)
        )

        try:
            ci = Ci(component.name, repo)
            ci.check(manifest.build.version, arch, args.snapshot)
        except:
            logging.error(
                f"Error checking {component.name}, retry with: {args.component_command(component.name)}"
            )
            raise

logging.info("Done.")
