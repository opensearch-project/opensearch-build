#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from git.git_repository import GitRepository


class TestComponent:
    repository: str
    commit_id: str

    def __init__(self, respository, commit_id):
        self.repository = respository
        self.commit_id = commit_id

    def checkout(self, directory):
        return GitRepository(self.repository, self.commit_id, directory)


TestComponent.__test__ = False  # type:ignore
