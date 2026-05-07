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
import threading
import uuid

from build_workflow.build_args import BuildArgs
from build_workflow.build_graph import BuildGraph
from build_workflow.build_incremental import BuildIncremental
from build_workflow.build_recorder import BuildRecorder
from build_workflow.build_target import BuildTarget
from build_workflow.builders import Builders
from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputManifest
from paths.build_output_dir import BuildOutputDir
from system import console
from system.temporary_directory import TemporaryDirectory

CRITICAL_COMPONENTS = ['OpenSearch', 'job-scheduler', 'common-utils', 'OpenSearch-Dashboards']


def main() -> int:
    args = BuildArgs()
    console.configure(level=args.logging_level)
    manifest = InputManifest.from_file(args.manifest)
    build_manifest = None
    components = args.components
    failed_plugins = []

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

    if args.incremental:
        buildIncremental = BuildIncremental(manifest, args.distribution, args.platform)
        list_of_updated_plugins = buildIncremental.commits_diff(manifest)
        components = buildIncremental.rebuild_plugins(list_of_updated_plugins, manifest)

        build_manifest_path = os.path.join(args.distribution, "builds", manifest.build.filename, "manifest.yml")
        if not os.path.exists(build_manifest_path):
            logging.error(f"Previous build manifest missing at path: {build_manifest_path}")
        build_manifest = BuildManifest.from_path(build_manifest_path)

        if not components:
            logging.info("No commit difference found between any components. Skipping the build.")
            build_manifest.build.id = os.getenv("BUILD_NUMBER") or uuid.uuid4().hex
            build_manifest.to_file(build_manifest_path)
            logging.info(f"Updating the build ID in the build manifest to {build_manifest.build.id}.")
            return 0

        logging.info(f"Plugins for incremental build: {components}")

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
            skip_artifact_check=args.skip_artifact_check,
        )

        build_recorder = BuildRecorder(target, build_manifest) if args.incremental else BuildRecorder(target)

        logging.info(f"Building {manifest.build.name} ({target.architecture}) into {target.output_dir}")

        if args.parallel:
            failed_plugins = _build_parallel(manifest, target, build_recorder, work_dir.name, args, components)
        else:
            for component in manifest.components.select(focus=components, platform=target.platform):
                logging.info(f"Building {component.name}")

                builder = Builders.builder_from(component, target)
                try:
                    builder.checkout(work_dir.name)
                    builder.build(build_recorder)
                    builder.export_artifacts(build_recorder)
                    logging.info(f"Successfully built {component.name}")
                except Exception as e:
                    logging.error(f"ERROR: {e}")
                    logging.error(f"Error building {component.name}, retry with: {args.component_command(component.name)}")
                    if args.continue_on_error and component.name not in CRITICAL_COMPONENTS:
                        failed_plugins.append(component.name)
                        continue
                    else:
                        raise

        build_recorder.write_manifest()
    if len(failed_plugins) > 0:
        logging.error(f"Failed plugins are {failed_plugins}")
    logging.info("Done.")
    return 0


def _build_parallel(manifest: InputManifest, target: BuildTarget, build_recorder: BuildRecorder, work_dir: str, args: BuildArgs, components: list) -> list:
    recorder_lock = threading.Lock()

    selected_components = list(manifest.components.select(focus=components, platform=target.platform))
    component_map = {c.name: c for c in selected_components}
    selected_names = set(component_map.keys())

    # OpenSearch core must build first — it publishes build-tools and artifacts
    # to Maven local that ALL plugins depend on implicitly.
    core_name = manifest.build.name.replace(" ", "-")
    if core_name in component_map:
        core_component = component_map[core_name]
        logging.info(f"Building {core_component.name}")
        builder = Builders.builder_from(core_component, target)
        try:
            builder.checkout(work_dir)
            builder.build(build_recorder)
            builder.export_artifacts(build_recorder)
            logging.info(f"Successfully built {core_component.name}")
        except Exception as e:
            logging.error(f"ERROR: {e}")
            logging.error(f"Error building {core_component.name}, retry with: {args.component_command(core_component.name)}")
            raise

    # Now build remaining components in parallel
    remaining_components = [c for c in selected_components if c.name != core_name]

    graph = BuildGraph(max_workers=args.parallel)

    for component in remaining_components:
        deps = getattr(component, 'depends_on', None) or []
        graph.add_component(component.name, [d for d in deps if d in selected_names and d != core_name])

    def build_component(name: str) -> None:
        component = component_map[name]
        logging.info(f"Building {component.name}")

        builder = Builders.builder_from(component, target)
        builder.checkout(work_dir)
        builder.build(build_recorder)
        with recorder_lock:
            builder.export_artifacts(build_recorder)
        logging.info(f"Successfully built {component.name}")

    failed = graph.execute_parallel(
        build_fn=build_component,
        critical_components=CRITICAL_COMPONENTS,
        continue_on_error=args.continue_on_error,
    )

    if not args.continue_on_error:
        critical_failures = [f for f in failed if f in CRITICAL_COMPONENTS]
        if critical_failures:
            raise Exception(f"Critical component(s) failed: {critical_failures}")

    return [f for f in failed if f not in CRITICAL_COMPONENTS]


if __name__ == "__main__":
    sys.exit(main())
