# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import yaml

'''
An InputManifest is an immutable view of the input manifest for the build system.
The manifest contains information about the product that is being built (in the `build` section),
and the components that make up the product in the `components` section.

The format for schema version 1.0 is:
schema-version: 1.0
build:
  name: string
  version: string
components:
  - name: string
    repository: URL of git repository
    ref: git ref to build (sha, branch, or tag)
  - ...
'''
class InputManifest:
    @staticmethod
    def from_file(file):
      return InputManifest(yaml.safe_load(file))

    def __init__(self, data):
        self.version = str(data['schema-version'])
        if self.version != '1.0':
            raise ValueError(f'Unsupported schema version: {self.version}')
        self.build = self.Build(data['build'])
        self.components = list(map(lambda entry: self.Component(entry),
                                   data['components']))

    class Build:
        def __init__(self, data):
            self.name = data['name']
            self.version = data['version']

    class Component:
        def __init__(self, data):
            self.name = data['name']
            self.repository = data['repository']
            self.ref = data['ref']
