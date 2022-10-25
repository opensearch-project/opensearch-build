# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, Mock, patch

from sign_workflow.sign_artifacts import SignArtifacts, SignArtifactsExistingArtifactFile, SignExistingArtifactsDir, SignWithBuildManifest


class TestSignArtifacts(unittest.TestCase):

    @patch("sign_workflow.signer.GitRepository")
    @patch("sign_workflow.signer_pgp.SignerPGP", return_value=MagicMock())
    def test_from_path_method(self, mock_signer: Mock, *mocks: Any) -> None:
        components = ['maven']
        artifact_type = 'dummy'
        sigtype = '.asc'
        platform = 'linux'

        klass = SignArtifacts.from_path(Path(r"/dummy/path/manifest.yml"), components, artifact_type, sigtype, platform)
        self.assertEqual(type(SignWithBuildManifest), type(klass.__class__))

        klass = SignArtifacts.from_path(Path(os.path.dirname(__file__)), components, artifact_type, sigtype, platform)
        self.assertEqual(type(SignExistingArtifactsDir), type(klass.__class__))

        klass = SignArtifacts.from_path(Path(r"/dummy/path/artifact.tar.gz"), components, artifact_type, sigtype, platform)
        self.assertEqual(type(SignArtifactsExistingArtifactFile), type(klass.__class__))

    def test_signer_class(self) -> None:
        self.assertIs(SignArtifacts.__signer_class__(
            Path(r"/dummy/path/manifest.yml")),
            SignWithBuildManifest)

        self.assertIs(SignArtifacts.__signer_class__(
            Path(os.path.dirname(__file__))),
            SignExistingArtifactsDir)

        self.assertIs(SignArtifacts.__signer_class__(
            Path(r"/dummy/path/artifact.tar.gz")),
            SignArtifactsExistingArtifactFile)

    @patch("sign_workflow.signer.GitRepository")
    def test_sign_with_build_manifest(self, mock_repo: Mock) -> None:
        manifest = Path(os.path.join(os.path.dirname(__file__), "data", "opensearch-build-1.1.0.yml"))
        sigtype = '.asc'
        platform = 'windows'
        signer_with_manifest = SignWithBuildManifest(
            target=manifest,
            components=[],
            artifact_type="maven",
            signature_type=sigtype,
            platform=platform
        )
        signer = MagicMock()
        signer_with_manifest.signer = signer
        signer_with_manifest.sign()
        expected = [
            'maven/org/opensearch/opensearch-performance-analyzer/maven-metadata-local.xml',
            'maven/org/opensearch/opensearch-performance-analyzer/1.1.0.0/opensearch-performance-analyzer-1.1.0.0-javadoc.jar',
            'maven/org/opensearch/opensearch-performance-analyzer/1.1.0.0/opensearch-performance-analyzer-1.1.0.0.pom',
            'maven/org/opensearch/opensearch-performance-analyzer/1.1.0.0/opensearch-performance-analyzer-1.1.0.0.module',
            'maven/org/opensearch/opensearch-performance-analyzer/1.1.0.0/opensearch-performance-analyzer-1.1.0.0.jar',
            'maven/org/opensearch/opensearch-performance-analyzer/1.1.0.0/opensearch-performance-analyzer-1.1.0.0-sources.jar'
        ]
        signer.sign_artifacts.assert_called_with(expected, manifest.parent, sigtype)

    @patch("sign_workflow.signer.GitRepository")
    def test_sign_existing_artifacts_file(self, mock_repo: Mock) -> None:
        path = Path(r"/dummy/path/file.tar.gz")
        sigtype = '.sig'
        platform = 'linux'
        signer_with_manifest = SignArtifactsExistingArtifactFile(
            target=path,
            components=['maven'],
            artifact_type='dummy',
            signature_type=sigtype,
            platform=platform
        )
        signer = MagicMock()
        signer_with_manifest.signer = signer
        signer_with_manifest.sign()
        expected = 'file.tar.gz'
        signer.sign_artifact.assert_called_with(expected, path.parent, sigtype)

    @patch("sign_workflow.signer.GitRepository")
    @patch('os.walk')
    def test_sign_existing_artifacts_folder(self, mock_os_walk: Mock, mock_repo: Mock) -> None:
        mock_os_walk.return_value = [
            ('dummy', (), ['tar_dummy_artifact_1.0.0.tar.gz', 'zip_dummy_artifact_1.1.0.zip'])
        ]
        path = Path('dummy')
        sigtype = '.sig'
        platform = 'linux'
        signer_with_manifest = SignExistingArtifactsDir(
            target=path,
            components=['maven'],
            artifact_type='dummy',
            signature_type=sigtype,
            platform=platform
        )
        signer = MagicMock()
        signer_with_manifest.signer = signer
        signer_with_manifest.sign()
        expected = ["tar_dummy_artifact_1.0.0.tar.gz", "zip_dummy_artifact_1.1.0.zip"]
        signer.sign_artifacts.assert_called_with(expected, path, sigtype)
