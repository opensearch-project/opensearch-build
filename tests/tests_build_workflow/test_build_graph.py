# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, call

from build_workflow.build_graph import BuildGraph


class TestBuildGraph(unittest.TestCase):

    def test_add_component_no_deps(self) -> None:
        graph = BuildGraph()
        graph.add_component("common-utils")
        graph.add_component("job-scheduler")
        self.assertEqual(graph.components, ["common-utils", "job-scheduler"])
        self.assertEqual(graph.dependencies["common-utils"], set())
        self.assertEqual(graph.dependencies["job-scheduler"], set())

    def test_add_component_with_deps(self) -> None:
        graph = BuildGraph()
        graph.add_component("common-utils")
        graph.add_component("security")
        graph.add_component("k-NN", ["common-utils", "security"])
        self.assertEqual(graph.dependencies["k-NN"], {"common-utils", "security"})
        self.assertEqual(graph.dependents["common-utils"], {"k-NN"})
        self.assertEqual(graph.dependents["security"], {"k-NN"})

    def test_add_component_ignores_deps_not_in_graph(self) -> None:
        graph = BuildGraph()
        graph.add_component("k-NN", ["common-utils", "security"])
        self.assertEqual(graph.dependencies["k-NN"], set())

    def test_add_component_partial_deps_in_graph(self) -> None:
        graph = BuildGraph()
        graph.add_component("common-utils")
        graph.add_component("k-NN", ["common-utils", "security"])
        self.assertEqual(graph.dependencies["k-NN"], {"common-utils"})

    def test_execute_parallel_returns_empty_on_success(self) -> None:
        graph = BuildGraph(max_workers=4)
        graph.add_component("common-utils")
        graph.add_component("job-scheduler")

        build_fn = MagicMock()
        failed = graph.execute_parallel(build_fn, required_components=[], continue_on_error=False)

        self.assertEqual(failed, [])
        build_fn.assert_has_calls([call("common-utils"), call("job-scheduler")], any_order=True)

    def test_execute_parallel_returns_failed_components(self) -> None:
        graph = BuildGraph(max_workers=4)
        graph.add_component("common-utils")
        graph.add_component("custom-codecs")

        build_fn = MagicMock(side_effect=lambda name: (_ for _ in ()).throw(Exception("fail")) if name == "custom-codecs" else None)

        failed = graph.execute_parallel(build_fn, required_components=[], continue_on_error=True)

        self.assertIn("custom-codecs", failed)
        self.assertNotIn("common-utils", failed)

    def test_execute_parallel_skips_dependents_on_failure(self) -> None:
        graph = BuildGraph(max_workers=4)
        graph.add_component("common-utils")
        graph.add_component("k-NN", ["common-utils"])
        graph.add_component("neural-search", ["k-NN"])

        build_fn = MagicMock(side_effect=lambda name: (_ for _ in ()).throw(Exception("fail")) if name == "common-utils" else None)

        failed = graph.execute_parallel(build_fn, required_components=[], continue_on_error=True)

        self.assertIn("common-utils", failed)
        self.assertIn("k-NN", failed)
        self.assertIn("neural-search", failed)

    def test_execute_parallel_raises_on_required_component_failure(self) -> None:
        graph = BuildGraph(max_workers=4)
        graph.add_component("common-utils")
        graph.add_component("security")

        build_fn = MagicMock(side_effect=lambda name: (_ for _ in ()).throw(Exception("common-utils failed")) if name == "common-utils" else None)

        with self.assertRaises(Exception) as ctx:
            graph.execute_parallel(build_fn, required_components=["common-utils"], continue_on_error=False)
        self.assertIn("common-utils failed", str(ctx.exception))

    def test_execute_parallel_does_not_raise_non_required_component_failure(self) -> None:
        graph = BuildGraph(max_workers=4)
        graph.add_component("common-utils")
        graph.add_component("custom-codecs")

        build_fn = MagicMock(side_effect=lambda name: (_ for _ in ()).throw(Exception("fail")) if name == "custom-codecs" else None)

        failed = graph.execute_parallel(build_fn, required_components=["common-utils"], continue_on_error=True)
        self.assertIn("custom-codecs", failed)
        self.assertNotIn("common-utils", failed)

    def test_execute_parallel_required_component_failure_raises_with_continue_on_error(self) -> None:
        graph = BuildGraph(max_workers=4)
        graph.add_component("common-utils")
        graph.add_component("job-scheduler")
        graph.add_component("security")

        build_fn = MagicMock(side_effect=lambda name: (_ for _ in ()).throw(Exception("common-utils failed")) if name == "common-utils" else None)

        with self.assertRaises(Exception) as ctx:
            graph.execute_parallel(build_fn, required_components=["common-utils", "job-scheduler"], continue_on_error=True)
        self.assertIn("common-utils failed", str(ctx.exception))

    def test_execute_parallel_non_required_component_failure_continues_with_continue_on_error(self) -> None:
        graph = BuildGraph(max_workers=4)
        graph.add_component("common-utils")
        graph.add_component("job-scheduler")
        graph.add_component("custom-codecs")
        graph.add_component("security")

        build_fn = MagicMock(side_effect=lambda name: (_ for _ in ()).throw(Exception("fail")) if name == "custom-codecs" else None)

        failed = graph.execute_parallel(build_fn, required_components=["common-utils", "job-scheduler"], continue_on_error=True)

        self.assertIn("custom-codecs", failed)
        self.assertNotIn("common-utils", failed)
        self.assertNotIn("job-scheduler", failed)
        self.assertNotIn("security", failed)
        build_fn.assert_any_call("common-utils")
        build_fn.assert_any_call("job-scheduler")
        build_fn.assert_any_call("security")

    def test_execute_parallel_respects_max_workers(self) -> None:
        graph = BuildGraph(max_workers=2)
        graph.add_component("common-utils")
        graph.add_component("job-scheduler")
        graph.add_component("security")
        graph.add_component("custom-codecs")

        build_fn = MagicMock()
        graph.execute_parallel(build_fn, required_components=[], continue_on_error=False)

        self.assertEqual(build_fn.call_count, 4)
