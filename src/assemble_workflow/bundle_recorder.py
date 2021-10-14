# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from urllib.parse import urljoin
from manifests.bundle_manifest import BundleManifest
from assemble_workflow.public_urls import PublicURLpath

class BundleRecorder:
    def __init__(self, build, output_dir, artifacts_dir):
        self.output_dir = output_dir
        self.build_id = build.id
        self.version = build.version
        self.tar_name = self.__get_tar_name(build)
        self.artifacts_dir = artifacts_dir
        self.arch = build.architecture
        self.urls = PublicURLpath(build).urls_path
        self.bundle_manifest = self.BundleManifestBuilder(
            build.id,
            build.name,
            build.version,
            build.architecture,
            self.__get_tar_location(self.urls["bundles"]),
        )

    def __get_tar_name(self, build):
        parts = [build.name.lower().replace(" ", "-"), build.version, "linux", build.architecture]
        return "-".join(parts) + ".tar.gz"

    def __get_public_url_path(self, url_path, rel_path):
        return urljoin(url_path + "/", rel_path)

    def __get_location(self, url_path, rel_path, abs_path):
        if url_path:
            return self.__get_public_url_path(url_path, rel_path)
        return abs_path

    # Assembled bundles are expected to be served from a separate "bundles" folder
    # Example: https://artifacts.opensearch.org/bundles/1.0.0/<build-id
    def __get_tar_location(self, url_path):
        return self.__get_location(
            url_path, self.tar_name, os.path.join(self.output_dir, self.tar_name)
        )

    # Build artifacts are expected to be served from a "builds" folder
    # Example: https://artifacts.opensearch.org/builds/1.0.0/<build-id>
    def __get_component_location(self, component_rel_path, url_path):
        abs_path = os.path.join(self.artifacts_dir, component_rel_path)
        return self.__get_location(url_path, component_rel_path, abs_path)

    def record_component(self, component, rel_path):
        self.bundle_manifest.append_component(
            component.name,
            component.repository,
            component.ref,
            component.commit_id,
            self.__get_component_location(rel_path, self.urls["builds"]),
        )

    def get_manifest(self):
        return self.bundle_manifest.to_manifest()

    def write_manifest(self, folder):
        manifest_path = os.path.join(folder, "manifest.yml")
        self.get_manifest().to_file(manifest_path)

    class BundleManifestBuilder:
        def __init__(self, build_id, name, version, arch, location):
            self.data = {}
            self.data["build"] = {}
            self.data["build"]["id"] = build_id
            self.data["build"]["name"] = name
            self.data["build"]["version"] = str(version)
            self.data["build"]["architecture"] = arch
            self.data["build"]["location"] = location
            self.data["schema-version"] = "1.0"
            # We need to store components as a hash so that we can append artifacts by component name
            # When we convert to a BundleManifest this will get converted back into a list
            self.data["components"] = []

        def append_component(self, name, repository_url, ref, commit_id, location):
            component = {
                "name": name,
                "repository": repository_url,
                "ref": ref,
                "commit_id": commit_id,
                "location": location,
            }
            self.data["components"].append(component)

        def to_manifest(self):
            return BundleManifest(self.data)
