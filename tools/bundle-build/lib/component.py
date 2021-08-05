import os
import tempfile
import subprocess
from lib.git import GitRepository

class Component:
    def __init__(self, data):
        self._name = data['name']
        self._repository = data['repository']
        self._ref = data['ref']

    def name(self):
        return self._name

    def repository(self):
        return self._repository

    def git_repository(self):
        return self._git_repository

    def ref(self):
        return self._ref

    def checkout(self):
        self._git_repository = GitRepository(self.repository(), self.ref())

    # script overridden in this repo
    def custom_component_script_path(self):
        dirname = os.path.dirname(os.path.abspath(__file__))      
        return os.path.realpath(os.path.join(dirname, '../../../scripts/bundle-build/components', self.name(), 'build.sh'))

    # script inside the component repo
    def component_script_path(self):
        dirname = self.git_repository().dir()     
        return os.path.realpath(os.path.join(dirname, 'scripts/build.sh'))

    # default gradle script
    def default_script_path(self):
        dirname = os.path.dirname(os.path.abspath(__file__))      
        return os.path.realpath(os.path.join(dirname, '../../../scripts/bundle-build/standard-gradle-build/build.sh'))

    def build_script(self):
        paths = [self.component_script_path(), self.custom_component_script_path(), self.default_script_path()]
        return next(filter(lambda path: os.path.exists(path), paths), None)

    def build(self, version, arch):
        build_script = f'{self.build_script()} {version} {arch}' 
        print(f'Running {build_script} ...')
        self.git_repository().execute(build_script)

