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
    ACCEPTED_FILE_TYPES = [".msi", ".exe", ".dll", ".sys", ".ps1", ".psm1", ".psd1", ".cat"]

    def generate_signature_and_verify(self, artifact: str, basepath: Path, signature_type: str) -> None:
        filename = os.path.join(basepath, artifact)
        signed_filename = filename if self.overwrite else os.path.join(basepath, "signed_" + artifact)
        self.sign(artifact, basepath, signature_type)
        self.verify(signed_filename)

    def is_valid_file_type(self, file_name: str) -> bool:
        return any(
            file_name.endswith(x) for x in SignerWindows.ACCEPTED_FILE_TYPES
        )

    def sign(self, artifact: str, basepath: Path, signature_type: str) -> None:
        filename = os.path.join(basepath, artifact)
        signed_filename = filename if self.overwrite else os.path.join(basepath, "signed_" + artifact)
        signing_cmd = [
            "./opensearch-signer-client",
            "-i",
            filename,
            "-o",
            signed_filename,
            "-p",
            "windows",
            "-r",
            str(self.overwrite)
        ]
        self.git_repo.execute(" ".join(signing_cmd))

    def verify(self, filename: str) -> None:
        verify_cmd = ["osslsigncode", "verify", "-in", filename]
        self.git_repo.execute(" ".join(verify_cmd))
