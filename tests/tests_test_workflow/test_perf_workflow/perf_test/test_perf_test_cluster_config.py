# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest

from test_workflow.perf_test.perf_test_cluster_config import PerfTestClusterConfig


class TestPerfTestClusterConfig(unittest.TestCase):

    def test_default_args(self) -> None:
        config = PerfTestClusterConfig()
        self.assertEqual(config.security, False)
        self.assertEqual(config.data_nodes, 1)
        self.assertEqual(config.master_nodes, 0)
        self.assertEqual(config.ingest_nodes, 0)
        self.assertEqual(config.client_nodes, 0)
        self.assertEqual(config.is_single_node_cluster, True)
        self.assertEqual(config.use_50_percent_heap, "disable")

    def test_non_default_args(self) -> None:
        config = PerfTestClusterConfig(True, 1, 2, 3, 4, "enable")
        self.assertEqual(config.security, True)
        self.assertEqual(config.data_nodes, 1)
        self.assertEqual(config.master_nodes, 2)
        self.assertEqual(config.ingest_nodes, 3)
        self.assertEqual(config.client_nodes, 4)
        self.assertEqual(config.is_single_node_cluster, False)
        self.assertEqual(config.use_50_percent_heap, "enable")
