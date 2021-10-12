# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from manifests.input_manifest import InputManifest
from manifests_workflow.component_opensearch_dashboards_min import \
    ComponentOpenSearchDashboardsMin
from manifests_workflow.input_manifests import InputManifests
from system.temporary_directory import TemporaryDirectory


class InputManifestsOpenSearchDashboards(InputManifests):
    @classmethod
    def files(self):
        return InputManifests.files("opensearch-dashboards")

    def update(self, keep=False):
        known_versions = self.versions
        logging.info(f"Known versions: {known_versions}")
        main_versions = {}
        with TemporaryDirectory(keep=keep) as work_dir:
            logging.info(f"Checking out components into {work_dir}")
            os.chdir(work_dir)

            # check out OpenSearch Dashboards#main, 1.x, etc.
            branches = ComponentOpenSearchDashboardsMin.branches()
            logging.info(f"Checking OpenSearch Dashboards {branches} branches")
            for branch in branches:
                c = ComponentOpenSearchDashboardsMin.checkout(
                    path=os.path.join(work_dir, f"OpenSearch-Dashboards/{branch}"),
                    branch=branch,
                )
                version = c.version
                logging.info(f"OpenSearch-Dashboards#{branch} is version {version}")
                if version not in main_versions.keys():
                    main_versions[version] = [c]

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
                    "build": {
                        "name": "OpenSearch Dashboards",
                        "version": release_version,
                    },
                    "components": [],
                }
                for component in main_versions[release_version]:
                    logging.info(f" Adding {component.name}")
                    data["components"].append(component.to_dict())

                manifest = InputManifest(data)
                manifest_dir = os.path.join(self.manifests_path(), release_version)
                os.makedirs(manifest_dir, exist_ok=True)
                manifest_path = os.path.join(
                    manifest_dir, f"opensearch-dashboards-{release_version}.yml"
                )
                manifest.to_file(manifest_path)
                logging.info(f"Wrote {manifest_path}")
