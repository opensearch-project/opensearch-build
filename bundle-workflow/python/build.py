#!/usr/bin/env python
# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import sys
import subprocess
import tempfile
from manifests.input_manifest import InputManifest
from build_workflow.build_recorder import BuildRecorder
from build_workflow.builder import Builder
from build_workflow.git_repository import GitRepository

if (len(sys.argv) < 2):
    print("Build an OpenSearch Bundle")
    print("usage: build.sh /path/to/manifest")
    exit(1)

component_scripts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scripts/bundle-build/components')
default_build_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scripts/bundle-build/standard-gradle-build/build.sh')

def get_arch():
    arch = subprocess.check_output(['uname', '-m']).decode().strip()
    if arch == 'x86_64':
        return 'x64'
    elif arch == 'aarch64' or arch == 'arm64':
        return  'arm64'
    else:
        raise ValueError(f'Unsupported architecture: {arch}')

arch = get_arch()
manifest = InputManifest.from_file(sys.argv[1])
output_dir = os.path.join(os.getcwd(), 'artifacts')
os.makedirs(output_dir, exist_ok = True)

with tempfile.TemporaryDirectory() as work_dir:
    print(f'Building in {work_dir}')

    os.chdir(work_dir)

    build_recorder = BuildRecorder(output_dir, manifest.build.name, manifest.build.version, arch)

    print(f'Building {manifest.build.name} ({arch}) into {output_dir}')

    for component in manifest.components:
        print(f'Building {component.name}')
        repo = GitRepository(component.repository, component.ref)
        builder = Builder(component.name,
                          repo,
                          component_scripts_path,
                          default_build_path,
                          build_recorder)
        builder.build(manifest.build.version, arch)
        builder.export_artifacts()

    build_recorder.write_manifest(output_dir)

print('Done')
