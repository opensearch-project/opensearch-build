#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import os
import shutil
import tempfile

from assemble_workflow.bundle import Bundle
from assemble_workflow.bundle_recorder import BundleRecorder
from manifests.build_manifest import BuildManifest

parser = argparse.ArgumentParser(description="Assemble an OpenSearch Bundle")
parser.add_argument("manifest", type=argparse.FileType("r"), help="Manifest file.")
args = parser.parse_args()

tarball_installation_script = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../../release/tar/linux/opensearch-tar-install.sh",
)
if not os.path.isfile(tarball_installation_script):
    print(f"No installation script found at path: {tarball_installation_script}")
    exit(1)

build_manifest = BuildManifest.from_file(args.manifest)
build = build_manifest.build
artifacts_dir = os.path.dirname(os.path.realpath(args.manifest.name))
output_dir = os.path.join(os.getcwd(), "bundle")
os.makedirs(output_dir, exist_ok=True)

with tempfile.TemporaryDirectory() as work_dir:
    print(f"Bundling {build.name} ({build.architecture}) into {output_dir} ...")

    os.chdir(work_dir)

    bundle_recorder = BundleRecorder(build, output_dir, artifacts_dir)
    bundle = Bundle(build_manifest, artifacts_dir, bundle_recorder)

    bundle.install_plugins()
    print(f"Installed plugins: {bundle.installed_plugins}")

    # Copy the tar installation script into the bundle
    shutil.copyfile(
        tarball_installation_script,
        os.path.join(
            bundle.archive_path, os.path.basename(tarball_installation_script)
        ),
    )

    #  Save a copy of the manifest inside of the tar
    bundle_recorder.write_manifest(bundle.archive_path)
    bundle.build_tar(output_dir)

    bundle_recorder.write_manifest(output_dir)

print("Done.")
