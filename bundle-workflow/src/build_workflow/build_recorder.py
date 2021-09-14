# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil

from build_workflow.build_artifact_check_maven import BuildArtifactCheckMaven
from build_workflow.build_artifact_check_plugin import BuildArtifactCheckPlugin
from manifests.build_manifest import BuildManifest


class BuildRecorder:
    def __init__(self, target):
        self.build_manifest = self.BuildManifestBuilder(target)
        self.target = target

    def record_component(self, component_name, git_repo):
        self.build_manifest.append_component(
            component_name,
            self.target.component_version,
            git_repo.url,
            git_repo.ref,
            git_repo.sha,
        )

    def record_artifact(
        self, component_name, artifact_type, artifact_path, artifact_file
    ):
        logging.info(
            f"Recording {artifact_type} artifact for {component_name}: {artifact_path} (from {artifact_file})"
        )
        # Ensure the target directory exists
        dest_file = os.path.join(self.target.output_dir, artifact_path)
        dest_dir = os.path.dirname(dest_file)
        os.makedirs(dest_dir, exist_ok=True)
        # Check artifact
        self.__check_artifact(artifact_type, artifact_file)
        # Copy the file
        shutil.copyfile(artifact_file, dest_file)
        # Notify the recorder
        self.build_manifest.append_artifact(
            component_name, artifact_type, artifact_path
        )

    def get_manifest(self):
        return self.build_manifest.to_manifest()

    def write_manifest(self):
        manifest_path = os.path.join(self.target.output_dir, "manifest.yml")
        self.get_manifest().to_file(manifest_path)
        logging.info(f'Created build manifest {manifest_path}')

    def __check_artifact(self, artifact_type, artifact_file):
        if artifact_type == "plugins":
            BuildArtifactCheckPlugin(self.target).check(artifact_file)
        elif artifact_type == "maven":
            BuildArtifactCheckMaven(self.target).check(artifact_file)

    class BuildManifestBuilder:
        def __init__(self, target):
            self.data = {}
            self.data["build"] = {}
            self.data["build"]["id"] = target.build_id
            self.data["build"]["name"] = target.name
            self.data["build"]["version"] = target.opensearch_version
            self.data["build"]["architecture"] = target.arch
            self.data["build"]["snapshot"] = str(target.snapshot).lower()
            self.data["schema-version"] = "1.0"
            # We need to store components as a hash so that we can append artifacts by component name
            # When we convert to a BuildManifest this will get converted back into a list
            self.data["components_hash"] = {}

        def append_component(self, name, version, repository_url, ref, commit_id):
            component = {
                "name": name,
                "repository": repository_url,
                "ref": ref,
                "commit_id": commit_id,
                "artifacts": {},
                "version": version,
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
