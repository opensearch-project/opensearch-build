# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from assemble_workflow.dist import Dist, DistRpm, DistTar, DistZip


class TestDist(unittest.TestCase):
    def test_create_dist_tar_gz(self) -> None:
        dist = Dist.create_dist("opensearch", "filename.tar.gz", "tar")
        self.assertIs(type(dist), DistTar)

    def test_create_dist_zip(self) -> None:
        dist = Dist.create_dist("opensearch", "filename.zip", "zip")
        self.assertIs(type(dist), DistZip)

    def test_create_dist_rpm(self) -> None:
        dist = Dist.create_dist("opensearch", "filename.rpm", "rpm")
        self.assertIs(type(dist), DistRpm)

    def test_create_dist_invalid(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Dist.create_dist("opensearch", "filename.invalid", "invalid")
        self.assertEqual(str(ctx.exception), 'Distribution not specified or invalid distribution')
