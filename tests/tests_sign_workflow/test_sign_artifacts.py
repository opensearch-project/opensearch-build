import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from sign_workflow.sign_artifacts import SignArtifacts, SignArtifactsExistingArtifactFile, SignExistingArtifactsDir, SignWithBuildManifest


class TestSignArtifacts(unittest.TestCase):

    @patch("sign_workflow.signer.GitRepository")
    @patch("sign_workflow.signer.Signer", return_value=MagicMock())
    def test_from_path_method(self, mock_signer, *mocks):
        path = Path(r"/dummy/path/manifest.yml")
        component = 'maven'
        artifact_type = 'dummy'
        sigtype = '.asc'

        klass = SignArtifacts.from_path(path, component, artifact_type, sigtype, mock_signer)
        self.assertEqual(type(SignWithBuildManifest), type(klass.__class__))

        path = Path(r"/dummy/path/")
        klass = SignArtifacts.from_path(path, component, artifact_type, sigtype, mock_signer)
        self.assertEqual(type(SignExistingArtifactsDir), type(klass.__class__))

        path = Path(r"/dummy/path/artifact.tar.gz")
        klass = SignArtifacts.from_path(path, component, artifact_type, sigtype, mock_signer)
        self.assertEqual(type(SignArtifactsExistingArtifactFile), type(klass.__class__))

    def test_signer_class(self):
        self.assertIs(SignArtifacts.__signer_class__(
            Path(r"/dummy/path/manifest.yml")),
            SignWithBuildManifest)

        self.assertIs(SignArtifacts.__signer_class__(
            Path(os.path.dirname(__file__))),
            SignExistingArtifactsDir)

        self.assertIs(SignArtifacts.__signer_class__(
            Path(r"/dummy/path/artifact.tar.gz")),
            SignArtifactsExistingArtifactFile)
