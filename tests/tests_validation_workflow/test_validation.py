# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from system.temporary_directory import TemporaryDirectory
from validation_workflow.tar.validation_tar import ValidateTar
from validation_workflow.validation import Validation
from validation_workflow.validation_args import ValidationArgs


class ImplementValidation(Validation):
    def __init__(self, args: ValidationArgs) -> None:
        super().__init__(args)
        self.tmp_dir = TemporaryDirectory()

    def download_artifacts(self) -> None:
        return None

    def installation(self) -> None:
        return None

    def start_cluster(self) -> None:
        return None

    def validation(self) -> None:
        return None

    def cleanup(self) -> None:
        return None


class TestValidation(unittest.TestCase):

    @patch('validation_workflow.download_utils.DownloadUtils')
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_check_url_valid(self, mock_validation_args: Mock, mock_download_utils: Mock) -> None:
        mock_validation_args.projects.return_value = ["opensearch"]

        mock_validation = ValidateTar(mock_validation_args.return_value)
        mock_download_utils_download = mock_download_utils.return_value
        mock_download_utils_download.download.return_value = True
        mock_download_utils_download.is_url_valid.return_value = True
        url = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.12/latest/linux/x64/rpm/dist/opensearch/opensearch-1.3.12.staging.repo"

        result = mock_validation.check_url(url)
        self.assertTrue(result)

    @patch('shutil.copy2', return_value=True)
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_copy_artifact(self, mock_validation_args: Mock, mock_copy: Mock) -> None:
        mock_validation_args.projects.return_value = ["opensearch"]
        mock_validation = ValidateTar(mock_validation_args.return_value)

        url = "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/1.3.12/latest/linux/x64/rpm/dist/opensearch/opensearch-1.3.12.staging.repo"

        result = mock_validation.copy_artifact(url, "tmp/tthcdhfh/")
        self.assertTrue(result)

    @patch('validation_workflow.validation.execute')
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_is_allow_with_security_true(self, mock_validation_args: Mock, mock_execute: Mock) -> None:
        mock_execute.return_value = (0, "opensearch-security", "")

        mock_validation_args.projects.return_value = ["opensearch"]
        mock_validation = ValidateTar(mock_validation_args.return_value)

        result = mock_validation.test_security_plugin("/bin/opensearch")

        self.assertTrue(result)

    @patch('validation_workflow.validation.execute')
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_is_allow_with_security_false(self, mock_validation_args: Mock, mock_execute: Mock) -> None:
        mock_execute.return_value = (0, "opensearch", "")

        mock_validation_args.projects.return_value = ["opensearch"]
        mock_validation = ValidateTar(mock_validation_args.return_value)

        result = mock_validation.test_security_plugin("/bin/opensearch")

        self.assertFalse(result)

    @patch('validation_workflow.validation.execute')
    @patch('validation_workflow.tar.validation_tar.ValidationArgs')
    def test_is_allow_with_security_exception(self, mock_validation_args: Mock, mock_execute: Mock) -> None:
        mock_execute.return_value = (0, "", "error")

        mock_validation_args.projects.return_value = ["opensearch"]
        mock_validation = ValidateTar(mock_validation_args.return_value)

        with self.assertRaises(Exception) as context:
            mock_validation.test_security_plugin("/bin/opensearch")

        self.assertEqual(str(context.exception), "Couldn't fetch the path to plugin folder")
