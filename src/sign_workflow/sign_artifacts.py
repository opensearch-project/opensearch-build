#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from abc import abstractmethod
from pathlib import Path

from manifests.build_manifest import BuildManifest


class SignArtifacts:
    def __init__(self, target: Path, component, artifact_type, signature_type, signer):
        self.target = target
        self.component = component
        self.artifact_type = artifact_type
        self.signature_type = signature_type
        self.signer = signer

    @abstractmethod
    def __sign__(self):
        pass

    def sign(self):
        self.__sign__()
        logging.info("Done.")

    def __sign_artifacts__(self, artifacts, basepath):
        self.signer.sign_artifacts(artifacts, basepath, self.signature_type)

    def __sign_artifact__(self, artifact, basepath):
        self.signer.sign_artifact(artifact, basepath, self.signature_type)

    @classmethod
    def __signer_class__(self, path: Path):
        if path.is_dir():
            return SignExistingArtifactsDir
        elif path.suffix == ".yml":
            return SignWithBuildManifest
        else:
            return SignArtifactsExistingArtifactFile

    @classmethod
    def from_path(self, path: Path, component, artifact_type, signature_type, signer):
        klass = self.__signer_class__(path)
        return klass(path, component, artifact_type, signature_type, signer)


class SignWithBuildManifest(SignArtifacts):

    def __sign__(self):
        manifest = BuildManifest.from_file(self.target.open("r"))
        basepath = self.target.parent
        for component in manifest.components.select(focus=self.component):
            logging.info(f"Signing {component.name}")

            for component_artifact_type in component.artifacts:
                if self.artifact_type and self.artifact_type != component_artifact_type:
                    continue

                super().__sign_artifacts__(component.artifacts[component_artifact_type], basepath)


class SignArtifactsExistingArtifactFile(SignArtifacts):

    def __sign__(self):
        artifacts = self.target.name
        basename = self.target.parent
        super().__sign_artifact__(artifacts, basename)


class SignExistingArtifactsDir(SignArtifacts):

    def __sign__(self):
        for subdir, dirs, files in os.walk(self.target):
            super().__sign_artifacts__(files, subdir)
