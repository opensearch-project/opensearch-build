# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess
import unittest
from unittest.mock import patch

from git.git_repository import GitRepository
from system.temporary_directory import TemporaryDirectory


class TestGitRepository(unittest.TestCase):
    def setUp(self):
        self.repo = GitRepository(
            url="https://github.com/opensearch-project/.github",
            ref="8ac515431bf24caf92fea9d9b0af3b8f10b88453",
        )

    def test_checkout(self):
        self.assertEqual(self.repo.url, "https://github.com/opensearch-project/.github")
        self.assertEqual(self.repo.ref, "8ac515431bf24caf92fea9d9b0af3b8f10b88453")
        self.assertEqual(self.repo.sha, "8ac515431bf24caf92fea9d9b0af3b8f10b88453")
        self.assertIs(type(self.repo.temp_dir), TemporaryDirectory)
        self.assertEqual(self.repo.dir, os.path.realpath(self.repo.temp_dir.name))
        self.assertTrue(os.path.isfile(os.path.join(self.repo.dir, "CODE_OF_CONDUCT.md")))
        # was added in the next commit
        self.assertFalse(os.path.exists(os.path.join(self.repo.dir, "CONTRIBUTING.md")))

    def test_execute(self):
        self.repo.execute("echo $PWD > created.txt")
        self.assertTrue(os.path.isfile(os.path.join(self.repo.dir, "created.txt")))

    def test_execute_in_dir(self):
        self.repo.execute("echo $PWD > created.txt", os.path.join(self.repo.dir, "ISSUE_TEMPLATE"))
        self.assertFalse(os.path.isfile(os.path.join(self.repo.dir, "created.txt")))
        self.assertTrue(os.path.isfile(os.path.join(self.repo.dir, "ISSUE_TEMPLATE", "created.txt")))

    @patch("subprocess.check_call")
    def test_execute_silent(self, mock_subprocess):
        self.repo.execute_silent("echo .")
        subprocess.check_call.assert_called_with(
            "echo .",
            cwd=self.repo.dir,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    @patch("subprocess.check_output")
    def test_output(self, mock_subprocess):
        self.repo.output("echo hello")
        subprocess.check_output.assert_called_with("echo hello", cwd=self.repo.dir, shell=True)


class TestGitRepositoryDir(unittest.TestCase):
    def test_checkout_into_dir(self):
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
            self.assertTrue(os.path.isfile(os.path.join(repo.dir, "CODE_OF_CONDUCT.md")))


class TestGitRepositoryWithWorkingDir(unittest.TestCase):
    def test_checkout_into_dir(self):
        with GitRepository(
            url="https://github.com/opensearch-project/.github",
            ref="163b5acaf6c7d220f800684801bbf2e12f99c797",
            working_subdirectory="ISSUE_TEMPLATE",
        ) as repo:
            working_directory = os.path.join(repo.dir, "ISSUE_TEMPLATE")
            self.assertEqual(repo.working_directory, working_directory)
            self.assertTrue("ISSUE_TEMPLATE" in repo.output("pwd"))
        self.assertFalse(os.path.exists(repo.dir))


class TestGitRepositoryClassMethods(unittest.TestCase):
    @patch("subprocess.check_output")
    def test_stable_ref(self, mock_output):
        mock_output.return_value.decode.return_value = "sha\tHEAD"
        ref, name = GitRepository.stable_ref("https://github.com/opensearch-project/OpenSearch", "sha")
        self.assertEqual(ref, "sha")
        self.assertEqual(name, "HEAD")

    @patch("subprocess.check_output")
    def test_stable_ref_none(self, mock_output):
        mock_output.return_value.decode.return_value = ""
        ref, name = GitRepository.stable_ref("https://github.com/opensearch-project/OpenSearch", "sha")
        self.assertEqual(ref, "sha")
        self.assertEqual(name, "sha")
