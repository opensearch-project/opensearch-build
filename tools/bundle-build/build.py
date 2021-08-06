# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import tempfile
import urllib.request
from lib.build_manifest import BuildManifest
from lib.build_output import BuildOutput

if (len(sys.argv) < 2):
    print("Build an OpenSearch Bundle")
    print("usage: build.sh /path/to/manifest")
    exit(1)

with tempfile.TemporaryDirectory() as work_dir:
    manifest = BuildManifest.from_file(sys.argv[1])
    build = manifest.build
    output = BuildOutput()

    print(f'Building {build.name} ({output.arch}) into {output.dest} ...')

    os.chdir(work_dir)

    for component in manifest.components:
        print(f'=== Building {component.name} ...')
        component.checkout()
        component.build(build.version, output.arch)
        component.export(output.dest)

    manifest_path = os.path.join(output.dest, 'manifest.yml')
    manifest.save_to(manifest_path)
    print(f'Done.')