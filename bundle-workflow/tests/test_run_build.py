# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from unittest.mock import MagicMock, call, patch

from run_build import main


class TestBuild(unittest.TestCase):
    OPENSEARCH_MANIFEST = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__), "../../manifests/1.1.0/opensearch-1.1.0.yml"
        )
    )

    @patch("argparse._sys.argv", ["run_build.py", OPENSEARCH_MANIFEST])
    @patch("run_build.Builder", return_value=MagicMock())
    @patch("run_build.BuildRecorder", return_value=MagicMock())
    @patch("run_build.GitRepository", return_value=MagicMock(working_directory="dummy"))
    @patch("run_build.TemporaryDirectory")
    def test_main(self, mock_temp, mock_repo, mock_recorder, mock_builder, *mocks):
        mock_temp.return_value.__enter__.return_value = tempfile.gettempdir()

        main()

        # each repository is checked out locally
        mock_repo.assert_has_calls(
            [
                call(
                    "https://github.com/opensearch-project/OpenSearch.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "OpenSearch"),
                    None,
                ),
                call(
                    "https://github.com/opensearch-project/common-utils.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "common-utils"),
                    None,
                ),
                call(
                    "https://github.com/opensearch-project/dashboards-reports.git",
                    "1.1",
                    os.path.join(tempfile.gettempdir(), "dashboards-reports"),
                    "reports-scheduler",
                ),
            ],
            any_order=True,
        )

        self.assertEqual(mock_repo.call_count, 14)

        # each component is built and its artifacts exported
        mock_builder.assert_has_calls(
            [
                call("OpenSearch", mock_repo.return_value, mock_recorder.return_value),
                call(
                    "common-utils", mock_repo.return_value, mock_recorder.return_value
                ),
                call(
                    "dashboards-reports",
                    mock_repo.return_value,
                    mock_recorder.return_value,
                ),
            ],
            any_order=True,
        )

        self.assertEqual(mock_builder.call_count, 14)
        self.assertEqual(mock_builder.return_value.build.call_count, 14)
        self.assertEqual(mock_builder.return_value.export_artifacts.call_count, 14)

        # the output manifest is written
        mock_recorder.return_value.write_manifest.assert_called()
