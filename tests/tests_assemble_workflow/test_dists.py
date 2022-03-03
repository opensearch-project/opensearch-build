# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from assemble_workflow.dists import Dists


class TestDists(unittest.TestCase):

    def setUp(self) -> None:

        self.dists = Dists

    def test_distribution_map(self) -> None:
        self.assertEqual(self.dists.DISTRIBUTIONS_MAP['tar'].cls.__name__, 'DistTar')
        self.assertEqual(self.dists.DISTRIBUTIONS_MAP['tar'].extension, '.tar.gz')
        self.assertEqual(self.dists.DISTRIBUTIONS_MAP['zip'].cls.__name__, 'DistZip')
        self.assertEqual(self.dists.DISTRIBUTIONS_MAP['zip'].extension, '.zip')

    def test_create_dist(self) -> None:
        return_cls_tar = self.dists.create_dist("OpenSearch", "artifacts/dist", "opensearch-1.3.0", 'tar')
        self.assertEqual(return_cls_tar.__class__.__name__, 'DistTar')
        return_cls_zip = self.dists.create_dist("OpenSearch", "artifacts/dist", "opensearch-1.3.0", 'zip')
        self.assertEqual(return_cls_zip.__class__.__name__, 'DistZip')
