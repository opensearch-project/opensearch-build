#!/usr/bin/env python

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import tempfile
import uuid
import uuid
from system.arch import current_arch
from manifests.input_manifest import InputManifest
from build_workflow.build_recorder import BuildRecorder
from build_workflow.builder import Builder
from build_workflow.build_args import BuildArgs
from paths.script_finder import ScriptFinder
from git.git_repository import GitRepository

args = BuildArgs()

component_scripts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scripts/bundle-build/components')
default_scripts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scripts/bundle-build/standard-gradle-build')
script_finder = ScriptFinder(component_scripts_path, default_scripts_path)

arch = current_arch()
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

        if args.component and args.component != component.name:
            print(f'\nSkipping {component.name}')
            continue

        print(f'\nBuilding {component.name}')
        repo = GitRepository(component.repository, component.ref)

        try:
            builder = Builder(component.name, repo, script_finder, build_recorder)
            builder.build(manifest.build.version, arch, args.snapshot)
            builder.export_artifacts()
        except:
            print(f'\nError building {component.name}, retry with\n\n\t{args.component_command(component.name)}\n')
            raise

    build_recorder.write_manifest(output_dir)

print('Done.')
