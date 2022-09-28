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

from sign_workflow.signer_windows import SignerWindows


class TestSignerWindows(unittest.TestCase):

    @patch("sign_workflow.signer.GitRepository")
    def test_accepted_file_types(self, git_repo: Mock) -> None:
        artifacts = [
            "bad-xml.xml",
            "the-msi.msi",
            "the-exe.exe",
            "the-dll.dll",
            "the-sys.sys",
            "the-ps1.ps1",
            "the-psm1.psm1",
            "the-cat.cat",
            "the-zip.zip",
            "random-file.txt",
            "something-1.0.0.0.jar",
        ]
        expected = [
            call("the-msi.msi", Path("path"), ".asc"),
            call("the-exe.exe", Path("path"), ".asc"),
            call("the-dll.dll", Path("path"), ".asc"),
            call("the-sys.sys", Path("path"), ".asc"),
            call("the-ps1.ps1", Path("path"), ".asc"),
            call("the-psm1.psm1", Path("path"), ".asc"),
            call("the-cat.cat", Path("path"), ".asc"),
            call("the-zip.zip", Path("path"), ".asc"),
        ]
        signer = SignerWindows()
        signer.sign = MagicMock()  # type: ignore
        signer.sign_artifacts(artifacts, Path("path"), ".asc")
        self.assertEqual(signer.sign.call_args_list, expected)

    @patch("sign_workflow.signer.GitRepository")
    @patch('os.rename')
    @patch('os.mkdir')
    def test_signer_sign(self, mock_os_mkdir: Mock, mock_os_rename: Mock, mock_repo: Mock) -> None:
        signer = SignerWindows()
        signer.sign("the-msi.msi", Path("/path/"), ".asc")
        command = "./opensearch-signer-client -i " + os.path.join(Path("/path/"), 'the-msi.msi') + " -o " + os.path.join(Path("/path/"), 'signed_the-msi.msi') + " -p windows"
        mock_repo.assert_has_calls(
            [call().execute(command)])
