import unittest
from unittest.mock import MagicMock, call, patch

from sign_workflow.signer import Signer


class TestSigner(unittest.TestCase):
    @patch("sign_workflow.signer.GitRepository")
    def test_accepted_file_types(self, git_repo):

        artifacts = [
            "bad-xml.xml",
            "the-jar.jar",
            "the-zip.zip",
            "the-war.war",
            "the-pom.pom",
            "the-module.module",
            "the-tar.tar.gz",
            "random-file.txt",
            "something-1.0.0.0.jar",
        ]
        expected = [
            call("/path/the-jar.jar"),
            call("/path/the-zip.zip"),
            call("/path/the-war.war"),
            call("/path/the-pom.pom"),
            call("/path/the-module.module"),
            call("/path/the-tar.tar.gz"),
            call("/path/something-1.0.0.0.jar"),
        ]
        signer = Signer()
        signer.sign = MagicMock()
        signer.sign_artifacts(artifacts, "/path")
        self.assertEqual(signer.sign.call_args_list, expected)
