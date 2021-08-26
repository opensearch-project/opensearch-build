#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import pathlib

from git.git_repository import GitRepository

"""
This class is responsible for signing an artifact using the OpenSearch-signer-client and verifying its signature.
The signed artifacts will be found in the same location as the original artifacts.
"""


class Signer:

    ACCEPTED_FILE_TYPES = [".zip", ".jar", ".war", ".pom", ".module", ".tar.gz"]

    def __init__(self):
        self.git_repo = GitRepository(self.get_repo_url(), "HEAD")
        self.git_repo.execute("./bootstrap", subdirname="src")
        self.git_repo.execute("rm config.cfg", subdirname="src")

    def sign_artifacts(self, artifacts, basepath):
        for artifact in artifacts:
            if not self.is_valid_file_type(artifact):
                print(f"Skipping signing of file ${artifact}")
                continue
            location = os.path.join(basepath, artifact)
            self.sign(location)
            self.verify(location + ".asc")

    def is_valid_file_type(self, file_name):
        return any(
            x
            in [
                pathlib.Path(file_name).suffix,
                "".join(pathlib.Path(file_name).suffixes),
            ]
            for x in Signer.ACCEPTED_FILE_TYPES
        )

    def get_repo_url(self):
        if "GITHUB_TOKEN" in os.environ:
            return "https://${GITHUB_TOKEN}@github.com/opensearch-project/opensearch-signer-client.git"
        return "https://github.com/opensearch-project/opensearch-signer-client.git"

    def sign(self, filename):
        signature_file = filename + ".asc"
        signing_cmd = [
            "./opensearch-signer-client",
            "-i",
            filename,
            "-o",
            signature_file,
            "-p",
            "pgp",
        ]
        self.git_repo.execute(" ".join(signing_cmd), subdirname="src")

    def verify(self, filename):
        verify_cmd = ["gpg", "--verify-files", filename]
        self.git_repo.execute(" ".join(verify_cmd))
