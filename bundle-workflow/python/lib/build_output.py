# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
from dataclasses import dataclass

@dataclass
class BuildOutput:
    dest: str = None
    arch: str = None

    def __post_init__(self):
        self.dest = os.path.join(os.getcwd(), 'artifacts')
        self.arch = BuildOutput.__get_arch()
        self.__ensure_dest__()

    def __ensure_dest__(self):
        if os.path.exists(self.dest):
            print(f'Directory exists: {self.dest}, aborting.')
            exit(1)
        os.makedirs(self.dest)

    @staticmethod
    def __get_arch():
        arch = subprocess.check_output(['uname', '-m']).decode().strip()
        if arch == 'x86_64':
            return 'x64'
        elif arch == 'aarch64' or arch == 'arm64':
            return  'arm64'
        else:
            raise ValueError(f'Unsupported architecture: {arch}')
