# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import yaml
import subprocess
from lib.component import Component
from dataclasses import dataclass
from typing import List

@dataclass
class Schema:
    data: str
    version: str = None
    
    def __post_init__(self):
        self.version = self.data['schema-version']
        if self.version != 1:
            raise ValueError(f'Unsupported schema version: {self.version}')

@dataclass
class Build:
    data: str
    name: str = None
    version: str = None
    dict: dict = None

    def __post_init__(self):
        self.name = self.data['name']
        self.version = self.data['version']
        self.__set_dict()

    def __set_dict(self):
        self.dict = {
            'name': self.name,
            'version': self.version
        }

@dataclass
class BuildManifest:
    data: str
    schema: Schema = None
    build: Build = None
    components: List[Component] = None

    @staticmethod
    def from_file(path):
        with open(path, 'r') as file:
            return BuildManifest(yaml.safe_load(file))

    def __post_init__(self):
        self.schema = Schema(self.data)
        self.build = Build(self.data['build'])
        self.components = list(map(lambda entry: Component(
            entry['name'], 
            entry['repository'], 
            entry['ref']
        ), self.data['components']))

    def save_to(self, path):
        with open(path, 'w') as file:
            data = {
                'schema-version' : 1.0,
                'build': self.build.dict,
                'components': list(map(lambda component: component.dict, self.components))
            }
            yaml.dump(data, file)
        print(f'Written manifest to {path}.')