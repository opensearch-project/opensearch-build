# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from src.validation_workflow.validation_tar import ValidationTar


class TestValidationTar(unittest.TestCase):

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=True)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=True)
    def test_download_artifacts_true(self, download_utils_is_url_valid: Mock, download_utils_download: Mock) -> None:
        self.assertTrue(ValidationTar.download_artifacts(["opensearch", "opensearch-dashboards"], "2.3.0"), 1)

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=False)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=False)
    def test_download_artifacts_throws_exception(self, download_utils_is_url_valid: Mock, download_utils_download: Mock) -> None:
        self.assertRaises(Exception, ValidationTar.download_artifacts, ["opensearch", "opensearch-dashboards"], "1.6.0")
