# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from assemble_workflow.bundle_file_location import BundleFileLocation
from assemble_workflow.bundle_locations import BundleLocations
from assemble_workflow.bundle_url_location import BundleUrlLocation


class TestBundleLocations(unittest.TestCase):

    def test(self) -> None:
        self.assertIsInstance(
            BundleLocations.from_path("", "file", "opensearch", "tar"),
            BundleFileLocation
        )

        self.assertIsInstance(
            BundleLocations.from_path("https://ci.opensearch.org/ci/ci-env-prod/job-name-opensearch/", "file", "opensearch", "tar"),
            BundleUrlLocation
        )
