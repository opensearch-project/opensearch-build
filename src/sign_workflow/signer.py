#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from git.git_repository import GitRepository

"""
This class is responsible for signing an artifact using the OpenSearch-signer-client and verifying its signature.
The signed artifacts will be found in the same location as the original artifacts.
"""


class Signer:
    ACCEPTED_FILE_TYPES = [".zip", ".jar", ".war", ".pom", ".module", ".tar.gz"]

    def __init__(self):
        self.git_repo = GitRepository(self.get_repo_url(), "HEAD", working_subdirectory="src")
        self.git_repo.execute("./bootstrap")
        self.git_repo.execute("rm config.cfg")

    def sign_artifact(self, artifact, basepath, signature_type):
        if not self.is_valid_file_type(artifact):
            logging.info(f"Skipping signing of file {artifact}")
            return
        self.generate_signature_and_verify(artifact, basepath, signature_type)

    def sign_artifacts(self, artifacts, basepath, signature_type):
        for artifact in artifacts:
            if not self.is_valid_file_type(artifact):
                logging.info(f"Skipping signing of file {artifact}")
                continue
            self.generate_signature_and_verify(artifact, basepath, signature_type)

    def generate_signature_and_verify(self, artifact, basepath, signature_type):
        location = os.path.join(basepath, artifact)
        self.sign(location, signature_type)
        self.verify(location + signature_type)

    def is_valid_file_type(self, file_name):
        return any(
            file_name.endswith(x) for x in Signer.ACCEPTED_FILE_TYPES
        )

    def get_repo_url(self):
        if "GITHUB_TOKEN" in os.environ:
            return "https://${GITHUB_TOKEN}@github.com/opensearch-project/opensearch-signer-client.git"
        return "https://github.com/opensearch-project/opensearch-signer-client.git"

    def __remove_existing_signature__(self, signature_file):
        if os.path.exists(signature_file):
            logging.warning(f"Removing existing signature file {signature_file}")
            os.remove(signature_file)

    def sign(self, filename, signature_type):
        signature_file = filename + signature_type
        self.__remove_existing_signature__(signature_file)
        signing_cmd = [
            "./opensearch-signer-client",
            "-i",
            filename,
            "-o",
            signature_file,
            "-p",
            "pgp",
        ]
        self.git_repo.execute(" ".join(signing_cmd))

    def verify(self, filename):
        verify_cmd = ["gpg", "--verify-files", filename]
        self.git_repo.execute(" ".join(verify_cmd))
