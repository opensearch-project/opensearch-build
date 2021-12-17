import unittest
from pathlib import Path

from sign_workflow.sign_artifacts import SignArtifacts, SignArtifactsExistingArtifactFile, SignExistingArtifactsDir, SignWithManifest


class TestSignArtifacts(unittest.TestCase):

    def test_signer_class_method(self):
        path = Path(r"/dummy/path/manifest.yml")
        klass = SignArtifacts.__signer_class__(path)

        self.assertEqual(type(SignWithManifest), type(klass))

        path = Path(r"/dummy/path/")
        klass = SignArtifacts.__signer_class__(path)

        self.assertEqual(type(SignExistingArtifactsDir), type(klass))

        path = Path(r"/dummy/path/artifact.tar.gz")
        klass = SignArtifacts.__signer_class__(path)

        self.assertEqual(type(SignArtifactsExistingArtifactFile), type(klass))

    def test_from_path_method(self):
        path = Path(r"/dummy/path/manifest.yml")
        component = 'maven'
        artifact_type = 'dummy'
        sigtype = '.asc'

        klass = SignArtifacts.from_path(path, component, artifact_type, sigtype)
        self.assertEqual(type(SignWithManifest), type(klass.__class__))

        path = Path(r"/dummy/path/")
        klass = SignArtifacts.from_path(path, component, artifact_type, sigtype)
        self.assertEqual(type(SignExistingArtifactsDir), type(klass.__class__))

        path = Path(r"/dummy/path/artifact.tar.gz")
        klass = SignArtifacts.from_path(path, component, artifact_type, sigtype)
        self.assertEqual(type(SignArtifactsExistingArtifactFile), type(klass.__class__))
