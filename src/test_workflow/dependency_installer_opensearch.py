# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from test_workflow.dependency_installer import DependencyInstaller


class DependencyInstallerOpenSearch(DependencyInstaller):

    def __init__(self, root_url: str, build_manifest: BuildManifest, bundle_manifest: BundleManifest) -> None:
        super().__init__(root_url, build_manifest, bundle_manifest)

    @property
    def maven_local_path(self) -> str:
        return os.path.join(os.path.expanduser("~"), ".m2", "repository")

    def install_maven_dependencies(self) -> None:
        for component in self.build_manifest.components.values():
            maven_artifacts = component.artifacts.get("maven", None)
            if maven_artifacts:
                self.download(maven_artifacts, "builds", self.maven_local_path)

    def install_build_dependencies(self, dependency_dict: dict, dest: str) -> None:
        """
        Downloads the build dependencies from S3 and puts them on the given custom path
        for each dependency in the dependencies.

        :param dependencies: dictionary of dependency names with version for which the build artifacts need to be downloaded.
        Example: {'opensearch-job-scheduler':'1.1.0.0'}
        """
        os.makedirs(dest, exist_ok=True)
        for dependency, version in dependency_dict.items():
            path = f"{self.root_url}/builds/opensearch/plugins/{dependency}-{version}.zip"
            local_path = os.path.join(dest, f"{dependency}-{version}.zip")
            self.download_or_copy(path, local_path)
