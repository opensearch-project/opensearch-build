# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from manifests_workflow.component_opensearch_dashboards_min import \
    ComponentOpenSearchDashboardsMin
from manifests_workflow.input_manifests import InputManifests
from system.temporary_directory import TemporaryDirectory


class InputManifestsOpenSearchDashboards(InputManifests):
    def __init__(self):
        super().__init__("OpenSearch Dashboards")

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
                self.write_manifest(release_version, main_versions[release_version])
