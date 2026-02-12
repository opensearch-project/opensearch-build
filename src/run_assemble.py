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
import platform
import yaml

from assemble_workflow.assemble_args import AssembleArgs
from assemble_workflow.bundle_locations import BundleLocations
from assemble_workflow.bundle_recorder import BundleRecorder
from assemble_workflow.bundles import Bundles
from manifests.build_manifest import BuildManifest
from paths.assemble_output_dir import AssembleOutputDir
from system import console

def generate_manifest_file(args: AssembleArgs):
    component = args.component or "opensearch"
    platform_name = args.platform or platform.system().lower()
    arch = args.arch or platform.machine().lower()
    version = args.version or "0.0.1"
    dist = args.dist or "tar"

    url = f"https://artifacts.opensearch.org/releases/bundle/{component}/{version}/{component}-{version}-{platform_name}-{arch}.{dist}"

    manifest_content = {
        "build": {
            "name": component,
            "version": version,
            "platform": platform_name,
            "architecture": arch,
            "distribution": dist
        },
        "components": [
            {
                "name": component,
                "version": version,
                "url": url
            }
        ]
    }

    with open(args.generate_manifest, "w") as f:
        yaml.dump(manifest_content, f)
        print(f"Generated manifest file: {args.generate_manifest}")


def main() -> int:
    args = AssembleArgs()

    if args.generate_manifest:
        generate_manifest_file(args)
        return 0

    console.configure(level=args.logging_level)

    if args.dry_run:
        print("Dry-run enabled. Skipping actual download or extraction.")
        if args.manifest:
            print(f"Manifest file: {args.manifest.name}")
        else:
            print("No manifest file provided.")
        return 0


    build_manifest = BuildManifest.from_file(args.manifest)
    build = build_manifest.build
    artifacts_dir = os.path.dirname(os.path.realpath(args.manifest.name))

    output_dir = AssembleOutputDir(build.filename, build.distribution).dir

    logging.info(f"Bundling {build.name} ({build.architecture}) on {build.platform} into {output_dir} ...")

    bundle_recorder = BundleRecorder(
        build,
        output_dir,
        artifacts_dir,
        BundleLocations.from_path(args.base_url, os.getcwd(), build.filename, build.distribution)
    )

    with Bundles.create(build_manifest, artifacts_dir, bundle_recorder, args.keep) as bundle:
        bundle.install_min()
        bundle.install_components()
        logging.info(f"Installed plugins: {bundle.installed_plugins}")

        #  Save a copy of the manifest inside of the tar
        bundle_recorder.write_manifest(bundle.min_dist.archive_path)
        bundle.package(output_dir)

        bundle_recorder.write_manifest(output_dir)

    logging.info("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
