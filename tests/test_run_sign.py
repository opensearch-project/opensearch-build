# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

import pytest

from run_sign import main


class TestRunSign(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def capfd(self, capfd):
        self.capfd = capfd

    @patch("argparse._sys.argv", ["run_sign.py", "--help"])
    def test_usage(self, *mocks):
        with self.assertRaises(SystemExit):
            main()

        out, _ = self.capfd.readouterr()
        self.assertTrue(out.startswith("usage:"))

    DATA_PATH = os.path.join(os.path.dirname(__file__), "data")

    BUILD_MANIFEST = os.path.join(DATA_PATH, "opensearch-build-1.1.0.yml")

    @patch("os.getcwd", return_value="curdir")
    @patch("argparse._sys.argv", ["run_sign.py", BUILD_MANIFEST])
    @patch("run_sign.Signer", return_value=MagicMock())
    def test_main(self, mock_signer, *mocks):
        main()

        self.assertEqual(mock_signer.return_value.sign_artifacts.call_count, 21)
        mock_signer.return_value.sign_artifacts.assert_has_calls(
            [
                call(
                    [
                        "maven/org/opensearch/common-utils/maven-metadata-local.xml",
                        "maven/org/opensearch/common-utils/1.1.0.0/common-utils-1.1.0.0-javadoc.jar",
                        "maven/org/opensearch/common-utils/1.1.0.0/common-utils-1.1.0.0-sources.jar",
                        "maven/org/opensearch/common-utils/1.1.0.0/common-utils-1.1.0.0.pom",
                        "maven/org/opensearch/common-utils/1.1.0.0/common-utils-1.1.0.0.jar",
                    ],
                    self.DATA_PATH,
                )
            ]
        )
        mock_signer.return_value.sign_artifacts.assert_has_calls([call(["plugins/opensearch-index-management-1.1.0.0.zip"], self.DATA_PATH)])
