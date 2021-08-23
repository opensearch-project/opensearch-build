import unittest
from unittest.mock import MagicMock, call, patch

from src.signing_workflow.signer import Signer


class TestSigner(unittest.TestCase):

    @patch('src.signing_workflow.signer.GitRepository')
    def test_accepted_file_types(self, git_repo):

        artifacts = [
            'bad-xml.xml',
            'the-jar.jar',
            'the-zip.zip',
            'the-war.war',
            'the-pom.pom',
            'the-module.module',
            'the-tar.tar.gz',
            'random-file.txt',
        ]
        expected = [
            call('/path/the-jar.jar'),
            call('/path/the-zip.zip'),
            call('/path/the-war.war'),
            call('/path/the-pom.pom'),
            call('/path/the-module.module'),
            call('/path/the-tar.tar.gz'),
        ]
        signer = Signer()
        signer.sign = MagicMock()
        signer.sign_artifacts(artifacts, '/path')
        self.assertEqual(signer.sign.call_args_list, expected)
