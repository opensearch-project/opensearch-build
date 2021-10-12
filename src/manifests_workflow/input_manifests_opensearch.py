# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess

from manifests.input_manifest import InputManifest
from manifests_workflow.component_opensearch import ComponentOpenSearch
from manifests_workflow.component_opensearch_min import ComponentOpenSearchMin
from manifests_workflow.input_manifests import InputManifests
from system.temporary_directory import TemporaryDirectory


class InputManifestsOpenSearch(InputManifests):
    @classmethod
    def files(self):
        return InputManifests.files("opensearch")

    def update(self, keep=False):
        known_versions = self.versions
        logging.info(f"Known versions: {known_versions}")
        main_versions = {}
        with TemporaryDirectory(keep=keep) as work_dir:
            logging.info(f"Checking out components into {work_dir}")
            os.chdir(work_dir)

            # check out and build OpenSearch#main, 1.x, etc.
            branches = ComponentOpenSearchMin.branches()
            logging.info(f"Checking OpenSearch {branches} branches")
            for branch in branches:
                c = ComponentOpenSearchMin.checkout(
                    path=os.path.join(work_dir, f"OpenSearch/{branch}"), branch=branch
                )
                c.publish_to_maven_local()
                version = c.version
                logging.info(f"OpenSearch#{branch} is version {version}")
                if version not in main_versions.keys():
                    main_versions[version] = [c]

            # components can increment their own version first without incrementing min
            manifest = self.latest
            for component in manifest.components:
                if component.name == "OpenSearch":
                    continue

                logging.info(f"Checking out {component.name}#main")
                component = ComponentOpenSearch.checkout(
                    name=component.name,
                    path=os.path.join(work_dir, component.name),
                    version=manifest.build.version,
                    branch="main",
                )

                try:
                    component_version = component.version
                    if component_version:
                        release_version = ".".join(component_version.split(".")[:3])
                        if release_version not in main_versions.keys():
                            main_versions[release_version] = []
                        main_versions[release_version].append(component)
                        logging.info(
                            f"{component.name}#main is version {release_version} (from {component_version})"
                        )
                except subprocess.CalledProcessError as err:
                    logging.warn(
                        f"Error getting version of {component.name}: {str(err)}, ignored"
                    )

            # summarize
            logging.info("Found versions on main:")
            for main_version in main_versions.keys():
                for component in main_versions[main_version]:
                    logging.info(f" {component.name}={main_version}")

            # generate new manifests
            for release_version in sorted(main_versions.keys() - known_versions):
                logging.info(f"Creating new version: {release_version}")
                data = {
                    "schema-version": "1.0",
                    "build": {"name": "OpenSearch", "version": release_version},
                    "components": [],
                }
                # TODO: copy OpenSearch and common-utils from the previous manifest
                for component in main_versions[release_version]:
                    logging.info(f" Adding {component.name}")
                    data["components"].append(component.to_dict())

                manifest = InputManifest(data)
                manifest_dir = os.path.join(self.manifests_path(), release_version)
                os.makedirs(manifest_dir, exist_ok=True)
                manifest_path = os.path.join(
                    manifest_dir, f"opensearch-{release_version}.yml"
                )
                manifest.to_file(manifest_path)
                logging.info(f"Wrote {manifest_path}")
