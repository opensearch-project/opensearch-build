# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from assemble_workflow.dist import Dist, DistTar, DistZip


class TestDist(unittest.TestCase):
    def test_from_path_tar_gz(self) -> None:
        dist = Dist.from_path("opensearch", "filename.tar.gz", "opensearch-1.1.0")
        self.assertIs(type(dist), DistTar)

    def test_from_path_zip(self) -> None:
        dist = Dist.from_path("opensearch", "filename.zip", "opensearch-1.1.0")
        self.assertIs(type(dist), DistZip)

    def test_from_path_invalid(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            Dist.from_path("opensearch", "filename.invalid", "opensearch-1.1.0")
        self.assertEqual(str(ctx.exception), 'Invalid min "dist" extension in input artifacts: .invalid (filename.invalid).')
