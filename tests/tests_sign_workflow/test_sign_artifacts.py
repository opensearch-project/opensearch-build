import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch, call

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
        BUILD_MANIFEST = Path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-1.1.0.yml"))
        sigtype = '.asc'
        signer = MagicMock()
        signer_with_manifest = SignWithBuildManifest(target=BUILD_MANIFEST,
                                                     component="maven",
                                                     artifact_type="artifacts",
                                                     signature_type=sigtype,
                                                     signer=signer)
        ## ToDo: focus maven not found
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
        path = Path(os.path.join(os.path.dirname(__file__), "data/artifacts"))
        sigtype = '.sig'
        signer = MagicMock()
        signer_with_manifest = SignExistingArtifactsDir(target=path,
                                                         component='maven',
                                                         artifact_type='dummy',
                                                         signature_type=sigtype,
                                                         signer=signer)
        ## ToDo: assert not found but method is called
        signer_with_manifest.sign()
        expected = ["dummy_artifact_1.1.0.tar.gz", "dummy_artifact_1.0.0.tar.gz"]
        signer.sign_artifact.assert_called_with(expected, path, sigtype)
