# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import logging
import os
import unittest
from unittest.mock import patch

from report_workflow.report_args import ReportArgs


class TestReportArgs(unittest.TestCase):

    ARGS_PY = os.path.realpath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "src", "run_test_report.py"
        )
    )

    PATH = os.path.join(
        os.path.dirname(__file__), "data"
    )

    TEST_MANIFEST_PATH = os.path.join(
        os.path.dirname(__file__), "data", "test_manifest.yml"
    )

    TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH = os.path.join(
        os.path.dirname(__file__), "data", "test-manifest-opensearch-dashboards.yml"
    )

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH])
    def test_opensearch_default_with_opensearch_test_manifest(self) -> None:
        report_args = ReportArgs()
        self.assertFalse(hasattr(report_args, "opensearch"))
        self.assertFalse(hasattr(report_args, "opensearch-dashboards"))

        self.assertIsNone(report_args.test_run_id)
        self.assertIsNone(report_args.components)
        self.assertIsNotNone(report_args.test_type)
        self.assertEqual(report_args.logging_level, logging.INFO)
        self.assertEqual(report_args.test_manifest_path, self.TEST_MANIFEST_PATH)

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--component", "component1", "component2"])
    def test_components(self) -> None:
        report_args = ReportArgs()
        self.assertEqual(report_args.components, ["component1", "component2"])

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--artifact-paths", "opensearch=" + TEST_MANIFEST_PATH])
    def test_opensearch_file_with_opensearch_test_manifest(self) -> None:
        report_args = ReportArgs()
        self.assertEqual(report_args.artifact_paths.get("opensearch"), os.path.realpath(self.TEST_MANIFEST_PATH))
        self.assertFalse(hasattr(report_args.artifact_paths, "opensearch-dashboards"))

        self.assertIsNone(report_args.test_run_id)
        self.assertIsNone(report_args.components)
        self.assertEqual(report_args.test_type, "integ-test")
        self.assertEqual(report_args.logging_level, logging.INFO)
        self.assertEqual(report_args.test_manifest_path, self.TEST_MANIFEST_PATH)

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--artifact-paths", "opensearch=https://ci.opensearch.org/x/y", "--verbose"])
    def test_opensearch_url_with_opensearch_test_manifest(self) -> None:
        report_args = ReportArgs()
        self.assertEqual(report_args.artifact_paths.get("opensearch"), "https://ci.opensearch.org/x/y")
        self.assertFalse(hasattr(report_args.artifact_paths, "opensearch-dashboards"))
        self.assertEqual(report_args.test_manifest_path, self.TEST_MANIFEST_PATH)

        self.assertIsNone(report_args.test_run_id)
        self.assertIsNone(report_args.components)
        self.assertEqual(report_args.test_type, "integ-test")
        self.assertEqual(report_args.logging_level, logging.DEBUG)

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH, "--artifact-paths", "opensearch-dashboards=" + TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH])
    def test_opensearch_dashboards_default_with_opensearch_dashboards_test_manifest(self) -> None:
        report_args = ReportArgs()
        self.assertFalse(hasattr(report_args.artifact_paths, "opensearch"))
        self.assertEqual(report_args.artifact_paths.get("opensearch-dashboards"), self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH)

        self.assertIsNone(report_args.test_run_id)
        self.assertIsNone(report_args.components)
        self.assertEqual(report_args.test_type, "integ-test")
        self.assertEqual(report_args.logging_level, logging.INFO)
        self.assertEqual(report_args.test_manifest_path, self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH)

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH, "--artifact-paths",
                                  "opensearch-dashboards=https://ci.opensearch.org/x/y", "opensearch=https://ci.opensearch.org/x/y/z"])
    def test_opensearch_dashboards_url_with_opensearch_dashboards_test_manifest(self) -> None:
        report_args = ReportArgs()
        self.assertEqual(report_args.artifact_paths.get("opensearch-dashboards"), "https://ci.opensearch.org/x/y")
        self.assertEqual(report_args.artifact_paths.get("opensearch"), "https://ci.opensearch.org/x/y/z")

        self.assertIsNone(report_args.test_run_id)
        self.assertIsNone(report_args.components)
        self.assertEqual(report_args.test_type, "integ-test")
        self.assertEqual(report_args.logging_level, logging.INFO)
        self.assertEqual(report_args.test_manifest_path, self.TEST_MANIFEST_OPENSEARCH_DASHBOARDS_PATH)

    @patch("argparse._sys.argv", [ARGS_PY, TEST_MANIFEST_PATH, "--artifact-paths", "opensearch=https://ci.opensearch.org/x/y/z", "--test-run-id", "6"])
    def test_run_id(self) -> None:
        report_args = ReportArgs()
        self.assertEqual(report_args.test_run_id, 6)
        self.assertEqual(report_args.test_manifest_path, self.TEST_MANIFEST_PATH)
        self.assertEqual(report_args.artifact_paths.get("opensearch"), "https://ci.opensearch.org/x/y/z")

    @patch(
        "argparse._sys.argv",
        [ARGS_PY,
         TEST_MANIFEST_PATH,
         "--artifact-paths",
         "opensearch-dashboards=https://ci.opensearch.org/x/y",
         "opensearch=https://ci.opensearch.org/x/y/z",
         "--base-path", "https://ci.opensearch.org/ci/dbc/integ-test/",
         "--test-run-id", "1234"])
    def test_base_path(self) -> None:
        report_args = ReportArgs()
        self.assertEqual(report_args.base_path, "https://ci.opensearch.org/ci/dbc/integ-test/")
        self.assertEqual(report_args.test_manifest_path, self.TEST_MANIFEST_PATH)
        self.assertEqual(report_args.artifact_paths.get("opensearch-dashboards"), "https://ci.opensearch.org/x/y")
        self.assertEqual(report_args.artifact_paths.get("opensearch"), "https://ci.opensearch.org/x/y/z")
        self.assertEqual(report_args.test_type, "integ-test")
        self.assertEqual(report_args.test_run_id, 1234)
