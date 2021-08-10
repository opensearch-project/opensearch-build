# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import subprocess
import tempfile
from dataclasses import dataclass

'''
This class checks out a Git repository at a particular ref into a temporary directory.
Clients can obtain the actual commit ID by querying the "sha" attribute, and the temp directory name with "dir.name".
'''
@dataclass
class GitRepository:
    url: str
    ref: str
    sha: str = None
    dir: tempfile.TemporaryDirectory = None

    def __post_init__(self):
        self.dir = tempfile.TemporaryDirectory()
        self.execute(f'git init')
        self.execute(f'git remote add origin {self.url}')
        self.execute(f'git fetch --depth 1 origin {self.ref}')
        self.execute(f'git checkout FETCH_HEAD')
        self.sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd = self.dir.name).decode().strip()
        print(f'Checked out {self.url}@{self.ref} into {self.dir.name} at {self.sha}')

    def execute(self, command):
        print(f'Executing "{command}" in {self.dir.name}')
        subprocess.check_call(command, cwd = self.dir.name, shell = True)
