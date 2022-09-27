#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from git.git_repository import GitRepository


class Signer(ABC):
    git_repo: GitRepository

    def __init__(self) -> None:
        self.git_repo = GitRepository(self.get_repo_url(), "HEAD", working_subdirectory="src")
        self.git_repo.execute("./bootstrap")
        self.git_repo.execute("rm config.cfg")

    def sign_artifact(self, artifact: str, basepath: Path, signature_type: str) -> None:
        if not self.is_valid_file_type(artifact):
            logging.info(f"Skipping signing of file {artifact}")
            return
        self.generate_signature_and_verify(artifact, basepath, signature_type)

    def sign_artifacts(self, artifacts: List[str], basepath: Path, signature_type: str) -> None:
        for artifact in artifacts:
            if not self.is_valid_file_type(artifact):
                logging.info(f"Skipping signing of file {artifact}")
                continue
            self.generate_signature_and_verify(artifact, basepath, signature_type)

    @abstractmethod
    def generate_signature_and_verify(self, artifact: str, basepath: Path, signature_type: str) -> None:
        pass

    @abstractmethod
    def is_valid_file_type(self, file_name: str) -> bool:
        pass

    def get_repo_url(self) -> str:
        if "GITHUB_TOKEN" in os.environ:
            return "https://${GITHUB_TOKEN}@github.com/opensearch-project/opensearch-signer-client.git"
        return "https://github.com/opensearch-project/opensearch-signer-client.git"

    def __remove_existing_signature__(self, signature_file: str) -> None:
        if os.path.exists(signature_file):
            logging.warning(f"Removing existing signature file {signature_file}")
            os.remove(signature_file)

    @abstractmethod
    def sign(self, artifact: str, basepath: Path, signature_type: str) -> None:
        pass
