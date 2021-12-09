# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from assemble_workflow.bundle_file_location import BundleFileLocation


class TestBundleFileLocation(unittest.TestCase):
    def test_opensearch(self) -> None:
        location = BundleFileLocation("dir", "opensearch")

        self.assertEqual(location.get_bundle_location("sql"), os.path.join("dir", "dist", "opensearch", "sql"))
        self.assertEqual(location.get_build_location("sql"), os.path.join("dir", "builds", "opensearch", "sql"))

    def test_opensearch_dashboards(self) -> None:
        location = BundleFileLocation("dir", "opensearch-dashboards")

        self.assertEqual(location.get_bundle_location("sql"), os.path.join("dir", "dist", "opensearch-dashboards", "sql"))
        self.assertEqual(location.get_build_location("sql"), os.path.join("dir", "builds", "opensearch-dashboards", "sql"))
