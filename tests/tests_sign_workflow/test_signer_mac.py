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

from sign_workflow.signer_mac import SignerMac


class TestSignerMac(unittest.TestCase):
    @patch("platform.system", return_value='Darwin')
    @patch("sign_workflow.signer.GitRepository")
    def test_accepted_file_types(self, git_repo: Mock, platform_moc: Mock) -> None:
        artifacts = [
            "bad-xml.xml",
            "the-dmg.dmg",
            "the-exe.exe",
            "the-dll.dll",
            "the-sys.sys",
            "the-pkg.pkg",
            "the-psm1.psm1",
            "the-cat.cat",
            "random-file.txt",
            "something-1.0.0.0.jar",
            "the-dylib.dylib"
        ]
        expected = [
            call("the-dmg.dmg", Path("path"), 'null'),
            call("the-pkg.pkg", Path("path"), 'null'),
            call("the-dylib.dylib", Path("path"), 'null')
        ]
        signer = SignerMac(True)
        signer.sign = MagicMock()  # type: ignore
        signer.sign_artifacts(artifacts, Path("path"), 'null')
        self.assertEqual(signer.sign.call_args_list, expected)

    @patch("sign_workflow.signer.GitRepository")
    @patch("platform.system", return_value='Darwin')
    @patch('os.rename')
    @patch('os.mkdir')
    def test_signer_sign(self, mock_os_mkdir: Mock, mock_os_rename: Mock, platform_moc: Mock, mock_repo: Mock) -> None:
        signer = SignerMac(False)
        signer.sign("the-pkg.pkg", Path("/path/"), "null")
        command = "./opensearch-signer-client -i " + os.path.join(Path("/path/"),
                                                                  'the-pkg.pkg') + " -o " + os.path.join(Path("/path/"),
                                                                                                         'signed_the-pkg.pkg') + " -p mac -r False"
        mock_repo.assert_has_calls(
            [call().execute(command)])

    @patch("platform.system", return_value='Darwin')
    @patch("sign_workflow.signer.GitRepository")
    def test_sign_command_for_overwrite(self, mock_repo: Mock, platform_moc: Mock) -> None:
        signer = SignerMac(True)
        signer.sign("the-pkg.pkg", Path("/path/"), 'null')
        command = "./opensearch-signer-client -i " + os.path.join(Path("/path/"),
                                                                  'the-pkg.pkg') + " -o " + os.path.join(Path("/path/"),
                                                                                                         'the-pkg.pkg') + " -p mac" + " -r True"
        mock_repo.assert_has_calls(
            [call().execute(command)])

    @patch("platform.system", return_value='Darwin')
    @patch("sign_workflow.signer.GitRepository")
    def test_signer_verify(self, mock_repo: Mock, platform_moc: Mock) -> None:
        signer = SignerMac(True)
        signer.verify("/path/the-pkg.pkg")
        mock_repo.assert_has_calls([call().execute('pkgutil --check-signature /path/the-pkg.pkg')])

    @patch("platform.system", return_value='Darwin')
    @patch("sign_workflow.signer.GitRepository")
    def test_signer_verify_dylib(self, mock_repo: Mock, platform_moc: Mock) -> None:
        signer = SignerMac(True)
        signer.verify("/path/the-dylib.dylib")
        mock_repo.assert_has_calls([call().execute('codesign --verify --deep --verbose=4 --display /path/the-dylib.dylib')])

    @patch("platform.system", return_value='Linux')
    @patch("sign_workflow.signer.GitRepository")
    def test_signer_invalid_os(self, mock_repo: Mock, platform_moc: Mock) -> None:
        with self.assertRaises(OSError) as ctx:
            signer = SignerMac(True)
            signer.verify("/path/the-pkg.pkg")
        self.assertEqual(str(ctx.exception), 'Cannot verify mac artifacts on non-Darwin system, Linux')
