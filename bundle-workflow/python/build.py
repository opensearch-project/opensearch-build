#!/usr/bin/env python

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
import tempfile
import uuid
import argparse
from manifests.input_manifest import InputManifest
from build_workflow.build_recorder import BuildRecorder
from build_workflow.builder import Builder
from build_workflow.git_repository import GitRepository
from paths.script_finder import ScriptFinder

parser = argparse.ArgumentParser(description = "Build an OpenSearch Bundle")
parser.add_argument('manifest', type = argparse.FileType('r'), help="Manifest file.")
parser.add_argument('-s', '--snapshot', action = 'store_true', default = False, help="Build snapshot.")
args = parser.parse_args()

component_scripts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scripts/bundle-build/components')
default_scripts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scripts/bundle-build/standard-gradle-build')
script_finder = ScriptFinder(component_scripts_path, default_scripts_path)

def get_arch():
    arch = subprocess.check_output(['uname', '-m']).decode().strip()
    if arch == 'x86_64':
        return 'x64'
    elif arch == 'aarch64' or arch == 'arm64':
        return  'arm64'
    else:
        raise ValueError(f'Unsupported architecture: {arch}')

arch = get_arch()
manifest = InputManifest.from_file(args.manifest)
output_dir = os.path.join(os.getcwd(), 'artifacts')
os.makedirs(output_dir, exist_ok = True)
build_id = os.getenv('OPENSEARCH_BUILD_ID', uuid.uuid4().hex)

with tempfile.TemporaryDirectory() as work_dir: 
    print(f'Building in {work_dir}')

    os.chdir(work_dir)

    build_recorder = BuildRecorder(build_id, output_dir, manifest.build.name, manifest.build.version, arch, args.snapshot)

    print(f'Building {manifest.build.name} ({arch}) into {output_dir}')

    for component in manifest.components:
        print(f'Building {component.name}')
        repo = GitRepository(component.repository, component.ref)
        builder = Builder(component.name,
                          repo,
                          script_finder,
                          build_recorder)
        builder.build(manifest.build.version, arch, args.snapshot)
        builder.export_artifacts()

    build_recorder.write_manifest(output_dir)

print('Done.')
