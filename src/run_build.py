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

from build_workflow.build_args import BuildArgs
from build_workflow.build_recorder import BuildRecorder
from build_workflow.build_target import BuildTarget
from build_workflow.builders import Builders
from manifests.input_manifest import InputManifest
from paths.build_output_dir import BuildOutputDir
from system import console
from system.temporary_directory import TemporaryDirectory


def main() -> int:
    args = BuildArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)

    if args.ref_manifest:
        manifest = manifest.stable()
        if os.path.exists(args.ref_manifest):
            if manifest == InputManifest.from_path(args.ref_manifest):
                logging.info(f"No changes since {args.ref_manifest}")
            else:
                logging.info(f"Updating {args.ref_manifest}")
                manifest.to_file(args.ref_manifest)
        else:
            logging.info(f"Creating {args.ref_manifest}")
            manifest.to_file(args.ref_manifest)
        return 0

    output_dir = BuildOutputDir(manifest.build.filename, args.distribution).dir

    with TemporaryDirectory(keep=args.keep, chdir=True) as work_dir:
        logging.info(f"Building in {work_dir.name}")

        target = BuildTarget(
            name=manifest.build.name,
            version=manifest.build.version,
            qualifier=manifest.build.qualifier,
            patches=manifest.build.patches,
            snapshot=args.snapshot if args.snapshot is not None else manifest.build.snapshot,
            output_dir=output_dir,
            distribution=args.distribution,
            platform=args.platform or manifest.build.platform,
            architecture=args.architecture or manifest.build.architecture,
        )

        build_recorder = BuildRecorder(target)

        logging.info(f"Building {manifest.build.name} ({target.architecture}) into {target.output_dir}")

        for component in manifest.components.select(focus=args.components, platform=target.platform):
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
