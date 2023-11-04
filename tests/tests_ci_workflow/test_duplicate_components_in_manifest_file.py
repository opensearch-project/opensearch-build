# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from ci_workflow.ci_manifests import CiManifests


class TestDuplicateComponentsInManifestFile(unittest.TestCase):
    def test_duplicate_components_in_manifest_file(self) -> None:
        data_path = os.path.join(os.path.dirname(__file__), "data")
        manifest_filename = os.path.join(data_path, 'opensearch-1.3.11-with-duplicates.yml')
        with self.assertRaises(ValueError) as valueErrorException:
            with open(manifest_filename, 'r') as manifest_file:
                CiManifests.from_file(manifest_file, None)
        self.assertTrue(
            "Found sql, k-NN, performance-analyzer, opensearch-observability, anomaly-detection, "
            "index-management as a duplicate component(s) in manifest "
            + manifest_filename
            in str(valueErrorException.exception))
