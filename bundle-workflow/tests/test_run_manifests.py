# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, call, patch

from run_manifests import main


class TestManifests(unittest.TestCase):
    @patch("argparse._sys.argv", ["manifests.py", "list"])
    @patch("run_manifests.logging", return_value=MagicMock())
    def test_main_list(self, mock_logging, *mocks):
        main()

        mock_logging.info.assert_has_calls(
            [
                call("OpenSearch 1.0.0"),
                call("OpenSearch 1.0.1"),
                call("OpenSearch 1.1.0"),
                call("OpenSearch 1.2.0"),
                call("OpenSearch 2.0.0"),
            ]
        )

        mock_logging.info.assert_has_calls([call("Done.")])
