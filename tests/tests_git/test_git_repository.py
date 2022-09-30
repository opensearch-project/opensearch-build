# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess
import unittest
from typing import Any
from unittest.mock import Mock, patch

from git.git_repository import GitRepository
from system.temporary_directory import TemporaryDirectory


class TestGitRepository(unittest.TestCase):

    @patch('subprocess.check_call', return_value=0)
    @patch('subprocess.check_output', return_value='8ac515431bf24caf92fea9d9b0af3b8f10b88453'.encode())
    def setUp(self, *mocks: Any) -> None:
        self.repo = GitRepository(
            url="https://github.com/opensearch-project/.github",
            ref="8ac515431bf24caf92fea9d9b0af3b8f10b88453",
        )

    def test_checkout(self) -> None:
        self.assertEqual(self.repo.url, "https://github.com/opensearch-project/.github")
        self.assertEqual(self.repo.ref, "8ac515431bf24caf92fea9d9b0af3b8f10b88453")
        self.assertEqual(self.repo.sha, "8ac515431bf24caf92fea9d9b0af3b8f10b88453")
        self.assertIs(type(self.repo.temp_dir), TemporaryDirectory)
        self.assertEqual(self.repo.dir, os.path.realpath(self.repo.temp_dir.name))

    def test_execute(self) -> None:
        self.repo.execute("echo $PWD > created.txt")
        self.assertTrue(os.path.isfile(os.path.join(self.repo.dir, "created.txt")))

    @patch('subprocess.check_call', return_value=0)
    def test_execute_in_subdir(self, mock_check_call: Mock) -> None:
        subdir = os.path.join(self.repo.dir, "ISSUE_TEMPLATE")
        self.repo.execute("echo $PWD > created.txt", subdir)
        mock_check_call.assert_called_with('echo $PWD > created.txt', cwd=subdir, shell=True)

    @patch("subprocess.check_call")
    def test_execute_silent(self, mock_subprocess: Mock) -> None:
        self.repo.execute_silent("echo .")
        mock_subprocess.assert_called_with(
            "echo .",
            cwd=self.repo.dir,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    @patch("subprocess.check_output")
    def test_output(self, mock_subprocess: Any) -> None:
        self.repo.output("echo hello")
        mock_subprocess.assert_called_with("echo hello", cwd=self.repo.dir, shell=True)

    @patch("subprocess.check_output", return_value='927de30 2022-07-12'.encode())
    def test_log(self, mock_subprocess: Any) -> None:
        log = self.repo.log('2021-10-26')
        last_commit = log[-1]
        self.assertEqual(last_commit.id, "927de30")
        self.assertEqual(last_commit.date, "2022-07-12")

    @patch("subprocess.check_output", return_value=''.encode())
    def test_log_empty(self, mock_subprocess: Any) -> None:
        log = self.repo.log('2021-10-26')
        self.assertEqual(len(log), 0)

    @patch("subprocess.check_output", return_value='927de30 2022-07-12\n787d971 2022-04-28\n989143e 22-04-26\n8b376fc 2022-04-26\n023a2ac 2022-04-26'.encode())
    def test_log_multiple(self, mock_subprocess: Any) -> None:
        log = self.repo.log('2022-04-25')
        self.assertEqual(len(log), 5)
        last_commit = log[-1]
        self.assertEqual(last_commit.id, "023a2ac")
        self.assertEqual(last_commit.date, "2022-04-26")


class TestGitRepositoryDir(unittest.TestCase):
    @patch('subprocess.check_call', return_value=0)
    @patch('subprocess.check_output', return_value='8ac515431bf24caf92fea9d9b0af3b8f10b88453'.encode())
    def test_checkout_into_dir(self, *mocks: Any) -> None:
        with TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir.name, ".github")
            repo = GitRepository(
                url="https://github.com/opensearch-project/.github",
                ref="8ac515431bf24caf92fea9d9b0af3b8f10b88453",
                directory=subdir,
            )

            self.assertEqual(repo.url, "https://github.com/opensearch-project/.github")
            self.assertEqual(repo.ref, "8ac515431bf24caf92fea9d9b0af3b8f10b88453")
            self.assertEqual(repo.sha, "8ac515431bf24caf92fea9d9b0af3b8f10b88453")
            self.assertIsNone(repo.temp_dir)
            self.assertEqual(repo.dir, subdir)


class TestGitRepositoryWithWorkingDir(unittest.TestCase):
    @patch('subprocess.check_call', return_value=0)
    @patch('subprocess.check_output', return_value='8ac515431bf24caf92fea9d9b0af3b8f10b88453'.encode())
    def test_checkout_into_dir(self, *mocks: Any) -> None:
        with GitRepository(
            url="https://github.com/opensearch-project/.github",
            ref="163b5acaf6c7d220f800684801bbf2e12f99c797",
            working_subdirectory="ISSUE_TEMPLATE",
        ) as repo:
            working_directory = os.path.join(repo.dir, "ISSUE_TEMPLATE")
            self.assertEqual(repo.working_directory, working_directory)
        self.assertFalse(os.path.exists(repo.dir))


class TestGitRepositoryClassMethods(unittest.TestCase):
    @patch("subprocess.check_output", return_value="sha\tHEAD".encode())
    def test_stable_ref(self, mock_output: Mock) -> None:
        ref, name = GitRepository.stable_ref("https://github.com/opensearch-project/OpenSearch", "sha")
        self.assertEqual(ref, "sha")
        self.assertEqual(name, "HEAD")

    @patch("subprocess.check_output", return_value="".encode())
    def test_stable_ref_none(self, mock_output: Mock) -> None:
        ref, name = GitRepository.stable_ref("https://github.com/opensearch-project/OpenSearch", "sha")
        self.assertEqual(ref, "sha")
        self.assertEqual(name, "sha")
