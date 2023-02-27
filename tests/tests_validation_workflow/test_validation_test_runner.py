# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from unittest.mock import MagicMock, patch

from validation_workflow.validation_test_runner import ValidationTestRunner  # type: ignore


class TestValidationTestRunner(unittest.TestCase):
    def test_docker(self) -> None:
        mock_args = MagicMock()
        mock_dist = "docker"
        mock_docker_runner_object = MagicMock()
        mock_docker_runner = MagicMock()
        mock_docker_runner.return_value = mock_docker_runner_object
        mock_tar_runner = MagicMock()
        mock_rpm_runner = MagicMock()
        mock_yum_runner = MagicMock()
        with patch.dict("validation_workflow.validation_test_runner.ValidationTestRunner.RUNNERS", {
            "docker": mock_docker_runner,
            "tar": mock_tar_runner,
            "rpm": mock_rpm_runner,
            "yum": mock_yum_runner,
        }):
            runner = ValidationTestRunner.dispatch(mock_args, mock_dist)
            self.assertEqual(runner, mock_docker_runner_object)
            mock_docker_runner.assert_called_once_with(mock_args)

    def test_tar(self) -> None:
        mock_args = MagicMock()
        mock_dist = "tar"
        mock_tar_runner_object = MagicMock()
        mock_docker_runner = MagicMock()
        mock_tar_runner = MagicMock()
        mock_tar_runner.return_value = mock_tar_runner_object
        mock_rpm_runner = MagicMock()
        mock_yum_runner = MagicMock()
        with patch.dict("validation_workflow.validation_test_runner.ValidationTestRunner.RUNNERS", {
            "docker": mock_docker_runner,
            "tar": mock_tar_runner,
            "rpm": mock_rpm_runner,
            "yum": mock_yum_runner,
        }):
            runner = ValidationTestRunner.dispatch(mock_args, mock_dist)
            self.assertEqual(runner, mock_tar_runner_object)
            mock_tar_runner.assert_called_once_with(mock_args)

    def test_rpm(self) -> None:
        mock_args = MagicMock()
        mock_dist = "rpm"
        mock_rpm_runner_object = MagicMock()
        mock_docker_runner = MagicMock()
        mock_tar_runner = MagicMock()
        mock_rpm_runner = MagicMock()
        mock_rpm_runner.return_value = mock_rpm_runner_object
        mock_yum_runner = MagicMock()
        with patch.dict("validation_workflow.validation_test_runner.ValidationTestRunner.RUNNERS", {
            "docker": mock_docker_runner,
            "tar": mock_tar_runner,
            "rpm": mock_rpm_runner,
            "yum": mock_yum_runner,
        }):
            runner = ValidationTestRunner.dispatch(mock_args, mock_dist)
            self.assertEqual(runner, mock_rpm_runner_object)
            mock_rpm_runner.assert_called_once_with(mock_args)

    def test_yum(self) -> None:
        mock_args = MagicMock()
        mock_dist = "yum"
        mock_yum_runner_object = MagicMock()
        mock_docker_runner = MagicMock()
        mock_tar_runner = MagicMock()
        mock_rpm_runner = MagicMock()
        mock_yum_runner = MagicMock()
        mock_yum_runner.return_value = mock_yum_runner_object
        with patch.dict("validation_workflow.validation_test_runner.ValidationTestRunner.RUNNERS", {
            "docker": mock_docker_runner,
            "tar": mock_tar_runner,
            "rpm": mock_rpm_runner,
            "yum": mock_yum_runner,
        }):
            runner = ValidationTestRunner.dispatch(mock_args, mock_dist)
            self.assertEqual(runner, mock_yum_runner_object)
            mock_yum_runner.assert_called_once_with(mock_args)


if __name__ == '__main__':
    unittest.main()
