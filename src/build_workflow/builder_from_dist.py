# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import urllib.request
from typing import Any

from build_workflow.build_recorder import BuildRecorder
from build_workflow.builder import Builder
from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest


class BuilderFromDist(Builder):
    class ManifestGitRepository(GitRepository):
        def __init__(self, manifest: Any) -> None:
            self.url = manifest.repository
            self.ref = manifest.ref
            self.sha = manifest.commit_id

    def checkout(self, work_dir: str) -> None:
        self.__download_build_manifest()

    def build(self, build_recorder: 'BuildRecorder') -> None:
        pass

    @property
    def target_name(self) -> str:
        return self.target.name.lower().replace(' ', '-')

    def export_artifacts(self, build_recorder: 'BuildRecorder') -> None:
        os.makedirs(self.output_path, exist_ok=True)
        component_manifest = self.build_manifest.components[self.component.name]
        logging.info(f"Downloading {component_manifest.name} {component_manifest.version} ({component_manifest.commit_id}) ...")
        logging.info(f"Distribution was built from {component_manifest.repository}#{component_manifest.ref}")
        build_recorder.record_component(self.component.name, BuilderFromDist.ManifestGitRepository(component_manifest))
        for artifact_type in component_manifest.artifacts:
            artifact_path = os.path.join(self.output_path, artifact_type)
            logging.info(f"Downloading into {artifact_path} ...")
            for artifact in component_manifest.artifacts[artifact_type]:
                artifact_url = f"{self.component.dist}/{self.target.platform}/{self.target.architecture}/builds/{self.target_name}/{artifact}"
                artifact_dest = os.path.realpath(os.path.join(self.output_path, artifact))
                os.makedirs(os.path.dirname(artifact_dest), exist_ok=True)
                logging.info(f"Downloading {artifact_url} into {artifact_dest}")
                urllib.request.urlretrieve(artifact_url, artifact_dest)
                build_recorder.record_artifact(self.component.name, artifact_type, artifact, artifact_dest)

    def __download_build_manifest(self) -> None:
        url = f"{self.component.dist}/{self.target.platform}/{self.target.architecture}/builds/{self.target_name}/manifest.yml"
        logging.info(f"Downloading {url} ...")
        self.build_manifest = BuildManifest.from_url(url)
