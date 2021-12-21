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

    @patch("sign_workflow.sign_artifacts.BuildManifest.from_path")
    def test_sign_with_build_manifest(self, *mocks):
        path = Path(r"/dummy/path/manifest.yml")
        component = 'maven'
        artifact_type = 'dummy'
        sigtype = '.asc'
        signer = MagicMock()
        signer_with_manifest = SignWithBuildManifest(path, component, artifact_type, sigtype, signer)
        ## ToDo: path to manifest is not found, so how to mock?
        signer_with_manifest.sign()
        signer.sign_artifacts.assert_called_with()

    def test_sign_existing_artifacts_file(self):
        sigtype = '.sig'
        signer = MagicMock()
        signer_with_manifest = SignArtifactsExistingArtifactFile(target=Path(r"/dummy/path/file.tar.gz"),
                                                                 component='maven',
                                                                 artifact_type='dummy',
                                                                 signature_type=sigtype,
                                                                 signer=signer)
        signer_with_manifest.sign()
        signer.sign_artifact.assert_called_with("file.tar.gz", Path(r"/dummy/path"), sigtype)

    def test_sign_existing_artifacts_folder(self):
        sigtype = '.sig'
        signer = MagicMock()
        signer_with_manifest = SignExistingArtifactsDir(target=Path(r"/dummy/path/"),
                                                                 component='maven',
                                                                 artifact_type='dummy',
                                                                 signature_type=sigtype,
                                                                 signer=signer)
        ## ToDo: path is not found, so how to mock?
        signer_with_manifest.sign()
        signer.sign_artifact.assert_called_with("file.tar.gz", Path(r"/dummy/path"), sigtype)
