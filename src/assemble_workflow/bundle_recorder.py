# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from typing import Any, Dict

from assemble_workflow.bundle_location import BundleLocation
from assemble_workflow.dists import Dists
from manifests.build_manifest import BuildComponent, BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.manifest import Manifest


class BundleRecorder:

    def __init__(self, build: BuildManifest.Build, output_dir: str, artifacts_dir: str, bundle_location: BundleLocation) -> None:
        self.output_dir = output_dir
        self.build_id = build.id
        self.bundle_location = bundle_location
        self.version = build.version
        self.distribution = build.distribution
        self.package_name = self.__get_package_name(build)
        self.artifacts_dir = artifacts_dir
        self.architecture = build.architecture
        self.bundle_manifest = self.BundleManifestBuilder(
            build.id,
            build.name,
            build.version,
            build.platform,
            build.architecture,
            build.distribution,
            self.__get_package_location(),
        )

    def __get_package_name(self, build: BuildManifest.Build) -> str:
        parts = [
            build.filename,
            build.version,
            build.platform,
            build.architecture,
        ]
        extension = Dists.DISTRIBUTIONS_MAP[self.distribution].extension if self.distribution else Dists.DISTRIBUTIONS_MAP['tar'].extension
        return "-".join(parts) + extension

    # Assembled output are expected to be served from a separate "dist" folder
    # Example: https://ci.opensearch.org/ci/dbc/bundle-build/1.2.0/build-id/linux/x64/dist/
    def __get_package_location(self) -> str:
        return self.bundle_location.get_bundle_location(self.package_name)

    # Build artifacts are expected to be served from a "builds" folder
    # Example: https://ci.opensearch.org/ci/dbc/bundle-build/1.2.0/build-id/linux/x64/builds/
    def __get_component_location(self, component_rel_path: str) -> str:
        return self.bundle_location.get_build_location(component_rel_path) if component_rel_path else None

    def record_component(self, component: BuildComponent, rel_path: str = None) -> None:
        self.bundle_manifest.append_component(
            component.name,
            component.repository,
            component.ref,
            component.commit_id,
            self.__get_component_location(rel_path),
        )

    def get_manifest(self) -> BundleManifest:
        return self.bundle_manifest.to_manifest()

    def write_manifest(self, folder: str) -> None:
        manifest_path = os.path.join(folder, "manifest.yml")
        self.get_manifest().to_file(manifest_path)

    class BundleManifestBuilder:
        def __init__(self, build_id: str, name: str, version: str, platform: str, architecture: str, distribution: str, location: str) -> None:
            self.data: Dict[str, Any] = {}
            self.data["build"] = {}
            self.data["build"]["id"] = build_id
            self.data["build"]["name"] = name
            self.data["build"]["version"] = str(version)
            self.data["build"]["platform"] = platform
            self.data["build"]["architecture"] = architecture
            self.data["build"]["distribution"] = distribution if distribution else "tar"
            self.data["build"]["location"] = location
            self.data["schema-version"] = "1.1"
            # We need to store components as a hash so that we can append artifacts by component name
            # When we convert to a BundleManifest this will get converted back into a list
            self.data["components"] = []

        def append_component(self, name: str, repository_url: str, ref: str, commit_id: str, location: str = None) -> None:
            component = Manifest.compact({
                "name": name,
                "repository": repository_url,
                "ref": ref,
                "commit_id": commit_id,
                "location": location,
            })
            self.data["components"].append(component)

        def to_manifest(self) -> BundleManifest:
            return BundleManifest(self.data)
