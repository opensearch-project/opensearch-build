# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess


class GitLog:

    def __init__(self, gitrepo: str, date: str) -> None:
        self.gitrepo = gitrepo
        self.date = date

    @property
    def commitID(self) -> str:
        gitLogCmd = f'git log --date=local --after={self.date} --pretty=format:"%h"'
        commitID = subprocess.check_output(gitLogCmd.split(), cwd=self.gitrepo).decode()
        return commitID

    @property
    def commitDate(self) -> str:
        gitLogCmd = f'git log --date=local --after={self.date} --pretty=format:"%as"'
        commitDate = subprocess.check_output(gitLogCmd.split(), cwd=self.gitrepo).decode()
        return commitDate
