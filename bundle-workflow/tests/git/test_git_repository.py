# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
import tempfile
import unittest
from unittest.mock import MagicMock

from src.git.git_repository import GitRepository


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
        self.assertIs(type(self.repo.temp_dir), tempfile.TemporaryDirectory)
        self.assertEqual(self.repo.dir, self.repo.temp_dir.name)
        self.assertTrue(
            os.path.isfile(os.path.join(self.repo.dir, "CODE_OF_CONDUCT.md"))
        )
        # was added in the next commit
        self.assertFalse(os.path.exists(os.path.join(self.repo.dir, "CONTRIBUTING.md")))

    def test_execute(self):
        self.repo.execute("echo $PWD > created.txt")
        self.assertTrue(os.path.isfile(os.path.join(self.repo.dir, "created.txt")))

    def test_execute_in_dir(self):
        self.repo.execute("echo $PWD > created.txt", subdirname="ISSUE_TEMPLATE")
        self.assertFalse(os.path.isfile(os.path.join(self.repo.dir, "created.txt")))
        self.assertTrue(
            os.path.isfile(os.path.join(self.repo.dir, "ISSUE_TEMPLATE/created.txt"))
        )

    def test_execute_silent(self):
        _check_call = subprocess.check_call
        subprocess.check_call = MagicMock(return_value=None)
        try:
            self.repo.execute("echo .", silent=True)
            subprocess.check_call.assert_called_with(
                "echo .",
                cwd=self.repo.dir,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        finally:
            subprocess.check_call = _check_call

    def test_execute_not_silent(self):
        _check_call = subprocess.check_call
        subprocess.check_call = MagicMock(return_value=None)
        try:
            self.repo.execute("echo .", silent=False)
            subprocess.check_call.assert_called_with(
                "echo .", cwd=self.repo.dir, shell=True
            )
        finally:
            subprocess.check_call = _check_call


class TestGitRepositoryDir(unittest.TestCase):
    def test_checkout_into_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, ".github")
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
            self.assertTrue(
                os.path.isfile(os.path.join(repo.dir, "CODE_OF_CONDUCT.md"))
            )
