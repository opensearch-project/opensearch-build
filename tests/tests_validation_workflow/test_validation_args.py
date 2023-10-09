# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import unittest
from unittest.mock import patch

from validation_workflow.validation_args import ValidationArgs


class TestValidationArgs(unittest.TestCase):

    VALIDATION_PY = "./src/run_validation.py" \


    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "2.3.0"])
    def test_version(self) -> None:
        self.assertTrue(ValidationArgs().version)
        self.assertEqual(ValidationArgs().version, "2.3.0")
        self.assertNotEqual(ValidationArgs().version, "2.1.0")

    @patch("argparse._sys.argv", [VALIDATION_PY])
    def test_without_arguments(self) -> None:
        with self.assertRaises(Exception) as ctx:
            self.assertEqual(ValidationArgs().version, "")
            self.assertEqual(ValidationArgs().file_path, "")
        self.assertEqual(str(ctx.exception), "Provide either version number or File Path")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "2.1.0", "--distribution", "rpm"])
    def test_rpm_distribution(self) -> None:
        self.assertEqual(ValidationArgs().distribution, "rpm")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "2.4.0", "--distribution", "docker"])
    def test_docker_distribution(self) -> None:
        self.assertEqual(ValidationArgs().distribution, "docker")
        self.assertNotEqual(ValidationArgs().distribution, "yum")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "1.3.6", "--platform", "linux"])
    def test_platform_default(self) -> None:
        self.assertEqual(ValidationArgs().platform, "linux")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "1.3.6", "--os-build-number", "6039"])
    def test_os_build_number(self) -> None:
        self.assertEqual(ValidationArgs().os_build_number, "6039")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "1.3.6", "--osd-build-number", "4100"])
    def test_osd_build_number(self) -> None:
        self.assertNotEqual(ValidationArgs().osd_build_number, "4104")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "1.3.0"])
    def test_verbose_default(self) -> None:
        self.assertEqual(ValidationArgs().logging_level, logging.INFO)

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "1.3.0", "--verbose"])
    def test_verbose_true(self) -> None:
        self.assertTrue(ValidationArgs().logging_level, logging.DEBUG)

    @patch("argparse._sys.argv", [VALIDATION_PY, "--file-path", "opensearch=https://opensearch.org/releases/opensearch/2.8.0/opensearch-2.8.0-linux-x64.rpm"])
    def test_file_path(self) -> None:
        self.assertNotEqual(ValidationArgs().file_path, "opensearch=https://opensearch.org/releases/opensearch/2.8.0/opensearch-2.8.0-linux-x64.rpm")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "1.3.6", "--distribution", "rpm", "--artifact-type", "staging", "--os-build-number", "1234", "--osd-build-number", "2312"])
    def test_artifact_type(self) -> None:
        self.assertNotEqual(ValidationArgs().artifact_type, "production")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--version", "1.3.0", "--projects", "opensearch"])
    def test_set_projects(self) -> None:
        self.assertEqual(ValidationArgs().projects, ["opensearch"])

    @patch("argparse._sys.argv", [VALIDATION_PY, "--file-path", "opensearch-dashboards=https://opensearch.org/releases/opensearch/2.8.0/opensearch-dashboards-2.8.0-linux-x64.rpm"])
    def test_projects_exception(self) -> None:
        with self.assertRaises(Exception) as ctx:
            self.assertEqual(ValidationArgs().distribution, "rpm")
            self.assertEqual(ValidationArgs().projects, ["opensearch-dashboards"])
        self.assertEqual(str(ctx.exception), "Missing OpenSearch OpenSearch artifact details! Please provide the same along with OpenSearch-Dashboards to validate")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--file-path", "opensearch=https://opensearch.org/releases/opensearch/2.8.0/opensearch-2.8.0-linux-x64.zip"])
    def test_file_path_distribution_type(self) -> None:
        with self.assertRaises(Exception) as ctx:
            self.assertEqual(ValidationArgs().projects, ["opensearch"])
        self.assertEqual(str(ctx.exception), "Provided distribution is not supported")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--file-path", "opensearch=https://opensearch.org/releases/opensearch/2.8.0/opensearch-2.8.0-linux-x64.tar.gz"])
    def test_get_distribution_type_tar(self) -> None:
        result = ValidationArgs().get_distribution_type(ValidationArgs().file_path)
        self.assertEqual(result, "tar")

    @patch("argparse._sys.argv", [VALIDATION_PY, "--file-path", "opensearch=https://opensearch.org/releases/opensearch/2.8.0/opensearch-2.x.staging.repo "])
    def test_get_distribution_type_yum(self) -> None:
        result = ValidationArgs().get_distribution_type(ValidationArgs().file_path)
        self.assertEqual(result, "yum")
