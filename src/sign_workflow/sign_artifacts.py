#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from abc import abstractmethod
from pathlib import Path
from typing import Any, List, Type

from manifests.build_manifest import BuildManifest
from sign_workflow.signer import Signer
from sign_workflow.signers import Signers


class SignArtifacts:
    target: Path
    component: str
    artifact_type: str
    signature_type: str
    platform: str
    signer: Signer

    def __init__(self, target: Path, components: List[str], artifact_type: str, signature_type: str, platform: str) -> None:
        self.target = target
        self.components = components
        self.artifact_type = artifact_type
        self.signature_type = signature_type
        self.platform = platform
        self.signer = Signers.create(platform)

    @abstractmethod
    def __sign__(self) -> None:
        pass

    def sign(self) -> None:
        self.__sign__()
        logging.info("Done.")

    def __sign_artifacts__(self, artifacts: List[str], basepath: Path) -> None:
        self.signer.sign_artifacts(artifacts, basepath, self.signature_type)

    def __sign_artifact__(self, artifact: str, basepath: Path) -> None:
        self.signer.sign_artifact(artifact, basepath, self.signature_type)

    @classmethod
    def __signer_class__(self, path: Path) -> Type[Any]:
        if path.is_dir():
            return SignExistingArtifactsDir
        elif path.suffix == ".yml":
            return SignWithBuildManifest
        else:
            return SignArtifactsExistingArtifactFile

    @classmethod
    def from_path(self, path: Path, components: List[str], artifact_type: str, signature_type: str, platform: str) -> Any:
        klass = self.__signer_class__(path)
        return klass(path, components, artifact_type, signature_type, platform)


class SignWithBuildManifest(SignArtifacts):
    def __sign__(self) -> None:
        manifest = BuildManifest.from_file(self.target.open("r"))
        basepath = self.target.parent
        for component in manifest.components.select(focus=self.components):
            logging.info(f"Signing {component.name}")

            for component_artifact_type in component.artifacts:
                if self.artifact_type and self.artifact_type != component_artifact_type:
                    continue

                super().__sign_artifacts__(component.artifacts[component_artifact_type], basepath)


class SignArtifactsExistingArtifactFile(SignArtifacts):
    def __sign__(self) -> None:
        artifacts = self.target.name
        basename = self.target.parent
        super().__sign_artifact__(artifacts, basename)


class SignExistingArtifactsDir(SignArtifacts):
    def __sign__(self) -> None:
        for subdir, dirs, files in os.walk(self.target):
            super().__sign_artifacts__(files, Path(subdir))
