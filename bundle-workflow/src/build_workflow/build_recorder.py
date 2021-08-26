# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import shutil

import yaml

from manifests.build_manifest import BuildManifest


class BuildRecorder:
    def __init__(self, build_id, output_dir, name, version, arch, snapshot):
        self.output_dir = output_dir
        self.build_manifest = self.BuildManifestBuilder(
            build_id, name, version, arch, snapshot
        )

    def record_component(self, component_name, git_repo):
        self.build_manifest.append_component(
            component_name, git_repo.url, git_repo.ref, git_repo.sha
        )

    def record_artifact(
        self, component_name, artifact_type, artifact_path, artifact_file
    ):
        print(
            f"Recording {artifact_type} artifact for {component_name}: {artifact_path} (from {artifact_file})"
        )
        # Ensure the target directory exists
        dest_file = os.path.join(self.output_dir, artifact_path)
        dest_dir = os.path.dirname(dest_file)
        os.makedirs(dest_dir, exist_ok=True)
        # Copy the file
        shutil.copyfile(artifact_file, dest_file)
        # Notify the recorder
        self.build_manifest.append_artifact(
            component_name, artifact_type, artifact_path
        )

    def get_manifest(self):
        return self.build_manifest.to_manifest()

    def write_manifest(self, dest_dir):
        output_manifest = self.get_manifest()
        manifest_path = os.path.join(dest_dir, "manifest.yml")
        with open(manifest_path, "w") as file:
            yaml.dump(output_manifest.to_dict(), file)

    class BuildManifestBuilder:
        def __init__(self, build_id, name, version, arch, snapshot):
            self.data = {}
            self.data["build"] = {}
            self.data["build"]["id"] = build_id
            self.data["build"]["name"] = name
            self.data["build"]["version"] = (
                str(version) + "-SNAPSHOT" if snapshot else str(version)
            )
            self.data["build"]["architecture"] = arch
            self.data["build"]["snapshot"] = str(snapshot).lower()
            self.data["schema-version"] = "1.0"
            # We need to store components as a hash so that we can append artifacts by component name
            # When we convert to a BuildManifest this will get converted back into a list
            self.data["components_hash"] = {}

        def append_component(self, name, repository_url, ref, commit_id):
            component = {
                "name": name,
                "repository": repository_url,
                "ref": ref,
                "commit_id": commit_id,
                "artifacts": {},
            }
            self.data["components_hash"][name] = component

        def append_artifact(self, component, type, path):
            artifacts = self.data["components_hash"][component]["artifacts"]
            list = artifacts.get(type, [])
            if len(list) == 0:
                artifacts[type] = list
            list.append(path)

        def to_manifest(self):
            # The build manifest expects `components` to be a list, not a hash, so we need to munge things a bit
            components = self.data["components_hash"].values()
            self.data["components"] = components
            return BuildManifest(self.data)
