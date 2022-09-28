# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import itertools
import os
import unittest

from paths.tree_walker import walk


class TestTreeWalker(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        self.data_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "data"))

    def test_walk(self) -> None:
        paths = sorted(list(itertools.chain(walk(self.data_path))), key=lambda path: path[0])  # type: ignore
        self.assertTrue(len(paths), 7)
        self.assertEqual(
            paths[0][1],
            os.path.join("git", "component-with-scripts-folder", "scripts", "build.sh"),
        )
        self.assertEqual(
            paths[0][0],
            os.path.realpath(
                os.path.join(
                    self.data_path,
                    os.path.join("git", "component-with-scripts-folder", "scripts", "build.sh"),
                )
            ),
        )
