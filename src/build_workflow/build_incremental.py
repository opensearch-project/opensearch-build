# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from typing import List

from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputManifest


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
