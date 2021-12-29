# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import Mock, patch

from ci_workflow.ci_check_list_dist import CiCheckListDist
from ci_workflow.ci_target import CiTarget
from manifests.build_manifest import BuildManifest
from manifests.input_manifest import InputComponentFromDist


class TestCiCheckListsDist(unittest.TestCase):
    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUILD_MANIFEST = os.path.join(DATA, "opensearch-1.1.0-x64-build-manifest.yml")

    @patch("manifests.distribution.find_build_root")
    @patch("manifests.build_manifest.BuildManifest.from_url")
    def test_check(self, mock_manifest_from_url: Mock, find_build_root: Mock):
        mock_manifest_from_url.return_value = BuildManifest.from_path(self.BUILD_MANIFEST)
        component = InputComponentFromDist({
            "name": "common-utils",
            "dist": "url",
            "checks": ["manifest:component"]
        })
        list = CiCheckListDist(component, CiTarget(version="1.1.0", name="opensearch", snapshot=True))
        list.check()
        mock_manifest_from_url.assert_called()
        find_build_root.assert_called()

    def test_invalid_check(self, *mocks):
        component = InputComponentFromDist({
            "name": "common-utils",
            "dist": "url",
            "checks": ["invalid:check"]
        })
        list = CiCheckListDist(component, CiTarget(version="1.1.0", name="opensearch", snapshot=True))
        list.checkout("path")
        with self.assertRaises(CiCheckListDist.InvalidCheckError) as ctx:
            list.check()
        self.assertTrue(str(ctx.exception).startswith("Invalid check: invalid:check"))
