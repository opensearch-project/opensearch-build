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

from sign_workflow.signer_pgp import SignerPGP


class TestSignerPGP(unittest.TestCase):
    @patch("sign_workflow.signer.GitRepository")
    def test_accepted_file_types_asc(self, git_repo: Mock) -> None:
        artifacts = [
            "bad-xml.xml",
            "the-jar.jar",
            "the-zip.zip",
            "the-whl.whl",
            "the-rpm.rpm",
            "the-war.war",
            "the-pom.pom",
            "the-module.module",
            "the-tar.tar.gz",
            "random-file.txt",
            "something-1.0.0.0.jar",
            "the-tgz.tgz"
        ]
        expected = [
            call("the-jar.jar", Path("path"), ".asc"),
            call("the-zip.zip", Path("path"), ".asc"),
            call("the-whl.whl", Path("path"), ".asc"),
            call("the-rpm.rpm", Path("path"), ".asc"),
            call("the-war.war", Path("path"), ".asc"),
            call("the-pom.pom", Path("path"), ".asc"),
            call("the-module.module", Path("path"), ".asc"),
            call("the-tar.tar.gz", Path("path"), ".asc"),
            call("something-1.0.0.0.jar", Path("path"), ".asc"),
            call("the-tgz.tgz", Path("path"), ".asc")
        ]
        signer = SignerPGP(False)
        signer.sign = MagicMock()  # type: ignore
        signer.verify = MagicMock()  # type: ignore
        signer.sign_artifacts(artifacts, Path("path"), ".asc")
        self.assertEqual(signer.sign.call_args_list, expected)

    @patch("sign_workflow.signer.GitRepository")
    def test_accepted_file_types_sig(self, git_repo: Mock) -> None:
        artifacts = [
            "bad-xml.xml",
            "the-jar.jar",
            "the-zip.zip",
            "the-whl.whl",
            "the-rpm.rpm",
            "the-war.war",
            "the-pom.pom",
            "the-module.module",
            "the-tar.tar.gz",
            "random-file.txt",
            "something-1.0.0.0.jar",
            "opensearch_sql_cli-1.0.0-py3-none-any.whl",
            "cratefile.crate",
            "the-tgz.tgz"
        ]
        expected = [
            call("the-jar.jar", Path("path"), ".sig"),
            call("the-zip.zip", Path("path"), ".sig"),
            call("the-whl.whl", Path("path"), ".sig"),
            call("the-rpm.rpm", Path("path"), ".sig"),
            call("the-war.war", Path("path"), ".sig"),
            call("the-pom.pom", Path("path"), ".sig"),
            call("the-module.module", Path("path"), ".sig"),
            call("the-tar.tar.gz", Path("path"), ".sig"),
            call("something-1.0.0.0.jar", Path("path"), ".sig"),
            call("opensearch_sql_cli-1.0.0-py3-none-any.whl", Path("path"), ".sig"),
            call("cratefile.crate", Path("path"), ".sig"),
            call("the-tgz.tgz", Path("path"), ".sig")
        ]
        signer = SignerPGP(False)
        signer.sign = MagicMock()  # type: ignore
        signer.verify = MagicMock()  # type: ignore
        signer.sign_artifacts(artifacts, Path("path"), ".sig")
        self.assertEqual(signer.sign.call_args_list, expected)

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_verify_asc(self, mock_repo: Mock) -> None:
        signer = SignerPGP(True)
        signer.verify("/path/the-jar.jar.asc")
        mock_repo.assert_has_calls([call().execute("gpg --verify-files /path/the-jar.jar.asc")])

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_verify_sig(self, mock_repo: Mock) -> None:
        signer = SignerPGP(True)
        signer.verify("/path/the-jar.jar.sig")
        mock_repo.assert_has_calls([call().execute("gpg --verify-files /path/the-jar.jar.sig")])

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_sign_asc(self, mock_repo: Mock) -> None:
        signer = SignerPGP(False)
        signer.sign("the-jar.jar", Path("/path/"), ".asc")
        command = "./opensearch-signer-client -i " + os.path.join(Path("/path/"), 'the-jar.jar') + " -o " + os.path.join(Path("/path/"), 'the-jar.jar.sig') + " -p pgp -r False"
        conversion_cmd = "gpg --enarmor < " + os.path.join(Path("/path/"), 'the-jar.jar.sig') + " > " +\
                         os.path.join(Path("/path/"), 'the-jar.jar.asc') + " && sed -i 's/ARMORED FILE/SIGNATURE/g' " +\
                         os.path.join(Path("/path/"), 'the-jar.jar.asc')
        mock_repo.assert_has_calls(
            [call().execute(command)])
        mock_repo.assert_has_calls([call().execute(conversion_cmd)])

    @patch("sign_workflow.signer.GitRepository")
    def test_signer_sign_sig(self, mock_repo: Mock) -> None:
        signer = SignerPGP(False)
        signer.sign("the-jar.jar", Path("/path/"), ".sig")
        command = "./opensearch-signer-client -i " + os.path.join(Path("/path/"), 'the-jar.jar') + " -o " + os.path.join(Path("/path/"), 'the-jar.jar.sig') + " -p pgp -r False"
        mock_repo.assert_has_calls(
            [call().execute(command)])
