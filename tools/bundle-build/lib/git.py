import os
import tempfile
import subprocess

class GitRepository:
    def __init__(self, url, ref):
        self._url = url
        self._dir = tempfile.TemporaryDirectory()
        self.execute(f'git init')
        self.execute(f'git remote add origin {url}')
        self.execute(f'git fetch --depth 1 origin {ref}')
        self.execute(f'git checkout FETCH_HEAD')
        self._sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd = self.dir()).decode().strip()
        print(f'Checked out {url}@{ref} into {self._dir.name} at {self._sha}')

    def dir(self):
        return self._dir.name

    def execute(self, command):
        current = os.getcwd()
        print(f'Executing "{command}" in {self.dir()}')
        subprocess.check_call(command, cwd = self.dir(), shell = True)

    def sha(self):
        return self._sha
        