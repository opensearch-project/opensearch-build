# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from subprocess import CalledProcessError

from git.git_repository import GitRepository
from release_notes_workflow.releasenotes_check import ReleaseNotesCheck, ReleaseNotesOpenSearch, ReleaseNotesOpenSearchPlugins
from release_notes_workflow.releasenotes_gitlog import GitLog


class TestReleaseNotesCheck(unittest.TestCase):

    def test_ReleaseNotesCheck(self) -> None:
        check_for_release_notes = ReleaseNotesCheck("OpenSearch", "2.2.2", "/tmp/")
        assert check_for_release_notes.check() == "NULL"
        OpenSearchFile = ReleaseNotesOpenSearch("2.2.2")
        assert OpenSearchFile.filename == '.release-notes-2.2.2.md'
        OpenSearchPluginFile = ReleaseNotesOpenSearchPlugins("2.2.2")
        assert OpenSearchPluginFile.filename == '.release-notes-2.2.2.0.md'

    def test_gitlog_getcommitID(self) -> None:
        repo = GitRepository(
            url="https://github.com/opensearch-project/.github",
            ref="8ac515431bf24caf92fea9d9b0af3b8f10b88453",
        )
        try:
            gitHistory = GitLog(repo.dir, '2022-07-26')
            gitHistory.commitID
            gitHistory.commitDate
        except CalledProcessError as e:
            assert e.returncode != 0
