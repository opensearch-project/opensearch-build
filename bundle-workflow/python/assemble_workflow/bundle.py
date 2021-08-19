# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import tarfile
import tempfile
import shutil
import subprocess

'''
This class is responsible for executing the build of the full bundle and passing results to a bundle recorder.
It requires a min tarball distribution where plugins will be installed and the path to an artifacts directory where 
plugins can be found.
'''


class Bundle:

    def __init__(self, build_manifest, artifacts_dir, bundle_recorder, script_finder):
        """
        Construct a new Bundle instance.
        :param build_manifest: A BuildManifest created from the build workflow.
        :param artifacts_dir: Dir location where build artifacts can be found locally
        :param bundle_recorder: The bundle recorder that will capture and build a BundleManifest
        """
        self.min_tarball = self.get_min_bundle(build_manifest.components)
        self.plugins = self.get_plugins(build_manifest.components)
        self.artifacts_dir = artifacts_dir
        self.bundle_recorder = bundle_recorder
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.installed_plugins = []
        self.script_finder = script_finder
        tmp_path = self.add_component(self.min_tarball, "bundle")
        self.unpack(tmp_path, self.tmp_dir.name)
        # OpenSearch & Dashboard tars will include only a single folder at the top level of the tar
        self.archive_path = next(iter([file.path for file in os.scandir(self.tmp_dir.name) if file.is_dir()]))

    def install_plugins(self):
        for plugin in self.plugins:
            print(f'Installing {plugin.name}')
            self.install_plugin(plugin)
        self.installed_plugins = os.listdir(os.path.join(self.archive_path, 'plugins'))

    def install_plugin(self, plugin):
        tmp_path = self.add_component(plugin, "plugins")
        cli_path = os.path.join(self.archive_path, 'bin/opensearch-plugin')
        self.execute(f'{cli_path} install --batch file:{tmp_path}')
        post_install_script = self.script_finder.find_install_script(plugin.name)
        self.execute(f'{post_install_script} -a "{self.artifacts_dir}" -o "{self.archive_path}"')

    def add_component(self, component, component_type):
        rel_path = self.get_rel_path(component, component_type)
        tmp_path = self.copy_component(rel_path, self.tmp_dir.name)
        self.bundle_recorder.record_component(component, rel_path)
        return tmp_path

    def execute(self, command):
        print(f'Executing "{command}" in {self.archive_path}')
        subprocess.check_call(command, cwd=self.archive_path, shell=True)

    def unpack(self, tar_path, dest):
        with tarfile.open(tar_path) as tar:
            tar.extractall(dest)

    def build_tar(self, dest):
        tar_name = self.bundle_recorder.tar_name
        with tarfile.open(tar_name, "w:gz") as tar:
            tar.add(self.archive_path, arcname=os.path.basename(self.archive_path))
        shutil.copyfile(tar_name, os.path.join(dest, tar_name))

    def get_rel_path(self, component, component_type):
        return next(iter(component.artifacts.get(component_type, [])), None)

    def copy_component(self, rel_path, dest):
        local_path = os.path.join(self.artifacts_dir, rel_path)
        dest_path = os.path.join(dest, os.path.basename(local_path))
        if os.path.isfile(local_path):
            # rel path provided, in this case we copy it into dest
            shutil.copyfile(local_path, dest_path)
            return os.path.join(dest, os.path.basename(local_path))
        else:
            raise ValueError(f'No file found at path: {local_path}')

    def get_plugins(self, build_components):
        return [c for c in build_components if "plugins" in c.artifacts]

    def get_min_bundle(self, build_components):
        min_bundle = next(iter([c for c in build_components if "bundle" in c.artifacts]), None)
        if min_bundle == None:
            raise ValueError(f'Missing min "bundle" in input artifacts.')
        return min_bundle

