# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil
from typing import Any, Dict

from build_workflow.build_artifact_checks import BuildArtifactChecks
from build_workflow.build_target import BuildTarget
from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest


class BuildRecorder:
    def __init__(self, target: BuildTarget):
        self.build_manifest = self.BuildManifestBuilder(target)
        self.target = target
        self.name = target.name

    def record_component(self, component_name: str, git_repo: GitRepository) -> None:
        self.build_manifest.append_component(
            component_name,
            self.target.component_version,
            git_repo.url,
            git_repo.ref,
            git_repo.sha,
        )

    def record_artifact(self, component_name: str, artifact_type: str, artifact_path: str, artifact_file: str) -> None:
        logging.info(f"Recording {artifact_type} artifact for {component_name}: {artifact_path} (from {artifact_file})")
        # Ensure the target directory exists
        dest_file = os.path.join(self.target.output_dir, artifact_path)
        dest_dir = os.path.dirname(dest_file)
        os.makedirs(dest_dir, exist_ok=True)
        # Check artifact
        BuildArtifactChecks.check(self.target, artifact_type, artifact_file)
        # Copy the file
        shutil.copyfile(artifact_file, dest_file)
        # Notify the recorder
        self.build_manifest.append_artifact(component_name, artifact_type, artifact_path)

    def get_manifest(self) -> BuildManifest:
        return self.build_manifest.to_manifest()

    def write_manifest(self) -> None:
        manifest_path = os.path.join(self.target.output_dir, "manifest.yml")
        self.get_manifest().to_file(manifest_path)
        logging.info(f"Created build manifest {manifest_path}")

    class BuildManifestBuilder:
        def __init__(self, target: BuildTarget):
            self.data: Dict[str, Any] = {}
            self.data["build"] = {}
            self.data["build"]["id"] = target.build_id
            self.data["build"]["name"] = target.name
            self.data["build"]["version"] = target.opensearch_version
            self.data["build"]["platform"] = target.platform
            self.data["build"]["architecture"] = target.architecture
            self.data["build"]["distribution"] = target.distribution if target.distribution else "tar"
            self.data["schema-version"] = "1.2"
            self.components_hash: Dict[str, Dict[str, Any]] = {}

        def append_component(self, name: str, version: str, repository_url: str, ref: str, commit_id: str) -> None:
            component = {
                "name": name,
                "repository": repository_url,
                "ref": ref,
                "commit_id": commit_id,
                "artifacts": {},
                "version": version,
            }
            self.components_hash[name] = component

        def append_artifact(self, component: str, type: str, path: str) -> None:
            artifacts = self.components_hash[component]["artifacts"]
            list = artifacts.get(type, [])
            if len(list) == 0:
                artifacts[type] = list
            list.append(path)

        def to_manifest(self) -> 'BuildManifest':
            # The build manifest expects `components` to be a list, not a hash, so we need to munge things a bit
            components = self.components_hash.values()
            if len(components):
                self.data["components"] = list(components)
            return BuildManifest(self.data)
