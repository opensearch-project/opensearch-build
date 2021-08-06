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

    def save_to(self, path):
        with open(path, 'w') as file:
            data = {
                'schema-version' : 1.0,
                'build': self.build().dict(),
                'components': list(map(lambda component: component.dict(), self.components()))
            }
            yaml.dump(data, file)

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

    def version(self):
        return self._version

    def name(self):
        return self._name

    def dict(self):
        return {
            'name': self.name(),
            'version': self.version()
        }
