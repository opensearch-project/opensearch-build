#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import sys

from checkout_workflow.checkout_args import CheckoutArgs
from git.git_repository import GitRepository
from manifests.input_manifest import InputComponentFromSource, InputManifest
from system import console
from system.temporary_directory import TemporaryDirectory


def main() -> int:
    args = CheckoutArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)

    with TemporaryDirectory(keep=True, chdir=True) as work_dir:
        logging.info(f"Checking out into {work_dir.name}")

        for component in manifest.components.select():
            logging.info(f"Checking out {component.name}")
            if type(component) is InputComponentFromSource:
                with GitRepository(
                    component.repository,
                    component.ref,
                    os.path.join(work_dir.name, component.name),
                    component.working_directory,
                ) as repo:
                    logging.debug(f"Checked out {component.name} into {repo.dir}")

    logging.info(f"Done, checked out into {work_dir.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
