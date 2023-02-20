# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import Mock, patch

from validation_workflow.validation_rpm import ValidationRpm


class TestValidationRpm(unittest.TestCase):

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=True)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=True)
    def test_download_artifacts_true(self, download_utils_is_url_valid: Mock, download_utils_download: Mock) -> None:
        self.assertTrue(ValidationRpm.download_artifacts(["opensearch", "opensearch-dashboards"], "2.1.0"), 1)

    @patch("validation_workflow.download_utils.DownloadUtils.is_url_valid", return_value=True)
    @patch("validation_workflow.download_utils.DownloadUtils.download", return_value=False)
    def test_download_artifacts_throws_exception(self, download_utils_is_url_valid: Mock, download_utils_download: Mock) -> None:
        self.assertRaises(Exception, ValidationRpm.download_artifacts, ["opensearch", "opensearch-dashboards"], "2.11.0")
