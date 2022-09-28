# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from ci_workflow.ci_check_list_source_ref import CiCheckListSourceRef
from manifests.input_manifest import InputComponentFromSource


class TestCiCheckListsSourceRef(unittest.TestCase):
    @patch("subprocess.check_output", return_value="invalid".encode())
    def test_ref_does_not_exist(self, mock_check_output: MagicMock) -> None:
        component = InputComponentFromSource({"name": "common-utils", "repository": "url", "ref": "ref"})
        with self.assertRaises(CiCheckListSourceRef.MissingRefError) as ctx:
            list = CiCheckListSourceRef(component, MagicMock())
            list.check()
        self.assertEqual("Missing url@ref.", str(ctx.exception))
        mock_check_output.assert_called_with("git ls-remote url ref", shell=True)

    @patch("subprocess.check_output", return_value="valid\tref".encode())
    def test_ref_exists(self, mock_check_output: MagicMock) -> None:
        component = InputComponentFromSource({"name": "common-utils", "repository": "url", "ref": "ref"})
        list = CiCheckListSourceRef(component, MagicMock())
        list.check()
        mock_check_output.assert_called_with("git ls-remote url ref", shell=True)
