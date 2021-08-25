#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import os

from manifests.build_manifest import BuildManifest
from signing_workflow.signer import Signer

parser = argparse.ArgumentParser(description="Sign artifacts")
parser.add_argument(
    "manifest", type=argparse.FileType("r"), help="Path to local manifest file."
)
parser.add_argument("--component", nargs="?", help="Component name")
parser.add_argument("--type", nargs="?", help="Artifact type")
args = parser.parse_args()

manifest = BuildManifest.from_file(args.manifest)
basepath = os.path.dirname(os.path.abspath(args.manifest.name))
signer = Signer()

for component in manifest.components:

    if args.component and args.component != component.name:
        print(f"\nSkipping {component.name}")
        continue

    print(f"\nSigning {component.name}")
    for artifact_type in component.artifacts:

        if args.type and args.type != artifact_type:
            continue

        signer.sign(component.artifacts[artifact_type])

print("Done.")
