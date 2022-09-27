# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import logging
import os
import re
from abc import abstractmethod
from typing import Dict, List, Type, Union

import ruamel.yaml

from manifests.input_manifest import InputComponents, InputManifest
from manifests.manifests import Manifests
from manifests_workflow.component_opensearch import ComponentOpenSearch
from manifests_workflow.component_opensearch_dashboards_min import ComponentOpenSearchDashboardsMin
from manifests_workflow.component_opensearch_min import ComponentOpenSearchMin
from system.temporary_directory import TemporaryDirectory


class InputManifests(Manifests):
    def __init__(self, name: str) -> None:
        self.name = name
        self.prefix = name.lower().replace(" ", "-")
        super().__init__(InputManifest, InputManifests.files(self.prefix))

    @classmethod
    def manifests_path(self) -> str:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "manifests"))

    @classmethod
    def workflows_path(self) -> str:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", ".github", "workflows"))

    @classmethod
    def legacy_manifests_path(self) -> str:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "legacy-manifests"))

    @classmethod
    def jenkins_path(self) -> str:
        return os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "..", "jenkins"))

    @classmethod
    def cron_jenkinsfile(self) -> str:
        return os.path.join(self.jenkins_path(), "check-for-build.jenkinsfile")

    @classmethod
    def versionincrement_workflow(self) -> str:
        return os.path.join(self.workflows_path(), "increment-plugin-versions.yml")

    @classmethod
    def files(self, name: str) -> List:
        results = []
        for path in [self.manifests_path(), self.legacy_manifests_path()]:
            for filename in glob.glob(os.path.join(path, f"**/{name}-*.yml")):
                # avoids the -maven manifest
                match = re.search(rf"^{name}-([0-9.]*).yml$", os.path.basename(filename))
                if match:
                    results.append(filename)
        return results

    @abstractmethod
    def update(
        self,
        min_klass: Union[Type[ComponentOpenSearchMin], Type[ComponentOpenSearchDashboardsMin]],
        component_klass: Type[ComponentOpenSearch],
        keep: bool = False,
    ) -> None:
        known_versions = self.versions
        logging.info(f"Known versions: {known_versions}")
        main_versions: Dict = {}
        with TemporaryDirectory(keep=keep, chdir=True) as work_dir:
            logging.info(f"Checking out components into {work_dir.name}")

            # check out and build #main, 1.x, etc.
            branches = min_klass.branches()

            logging.info(f"Checking {self.name} {branches} branches")
            for branch in branches:
                c = min_klass.checkout(
                    path=os.path.join(work_dir.name, self.name.replace(" ", ""), branch),
                    branch=branch,
                )

                version = c.version
                logging.info(f"{self.name}#{branch} is version {version}")
                if version not in main_versions.keys():
                    main_versions[version] = [c]

            if component_klass is not None:
                # components can increment their own version first without incrementing min
                manifest = self.latest
                logging.info(f"Examining components in the latest manifest of {manifest.build.name} ({manifest.build.version})")
                for component in manifest.components.values():
                    if component.name == self.name:
                        continue

                    logging.info(f"Checking out {component.name}#main")
                    component = component_klass.checkout(
                        name=component.name,
                        path=os.path.join(work_dir.name, component.name),
                        opensearch_version=manifest.build.version,
                        branch="main",
                    )

                    component_version = component.version
                    if component_version:
                        release_version = ".".join(component_version.split(".")[:3])
                        if release_version not in main_versions.keys():
                            main_versions[release_version] = []
                        main_versions[release_version].append(component)
                        logging.info(f"{component.name}#main is version {release_version} (from {component_version})")

            # summarize
            logging.info("Found versions on main:")
            for main_version in main_versions.keys():
                for component in main_versions[main_version]:
                    logging.info(f" {component.name}={main_version}")

            # generate new manifests
            for release_version in sorted(main_versions.keys() - known_versions):
                self.write_manifest(release_version, main_versions[release_version])
                self.add_to_cron(release_version)
                self.add_to_versionincrement_workflow(release_version)

    def create_manifest(self, version: str, components: List = []) -> InputManifest:
        templates_base_path = os.path.join(self.manifests_path(), "templates")
        template_version_folder = version.split(".")[0] + ".x"
        template_full_path = os.path.join(templates_base_path, self.prefix, template_version_folder, "manifest.yml")
        if not os.path.exists(template_full_path):
            template_full_path = os.path.join(templates_base_path, self.prefix, "default", "manifest.yml")

        manifest = InputManifest.from_file(open(template_full_path))

        manifest.build.version = version
        manifests_components = []

        for component in components:
            logging.info(f" Adding {component.name}")
            manifests_components.append(component.to_dict())

        manifest.components = InputComponents(manifests_components)  # type: ignore
        return manifest

    def write_manifest(self, version: str, components: List = []) -> None:
        logging.info(f"Creating new version: {version}")
        manifest = self.create_manifest(version, components)
        manifest_dir = os.path.join(self.manifests_path(), version)
        os.makedirs(manifest_dir, exist_ok=True)
        manifest_path = os.path.join(manifest_dir, f"{self.prefix}-{version}.yml")
        manifest.to_file(manifest_path)
        logging.info(f"Wrote {manifest_path}")

    def add_to_cron(self, version: str) -> None:
        logging.info(f"Adding new version to cron: {version}")
        jenkinsfile = self.cron_jenkinsfile()
        with open(jenkinsfile, "r") as f:
            data = f.read()

        cron_entry = f"H 1 * * * %INPUT_MANIFEST={version}/{self.prefix}-{version}.yml;TARGET_JOB_NAME=distribution-build-{self.prefix}\n"

        if cron_entry in data:
            raise ValueError(f"{jenkinsfile} already contains an entry for {self.prefix} {version}")

        data = data.replace("parameterizedCron '''\n", f"parameterizedCron '''\n{' ' * 12}{cron_entry}")

        with open(jenkinsfile, "w") as f:
            f.write(data)

        logging.info(f"Wrote {jenkinsfile}")

    def add_to_versionincrement_workflow(self, version: str) -> None:
        versionincrement_workflow_file = self.versionincrement_workflow()
        yaml = ruamel.yaml.YAML()
        yaml.explicit_start = True  # type: ignore
        yaml.preserve_quotes = True  # type: ignore

        with open(versionincrement_workflow_file) as f:
            data = yaml.load(f)

        version_entry = []
        major_version_entry = version.split(".")[0] + ".x"
        minor_version_entry = version.rsplit(".", 1)[0]
        if minor_version_entry not in data["jobs"]["plugin-version-increment-sync"]["strategy"]["matrix"]["branch"]:
            print(f"Adding {minor_version_entry} to {versionincrement_workflow_file}")
            version_entry.append(minor_version_entry)
        if major_version_entry not in data["jobs"]["plugin-version-increment-sync"]["strategy"]["matrix"]["branch"]:
            print(f"Adding {major_version_entry} to {versionincrement_workflow_file}")
            version_entry.append(major_version_entry)

        if version_entry:
            branch_list = list(data["jobs"]["plugin-version-increment-sync"]["strategy"]["matrix"]["branch"])
            branch_list.extend(version_entry)
            data["jobs"]["plugin-version-increment-sync"]["strategy"]["matrix"]["branch"] = branch_list
            yaml.indent(mapping=2, sequence=4, offset=2)
            with open(versionincrement_workflow_file, 'w') as f:
                yaml.dump(data, f)
            logging.info("Added new version to the version increment workflow")
