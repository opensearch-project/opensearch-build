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
from packaging.version import Version
from packaging.version import parse as version_parse

from manifests.input_manifest import InputManifest
from manifests.manifests import Manifests
from manifests_workflow.component_opensearch import ComponentOpenSearch
from manifests_workflow.component_opensearch_dashboards_min import ComponentOpenSearchDashboardsMin
from manifests_workflow.component_opensearch_min import ComponentOpenSearchMin
from system.temporary_directory import TemporaryDirectory


class InputManifests(Manifests):
    BUILD_PLATFORM = {
        "opensearch": "linux macos windows",
        "opensearch-dashboards": "linux windows"
    }
    BUILD_DISTRIBUTION = {
        "opensearch": "tar rpm deb zip",
        "opensearch-dashboards": "tar rpm deb zip"
    }

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
    def os_versionincrement_workflow(self) -> str:
        return os.path.join(self.workflows_path(), "os-increment-plugin-versions.yml")

    @classmethod
    def osd_versionincrement_workflow(self) -> str:
        return os.path.join(self.workflows_path(), "osd-increment-plugin-versions.yml")

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
        known_versions = sorted(self.versions, key=version_parse)
        branch_versions: Dict = {}
        logging.info(f"Known versions: {known_versions}")
        with TemporaryDirectory(keep=keep, chdir=True) as work_dir:
            logging.info(f"Checking out components into {work_dir.name}")

            # ignore branches that are legacy/outdated and not maintained anymore
            # get possible legacy branches based on legacy manifests, then cross check with current branches from current manifests
            # ex: 1.0 failed due to certain dependencies not available anymore: https://github.com/avast/gradle-docker-compose-plugin/issues/446
            all_manifests = set(InputManifests.files(self.prefix))
            legacy_manifests = {m for m in all_manifests if "legacy-manifests" in m}
            legacy_branches = {".".join(m.split(os.sep)[-2].rsplit(".", 1)[:-1]) for m in legacy_manifests}
            current_manifests = all_manifests - legacy_manifests
            current_branches = {".".join(m.split(os.sep)[-2].rsplit(".", 1)[:-1]) for m in current_manifests}

            # make sure only branches in legacy-manifests but not in manifests get ignored
            legacy_branches -= current_branches

            # check out and build #main, 1.x, etc.
            all_branches = sorted(min_klass.branches())
            branches = [b for b in all_branches if not any(b == o or b.startswith((f"{o}-", f"{o}/")) for o in legacy_branches)]
            logging.info(f"Checking {self.name} {sorted(branches)} branches")
            logging.info(f"Ignoring {self.name} {sorted(set(all_branches) - set(branches))} branches as they are legacy")

            for branch in branches:
                min_component_klass = min_klass.checkout(
                    path=os.path.join(work_dir.name, self.name.replace(" ", ""), branch),
                    branch=branch,
                )

                version = min_component_klass.version
                logging.info(f"{self.name}#{branch} is version {version}")
                if version not in branch_versions:
                    branch_versions[version] = branch

            # generate new manifests
            new_versions = sorted(branch_versions.keys() - known_versions, key=version_parse)
            logging.info(f"New Versions: {new_versions}")
            for new_version_entry in new_versions:
                self.write_manifest(new_version_entry, branch_versions[new_version_entry], known_versions)
                self.add_to_cron(new_version_entry)
                self.add_to_versionincrement_workflow(new_version_entry)
                known_versions.append(new_version_entry)

    def create_manifest(self, version: str, branch: str, known_versions: List[str]) -> InputManifest:
        # If  : No known_versions manifests exist or new version smaller than the min(known_versions), create new manifests from the templates
        #       (1.0.0-3.0.0 based on template 1.x-3.x, 4.0.0+ from default.x, previous behavior)
        # Else: Create new manifests based on the latest version before the new version
        #       (2.12.1 from 2.12.0, 2.13.0 from 2.12.1, 3.0.0 from 2.13.0, 4.0.0 from 3.0.0, etc.)
        if not known_versions or Version(version) < Version(min(known_versions, key=version_parse)):
            logging.info("No previous version exist before {version}, create with templates")
            templates_base_path = os.path.join(self.manifests_path(), "templates")
            template_version_folder = version.split(".")[0] + ".x"
            template_full_path = os.path.join(templates_base_path, self.prefix, template_version_folder, "manifest.yml")
            if not os.path.exists(template_full_path):
                template_full_path = os.path.join(templates_base_path, self.prefix, "default", "manifest.yml")
        else:
            previous_versions = [v for v in known_versions if Version(v) < Version(version)]
            base_version = max(previous_versions, key=version_parse)
            logging.info(f"Base Version: {base_version} is the highest version before {version}")
            template_full_path = os.path.join(self.manifests_path(), base_version, f"{self.prefix}-{base_version}.yml")
            if not os.path.exists(template_full_path):
                template_full_path = os.path.join(self.legacy_manifests_path(), base_version, f"{self.prefix}-{base_version}.yml")

        logging.info(f"Using {template_full_path} as the base manifest")

        manifest = InputManifest.from_file(open(template_full_path))

        manifest.build.version = version

        for component in manifest.components.select():
            component.ref = branch  # type: ignore

        return manifest

    def write_manifest(self, version: str, branch: str, known_versions: List[str]) -> None:
        logging.info(f"Creating new version: {version}")
        manifest = self.create_manifest(version, branch, known_versions)
        manifest_dir = os.path.join(self.manifests_path(), version)
        os.makedirs(manifest_dir, exist_ok=True)
        manifest_path = os.path.join(manifest_dir, f"{self.prefix}-{version}.yml")
        manifest.to_file(manifest_path)
        logging.info(f"Wrote {manifest_path} as the new manifest")

    def add_to_cron(self, version: str) -> None:
        logging.info(f"Adding new version to cron: {version}")
        jenkinsfile = self.cron_jenkinsfile()
        with open(jenkinsfile, "r") as f:
            data = f.read()

        build_platform = self.BUILD_PLATFORM.get(self.prefix, "linux")
        build_distribution = self.BUILD_DISTRIBUTION.get(self.prefix, "tar")

        cron_entry = f"H 1 * * * %INPUT_MANIFEST={version}/{self.prefix}-{version}.yml;" \
                     f"TARGET_JOB_NAME=distribution-build-{self.prefix};" \
                     f"BUILD_PLATFORM={build_platform};" \
                     f"BUILD_DISTRIBUTION={build_distribution}\n"

        if cron_entry in data:
            raise ValueError(f"{jenkinsfile} already contains an entry for {self.prefix} {version}")

        data = data.replace("parameterizedCron '''\n", f"parameterizedCron '''\n{' ' * 12}{cron_entry}")

        with open(jenkinsfile, "w") as f:
            f.write(data)

        logging.info(f"Wrote {jenkinsfile}")

    def add_to_versionincrement_workflow(self, version: str) -> None:
        versionincrement_workflow_files = [self.os_versionincrement_workflow(), self.osd_versionincrement_workflow()]
        yaml = ruamel.yaml.YAML()
        yaml.explicit_start = True  # type: ignore
        yaml.preserve_quotes = True  # type: ignore

        for workflow_file in versionincrement_workflow_files:

            with open(workflow_file) as f:
                data = yaml.load(f)

            version_entry = []
            major_version_entry = version.split(".")[0] + ".x"
            minor_version_entry = version.rsplit(".", 1)[0]
            if minor_version_entry not in data["jobs"]["plugin-version-increment-sync"]["strategy"]["matrix"]["branch"]:
                logging.info(f"Adding {minor_version_entry} to {workflow_file}")
                version_entry.append(minor_version_entry)
            if major_version_entry not in data["jobs"]["plugin-version-increment-sync"]["strategy"]["matrix"]["branch"]:
                logging.info(f"Adding {major_version_entry} to {workflow_file}")
                version_entry.append(major_version_entry)

            if version_entry:
                branch_list = list(data["jobs"]["plugin-version-increment-sync"]["strategy"]["matrix"]["branch"])
                branch_list.extend(version_entry)
                data["jobs"]["plugin-version-increment-sync"]["strategy"]["matrix"]["branch"] = branch_list
                yaml.indent(mapping=2, sequence=4, offset=2)
                with open(workflow_file, 'w') as f:
                    yaml.dump(data, f)
                logging.info("Added new version to the version increment workflow")
