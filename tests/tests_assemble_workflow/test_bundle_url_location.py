# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from assemble_workflow.bundle_url_location import BundleUrlLocation


class TestBundleUrlLocation(unittest.TestCase):
    def test_opensearch(self) -> None:
        location = BundleUrlLocation("https://ci.opensearch.org/ci/dbc/bundle-build/1.3.0/1318/linux/x64", "opensearch")

        self.assertEqual(
            location.get_bundle_location("sql"),
            "https://ci.opensearch.org/ci/dbc/bundle-build/1.3.0/1318/linux/x64/dist/opensearch/sql"
        )

        self.assertEqual(
            location.get_build_location("sql"),
            "https://ci.opensearch.org/ci/dbc/bundle-build/1.3.0/1318/linux/x64/builds/opensearch/sql"
        )

    def test_opensearch_tailing_slash(self) -> None:
        location = BundleUrlLocation("https://ci.opensearch.org/ci/dbc/bundle-build/1.3.0/1318/linux/x64/", "opensearch")

        self.assertEqual(
            location.get_bundle_location("sql"),
            "https://ci.opensearch.org/ci/dbc/bundle-build/1.3.0/1318/linux/x64/dist/opensearch/sql"
        )

        self.assertEqual(
            location.get_build_location("sql"),
            "https://ci.opensearch.org/ci/dbc/bundle-build/1.3.0/1318/linux/x64/builds/opensearch/sql"
        )

    def test_opensearch_dashboards(self) -> None:
        location = BundleUrlLocation("https://ci.opensearch.org/ci/dbc/bundle-build/1.3.0/1318/linux/x64", "opensearch-dashboards")

        self.assertEqual(
            location.get_bundle_location("sql"),
            "https://ci.opensearch.org/ci/dbc/bundle-build/1.3.0/1318/linux/x64/dist/opensearch-dashboards/sql"
        )

        self.assertEqual(
            location.get_build_location("sql"),
            "https://ci.opensearch.org/ci/dbc/bundle-build/1.3.0/1318/linux/x64/builds/opensearch-dashboards/sql"
        )
