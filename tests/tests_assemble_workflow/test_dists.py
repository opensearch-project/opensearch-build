# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest

from assemble_workflow.dists import Dists
from manifests.build_manifest import BuildManifest


class TestDists(unittest.TestCase):

    def setUp(self) -> None:

        self.dists = Dists
        self.manifest_tar = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-linux-1.1.1.yml"))
        self.manifest_zip = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-windows-1.3.0.yml"))
        self.manifest_rpm = BuildManifest.from_path(os.path.join(os.path.dirname(__file__), "data/opensearch-build-rpm-1.3.0.yml"))

    def test_distribution_map(self) -> None:
        self.assertEqual(self.dists.DISTRIBUTIONS_MAP['tar'].cls.__name__, 'DistTar')
        self.assertEqual(self.dists.DISTRIBUTIONS_MAP['tar'].extension, '.tar.gz')
        self.assertEqual(self.dists.DISTRIBUTIONS_MAP['zip'].cls.__name__, 'DistZip')
        self.assertEqual(self.dists.DISTRIBUTIONS_MAP['zip'].extension, '.zip')
        self.assertEqual(self.dists.DISTRIBUTIONS_MAP['rpm'].cls.__name__, 'DistRpm')
        self.assertEqual(self.dists.DISTRIBUTIONS_MAP['rpm'].extension, '.rpm')

    def test_create_dist(self) -> None:
        return_cls_tar = self.dists.create_dist("OpenSearch", "artifacts/dist", "opensearch-1.3.0", self.manifest_tar.build)
        self.assertEqual(return_cls_tar.__class__.__name__, 'DistTar')
        return_cls_zip = self.dists.create_dist("OpenSearch", "artifacts/dist", "opensearch-1.3.0", self.manifest_zip.build)
        self.assertEqual(return_cls_zip.__class__.__name__, 'DistZip')
        return_cls_rpm = self.dists.create_dist("OpenSearch", "artifacts/dist", "opensearch-1.3.0", self.manifest_rpm.build)
        self.assertEqual(return_cls_rpm.__class__.__name__, 'DistRpm')
