# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, patch

from sign_workflow.signer import Signer


class TestSigner(unittest.TestCase):
    class DummySigner(Signer):
        def generate_signature_and_verify(self, artifact: str, basepath: Path, signature_type: str) -> None:
            pass

        def is_valid_file_type(self, file_name: str) -> bool:
            return file_name.endswith('zip')

        def sign(self, artifact: str, basepath: Path, signature_type: str) -> None:
            pass

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_checks_out_tool(self, mock_repo: Mock) -> None:
        self.DummySigner()
        self.assertEqual(mock_repo.return_value.execute.call_count, 2)
        mock_repo.return_value.execute.assert_has_calls([call("./bootstrap"), call("rm config.cfg")])

    @patch("sign_workflow.signer.GitRepository")
    def test_sign_artifact_not_called(self, mock_repo: Mock) -> None:
        signer = self.DummySigner()
        signer.generate_signature_and_verify = MagicMock()  # type: ignore
        signer.sign_artifact("the-jar.notvalid", Path("/path"), ".sig")
        signer.generate_signature_and_verify.assert_not_called()

    @patch("sign_workflow.signer.GitRepository")
    def test_sign_artifact_called(self, mock_repo: Mock) -> None:
        signer = self.DummySigner()
        signer.generate_signature_and_verify = MagicMock()  # type: ignore
        signer.sign_artifact("the-jar.zip", Path("/path"), ".sig")
        signer.generate_signature_and_verify.assert_called_with("the-jar.zip", Path("/path"), ".sig")

    @patch("sign_workflow.signer.GitRepository")
    def test_remove_existing_signature_found(self, mock_repo: Mock) -> None:
        signer = self.DummySigner()
        os.remove = MagicMock()
        signer.__remove_existing_signature__("tests/tests_sign_workflow/data/signature/tar_dummy_artifact_1.0.0.tar.gz.sig")
        os.remove.assert_called_with("tests/tests_sign_workflow/data/signature/tar_dummy_artifact_1.0.0.tar.gz.sig")

    @patch("sign_workflow.signer.GitRepository")
    def test_remove_existing_signature_not_found(self, mock_repo: Mock) -> None:
        signer = self.DummySigner()
        os.remove = MagicMock()
        signer.__remove_existing_signature__("tests/tests_sign_workflow/data/signature/not_found.tar.gz.sig")
        os.remove.assert_not_called()
