import os
import subprocess

class BuildOutput:
    def __init__(self):
        self._dest = os.path.join(os.getcwd(), 'artifacts')
        self._arch = BuildOutput.arch()
        self.__ensure_dest()

    def dest(self):
        return self._dest

    def arch(self):
        return self._arch

    def __ensure_dest(self):
        if os.path.exists(self.dest()):
            raise Exception(f'Directory exists: {self.dest()}')
        os.makedirs(self.dest())

    @staticmethod
    def arch():
        arch = subprocess.check_output(['uname', '-m']).decode().strip()
        if arch == 'x86_64':
            return 'x64'
        elif arch == 'aarch64' or arch == 'arm64':
            return  'arm64'
        else:
            raise ValueError(f'Unsupported architecture: {arch}')
