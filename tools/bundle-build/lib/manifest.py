import yaml
import subprocess
from lib.component import Component

class BuildManifest:
    @staticmethod
    def from_file(path):
        with open(path, 'r') as file:
            return BuildManifest(yaml.safe_load(file))

    def __init__(self, data):
        self._schema = Schema(data)
        self._build = Build(data['build'])
        self._components = list(map(lambda entry: Component(entry), data['components']))

    def build(self):
        return self._build

    def components(self):
        return self._components

class Schema:
    def __init__(self, data):
        self._version = data['schema-version']
        if self._version != 1:
            raise ValueError(f'Unsupported schema version: {self._version}')

    def version(self):
        return self._version

class Build:
    def __init__(self, data):
        self._name = data['name']
        self._version = data['version']
        self._arch = Build.arch()

    def version(self):
        return self._version

    def name(self):
        return self._name

    def arch(self):
        return self._arch

    @staticmethod
    def arch():
        arch = subprocess.check_output(['uname', '-m']).decode().strip()
        if arch == 'x86_64':
            return 'x64'
        elif arch == 'aarch64' or arch == 'arm64':
            return  'arm64'
        else:
            raise ValueError(f'Unsupported architecture: ' + arch)
