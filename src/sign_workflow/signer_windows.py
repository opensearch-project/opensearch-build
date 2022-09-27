#!/usr/bin/env python
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from pathlib import Path

from sign_workflow.signer import Signer

"""
This class is responsible for signing an artifact using the OpenSearch-signer-client and verifying its signature.
The signed artifacts will be found in the subfolder called signed under the origin location as the original artifacts.
"""


class SignerWindows(Signer):

    ACCEPTED_FILE_TYPES = [".msi", ".exe", ".dll", ".sys", ".ps1", ".psm1", ".psd1", ".cat", ".zip"]

    def generate_signature_and_verify(self, artifact: str, basepath: Path, signature_type: str) -> None:
        self.sign(artifact, basepath, signature_type)

    def is_valid_file_type(self, file_name: str) -> bool:
        return any(
            file_name.endswith(x) for x in SignerWindows.ACCEPTED_FILE_TYPES
        )

    def sign(self, artifact: str, basepath: Path, signature_type: str) -> None:
        filename = os.path.join(basepath, artifact)
        signed_prefix = "signed_"
        signature_file = os.path.join(basepath, signed_prefix + artifact)
        self.__remove_existing_signature__(signature_file)
        signing_cmd = [
            "./opensearch-signer-client",
            "-i",
            filename,
            "-o",
            signature_file,
            "-p",
            "windows",
        ]
        self.git_repo.execute(" ".join(signing_cmd))
        signed_folder = os.path.join(basepath, "signed")
        if not os.path.exists(signed_folder):
            os.mkdir(signed_folder)
        signed_location = os.path.join(signed_folder, artifact)
        os.rename(signature_file, signed_location)
