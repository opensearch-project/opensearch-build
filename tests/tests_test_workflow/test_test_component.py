# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import os
import unittest
from unittest.mock import Mock, patch

from system.temporary_directory import TemporaryDirectory
from test_workflow.test_component import TestComponent


class TestTestComponent(unittest.TestCase):
    def setUp(self) -> None:
        self.test_component = TestComponent(
            "https://github.com/opensearch-project/.github",
            "8ac515431bf24caf92fea9d9b0af3b8f10b88453",
        )

    @patch("test_workflow.test_component.GitRepository")
    def test_checkout(self, mock_repo: Mock) -> None:
        with TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir.name, ".github")
            repo = self.test_component.checkout(subdir)
            self.assertEqual(repo, mock_repo.return_value)
            mock_repo.assert_called_with(
                "https://github.com/opensearch-project/.github",
                "8ac515431bf24caf92fea9d9b0af3b8f10b88453",
                subdir
            )
