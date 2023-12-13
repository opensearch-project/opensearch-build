# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from typing import List

from build_workflow.build_args import BuildArgs
from build_workflow.build_recorder import BuildRecorder
from build_workflow.build_target import BuildTarget
from build_workflow.builders import Builders
from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputManifest
from paths.build_output_dir import BuildOutputDir
from system.temporary_directory import TemporaryDirectory


class BuildIncremental:
    def __init__(self, input_manifest: InputManifest, distribution: str):
        self.distribution = distribution
        self.input_manifest = input_manifest

    # Given input manifest and return a list of what components changed and added.
    def commits_diff(self, input_manifest: InputManifest) -> List[str]:
        build_manifest_path = os.path.join(self.distribution, "builds", input_manifest.build.filename, "manifest.yml")
        if not os.path.exists(build_manifest_path):
            logging.info("Previous build manifest does not exist. Rebuilding Core.")
            return [input_manifest.build.name.replace(" ", "-")]
        previous_build_manifest = BuildManifest.from_path(build_manifest_path)
        stable_input_manifest = input_manifest.stable()
        if previous_build_manifest.build.version != stable_input_manifest.build.version:
            logging.info("The version of previous build manifest doesn't match the current input manifest. Rebuilding Core.")
            return [input_manifest.build.name.replace(" ", "-")]
        components = []
        for component in stable_input_manifest.components.select():
            if component.name not in previous_build_manifest.components:
                components.append(component.name)
                logging.info(f"Adding {component.name} since it is missing from previous build manifest")
                continue
            if component.ref != previous_build_manifest.components[component.name].commit_id:  # type: ignore[attr-defined]
                components.append(component.name)
                logging.info(f"Adding {component.name} because it has different commit ID and needs to be rebuilt.")
                continue
        return components

    # Given updated plugins and look into the depends_on of all components to finalize a list of rebuilding components.
    def rebuild_plugins(self, changed_plugins: List, input_manifest: InputManifest) -> List[str]:
        if not changed_plugins:
            return []

        if any(core in changed_plugins for core in ("OpenSearch", "OpenSearch-Dashboards")):
            logging.info("Core engine has new changes, rebuilding all components.")
            return [component.name for component in input_manifest.components.select()]

        queue = changed_plugins
        rebuild_list = []

        rebuild_list.append("OpenSearch-Dashboards") if input_manifest.build.filename == "opensearch-dashboards" else rebuild_list
        while queue:
            plugin = queue.pop(0)
            rebuild_list.append(plugin) if plugin not in rebuild_list else rebuild_list
            for dependent_plugin in input_manifest.plugins_depend_on(plugin):
                queue.append(dependent_plugin) if dependent_plugin not in rebuild_list else queue

        logging.info(f"Rebuilding list is {rebuild_list}")
        return rebuild_list

    def build_incremental(self, args: BuildArgs, input_manifest: InputManifest, components: List) -> None:
        build_manifest_path = os.path.join(self.distribution, "builds", input_manifest.build.filename, "manifest.yml")
        if not os.path.exists(build_manifest_path):
            logging.error("Previous build manifest is not exists. Throw error.")

        logging.info(f"Build {components} incrementally.")

        build_manifest_data = BuildManifest.from_path(build_manifest_path).__to_dict__()

        output_dir = BuildOutputDir(input_manifest.build.filename, args.distribution).dir
        failed_plugins = []

        with TemporaryDirectory(keep=args.keep, chdir=True) as work_dir:
            logging.info(f"Building in {work_dir.name}")
            target = BuildTarget(
                name=input_manifest.build.name,
                version=input_manifest.build.version,
                qualifier=input_manifest.build.qualifier,
                patches=input_manifest.build.patches,
                snapshot=args.snapshot if args.snapshot is not None else input_manifest.build.snapshot,
                output_dir=output_dir,
                distribution=args.distribution,
                platform=args.platform or input_manifest.build.platform,
                architecture=args.architecture or input_manifest.build.architecture,
            )

            build_recorder_incremental = BuildRecorder(target, build_manifest_data)

            logging.info(f"Building {input_manifest.build.name} ({target.architecture}) into {target.output_dir}")

            for component in input_manifest.components.select(focus=components, platform=target.platform):
                logging.info(f"Rebuilding {component.name}")

                builder = Builders.builder_from(component, target)
                try:
                    builder.checkout(work_dir.name)
                    builder.build(build_recorder_incremental)
                    builder.export_artifacts(build_recorder_incremental)
                    logging.info(f"Successfully built {component.name}")
                except:
                    logging.error(f"Error building {component.name}, retry with: {args.component_command(component.name)}")
                    if args.continue_on_error and component.name not in ['OpenSearch', 'job-scheduler', 'common-utils', 'OpenSearch-Dashboards']:
                        failed_plugins.append(component.name)
                        continue
                    else:
                        raise

            build_recorder_incremental.write_manifest()

        if len(failed_plugins) > 0:
            logging.error(f"Failed plugins are {failed_plugins}")
        logging.info("Done.")
