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

from sign_workflow.signer_jar import SignerJar


class TestSignerJar(unittest.TestCase):

    @patch("sign_workflow.signer.GitRepository")
    def test_accepted_file_types(self, git_repo: Mock) -> None:
        artifacts = [
            "the-msi.msi",
            "the-zip.zip",
            "the-jar.jar",
            "the-taco.taco",
            "the-sys.sys",
            "something-1.0.0.0.jar",
        ]
        expected = [
            call("the-jar.jar", Path("path"), 'null'),
            call("the-taco.taco", Path("path"), 'null'),
            call("something-1.0.0.0.jar", Path("path"), 'null')
        ]
        signer = SignerJar(True)
        signer.sign = MagicMock()  # type: ignore
        signer.sign_artifacts(artifacts, Path("path"), 'null')
        self.assertEqual(signer.sign.call_args_list, expected)

    @patch("sign_workflow.signer.GitRepository")
    @patch('os.rename')
    @patch('os.mkdir')
    def test_signer_sign(self, mock_os_mkdir: Mock, mock_os_rename: Mock, mock_repo: Mock) -> None:
        signer = SignerJar(False)
        signer.sign("the-jar.jar", Path("/path/"), "null")
        command = "./opensearch-signer-client -i " + os.path.join(Path("/path/"), 'the-jar.jar') + " -o " + os.path.join(Path("/path/"), 'signed_the-jar.jar') + " -p jar_signer -r False"
        mock_repo.assert_has_calls(
            [call().execute(command)])

    @patch("sign_workflow.signer.GitRepository")
    def test_sign_command_for_overwrite(self, mock_repo: Mock) -> None:
        signer = SignerJar(True)
        signer.sign("the-taco.taco", Path("/path/"), 'null')
        command = "./opensearch-signer-client -i " + os.path.join(Path("/path/"), 'the-taco.taco') + " -o " + os.path.join(Path("/path/"), 'the-taco.taco') + " -p jar_signer" + " -r True"
        mock_repo.assert_has_calls(
            [call().execute(command)])

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_verify(self, mock_repo: Mock) -> None:
        signer = SignerJar(True)
        signer.verify('/path/the-jar.jar')
        mock_repo.assert_has_calls([call().output("jarsigner -verify /path/the-jar.jar -verbose -certs -strict")])
