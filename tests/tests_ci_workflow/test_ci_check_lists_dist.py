# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, patch

from ci_workflow.ci_check_list_dist import CiCheckListDist
from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputComponentFromDist


class TestCiCheckListsDist(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUILD_MANIFEST = os.path.join(DATA, "opensearch-1.1.0-x64-build-manifest.yml")

    @patch("manifests.build_manifest.BuildManifest.from_url")
    def test_check(self, mock_manifest, *mocks):
        mock_manifest.return_value = BuildManifest.from_path(self.BUILD_MANIFEST)
        component = InputComponentFromDist({
            "name": "common-utils",
            "dist": "url",
            "checks": ["manifest:component"]
        })
        list = CiCheckListDist(component, MagicMock())
        list.check()
        mock_manifest.assert_called()

    def test_invalid_check(self, *mocks):
        component = InputComponentFromDist({
            "name": "common-utils",
            "dist": "url",
            "checks": ["invalid:check"]
        })
        list = CiCheckListDist(component, MagicMock())
        list.checkout("path")
        with self.assertRaises(CiCheckListDist.InvalidCheckError) as ctx:
            list.check()
        self.assertTrue(str(ctx.exception).startswith("Invalid check: invalid:check"))
