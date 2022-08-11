# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from subprocess import CalledProcessError

from git.git_repository import GitRepository
from release_notes_workflow.release_notes_component import ComponentReleaseNotes
from release_notes_workflow.release_notes_gitlog import GitLog


class TestReleaseNotesCheck(unittest.TestCase):

    def test_ReleaseNotesCheck(self) -> None:
        manifest_check_opensearch = ComponentReleaseNotes("OpenSearch", "2.2.0", "/tmp/")
        assert manifest_check_opensearch.from_component() == ".release-notes-2.2.0.md"
        manifest_check_opensearchplugin = ComponentReleaseNotes("common-utils", "2.2.0", "/tmp/")
        assert manifest_check_opensearchplugin.from_component() == ".release-notes-2.2.0.0.md"

    def test_ReleaseNotesCheckFunctions(self) -> None:
        repo = GitRepository(
            url="https://github.com/opensearch-project/common-utils",
            ref="c3408f34961eb7e8ebc0510306f62238a457dbbc",
        )
        manifest_check = ComponentReleaseNotes("common-utils", "2.2.0", repo.dir)
        assert manifest_check.exists() is True

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
