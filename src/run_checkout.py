#!/usr/bin/env python

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
from manifests.input_manifest import InputManifest
from system import console
from system.temporary_directory import TemporaryDirectory


def main():
    args = CheckoutArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)

    with TemporaryDirectory(keep=True) as work_dir:
        logging.info(f"Checking out into {work_dir}")

        os.chdir(work_dir)

        for component in manifest.components:

            logging.info(f"Checking out {component.name}")
            GitRepository(
                component.repository,
                component.ref,
                os.path.join(work_dir, component.name),
                component.working_directory,
            )

    logging.info(f"Done, checked out into {work_dir}.")


if __name__ == "__main__":
    sys.exit(main())
