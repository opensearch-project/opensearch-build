import subprocess
import tempfile

class GitRepository:
    def __init__(self, url, ref):
        self._url = url
        self._dir = tempfile.TemporaryDirectory()
        self.execute(f'git init')
        self.execute(f'git remote add origin {url}')
        self.execute(f'git fetch --depth 1 origin {ref}')
        self.execute(f'git checkout {ref}')
        print(f'Checked out {url}@{ref} into {self._dir.name}')

    def dir(self):
        return self._dir.name

    def execute(self, command):
        print(f'Executing "{command}" in {self._dir.name}')
        subprocess.check_call(command, shell=True, cwd=self._dir.name)
