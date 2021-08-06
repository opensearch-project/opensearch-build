# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import tempfile
import subprocess
from lib.git_repository import GitRepository
from dataclasses import dataclass

@dataclass
class Component:
    name: str
    repository: str
    ref: str
    artifacts: dict = None
    git_repository: GitRepository = None
    dict: dict = None
    artifacts_path: str = None
    build_script: str = None
    component_script_path: str = None
    custom_component_script_path: str = None

    def checkout(self):
        self.git_repository = GitRepository(self.repository, self.ref)
        self.__set_custom_component_script_path()
        self.__set_component_script_path()
        self.__set_default_script_path()
        self.__set_build_script()
        self.__set_artifacts_path()

    # script overridden in this repo
    def __set_custom_component_script_path(self):
        dirname = os.path.dirname(os.path.abspath(__file__))      
        self.custom_component_script_path = os.path.realpath(os.path.join(dirname, '../../../scripts/bundle-build/components', self.name, 'build.sh'))

    # script inside the component repo
    def __set_component_script_path(self):
        dirname = self.git_repository.dir.name     
        self.component_script_path = os.path.realpath(os.path.join(dirname, 'scripts/build.sh'))

    # default gradle script
    def __set_default_script_path(self):
        dirname = os.path.dirname(os.path.abspath(__file__))      
        self.default_script_path = os.path.realpath(os.path.join(dirname, '../../../scripts/bundle-build/standard-gradle-build/build.sh'))

    def __set_build_script(self):
        paths = [self.component_script_path, self.custom_component_script_path, self.default_script_path]
        self.build_script = next(filter(lambda path: os.path.exists(path), paths), None)

    def build(self, version, arch):
        build_script = f'{self.build_script} {version} {arch}' 
        print(f'Running {build_script} ...')
        self.git_repository.execute(build_script)

    def __set_artifacts_path(self):
        dirname = self.git_repository.dir.name
        self.artifacts_path = os.path.realpath(os.path.join(dirname, 'artifacts'))

    def export(self, dest):
        if os.path.exists(self.artifacts_path):
            print(f'Publishing artifacts from {self.artifacts_path} into {dest} ...')
            self.git_repository.execute(f'cp -r "{self.artifacts_path}/"* "{dest}"')
        else:
            print(f'No artifacts found in {artifacts_path}, skipping.')
        self.__set_artifacts()
        self.__set_dict()

    def __set_artifacts(self):
        artifacts = {}
        for key in ["maven", "plugins", "bundle", "libs"]:
            file_paths = self.__get_file_paths(key)
            if file_paths:
                artifacts[key] = file_paths
        self.artifacts = artifacts

    def __get_file_paths(self, dir_name):
      sub_dir = os.path.join(self.artifacts_path, dir_name)
      file_paths = []
      if os.path.exists(sub_dir):
        for dir, dirs, files in os.walk(sub_dir):
          for file_name in files:
            path = os.path.relpath(os.path.join(dir, file_name), self.artifacts_path)
            file_paths.append(path)
      return file_paths

    def __set_dict(self):
        self.dict = {
            'name': self.name,
            'repository': self.repository,
            'ref': self.ref,
            'sha': self.git_repository.sha,
            'artifacts': self.artifacts
        }
