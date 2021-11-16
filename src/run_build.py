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
from build_workflow.builders import Builders
from manifests.input_manifest import InputManifest
from system import console
from system.os import current_architecture, current_platform
from system.temporary_directory import TemporaryDirectory


def main():
    args = BuildArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)
    output_dir = os.path.join(os.getcwd(), "builds")

    if args.ref_manifest:
        manifest = manifest.stable(
            architecture=args.architecture or current_architecture(),
            platform=args.platform or current_platform(),
            snapshot=args.snapshot if args.snapshot is not None else False
        )
        if os.path.exists(args.ref_manifest):
            if manifest == InputManifest.from_path(args.ref_manifest):
                logging.info(f"No changes since {args.ref_manifest}")
            else:
                logging.info(f"Updating {args.ref_manifest}")
                manifest.to_file(args.ref_manifest)
        else:
            logging.info(f"Creating {args.ref_manifest}")
            manifest.to_file(args.ref_manifest)
        exit(0)

    with TemporaryDirectory(keep=args.keep, chdir=True) as work_dir:
        logging.info(f"Building in {work_dir.name}")

        target = BuildTarget(
            name=manifest.build.name,
            version=manifest.build.version,
            patches=manifest.build.patches,
            snapshot=args.snapshot if args.snapshot is not None else manifest.build.snapshot,
            output_dir=output_dir,
            platform=args.platform or manifest.build.platform,
            architecture=args.architecture or manifest.build.architecture,
        )

        os.makedirs(target.output_dir, exist_ok=True)

        build_recorder = BuildRecorder(target)

        logging.info(f"Building {manifest.build.name} ({target.architecture}) into {target.output_dir}")

        for component in manifest.components.select(focus=args.component, platform=target.platform):
            logging.info(f"Building {component.name}")

            builder = Builders.builder_from(component, target)
            try:
                builder.checkout(work_dir.name)
                builder.build(build_recorder)
                builder.export_artifacts(build_recorder)
            except:
                logging.error(f"Error building {component.name}, retry with: {args.component_command(component.name)}")
                raise

        build_recorder.write_manifest()

    logging.info("Done.")


if __name__ == "__main__":
    sys.exit(main())
