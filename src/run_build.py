#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import sys

from build_workflow.build_args import BuildArgs
from build_workflow.build_recorder import BuildRecorder
from build_workflow.build_target import BuildTarget
from build_workflow.builder import Builder
from git.git_repository import GitRepository
from manifests.input_manifest import InputManifest
from system import console
from system.temporary_directory import TemporaryDirectory


def main():
    args = BuildArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)
    output_dir = os.path.join(os.getcwd(), "builds")

    with TemporaryDirectory(keep=args.keep, chdir=True) as work_dir:
        logging.info(f"Building in {work_dir.name}")

        target = BuildTarget(
            name=manifest.build.name,
            version=manifest.build.version,
            snapshot=args.snapshot,
            output_dir=output_dir,
            platform=args.platform,
            architecture=args.architecture,
        )

        os.makedirs(target.output_dir, exist_ok=True)

        build_recorder = BuildRecorder(target)

        logging.info(f"Building {manifest.build.name} ({target.architecture}) into {target.output_dir}")

        for component in manifest.components.select(focus=args.component, platform=target.platform):
            logging.info(f"Building {component.name}")

            with GitRepository(
                component.repository,
                component.ref,
                os.path.join(work_dir.name, component.name),
                component.working_directory,
            ) as repo:
                try:
                    builder = Builder(component.name, repo, build_recorder)
                    builder.build(target)
                    builder.export_artifacts()
                except:
                    logging.error(f"Error building {component.name}, retry with: {args.component_command(component.name)}")
                    raise

        build_recorder.write_manifest()

    logging.info("Done.")


if __name__ == "__main__":
    sys.exit(main())
