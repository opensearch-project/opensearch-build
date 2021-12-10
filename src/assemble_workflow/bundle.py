# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import errno
import logging
import os
import shutil
import subprocess
from abc import ABC, abstractmethod
from typing import Any, List

from assemble_workflow.bundle_recorder import BundleRecorder
from assemble_workflow.dist import Dist
from manifests.build_manifest import BuildComponent, BuildComponents, BuildManifest
from paths.script_finder import ScriptFinder
from system.temporary_directory import TemporaryDirectory

"""
This class is responsible for executing the build of the full bundle and passing results to a bundle recorder.
It requires a min tarball distribution where plugins will be installed and the path to an artifacts directory where
plugins can be found.
"""


class Bundle(ABC):
    def __enter__(self) -> 'Bundle':
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        self.tmp_dir.__exit__(exc_type, exc_value, exc_traceback)

    def __init__(self, build_manifest: BuildManifest, artifacts_dir: str, bundle_recorder: BundleRecorder, keep: bool = False) -> None:
        """
        Construct a new Bundle instance.
        :param build_manifest: A BuildManifest created from the build workflow.
        :param artifacts_dir: Dir location where build artifacts can be found locally
        :param bundle_recorder: The bundle recorder that will capture and build a BundleManifest
        """
        self.build = build_manifest.build
        self.plugins = self.__get_plugins(build_manifest.components)
        self.artifacts_dir = artifacts_dir
        self.bundle_recorder = bundle_recorder
        self.tmp_dir = TemporaryDirectory(keep=keep)
        self.min_dist = self.__get_min_dist(build_manifest.components)
        self.installed_plugins: List[str] = []

    def install_min(self) -> None:
        install_script = ScriptFinder.find_install_script(self.min_dist.name)
        install_command = " ".join(
            [
                "bash",
                install_script,
                "-v",
                self.build.version,
                "-p",
                self.build.platform,
                "-a",
                self.build.architecture,
                "-f",
                self.artifacts_dir,
                "-o",
                self.min_dist.archive_path,
            ]
        )
        self._execute(install_command)

    def install_plugins(self) -> None:
        for plugin in self.plugins:
            logging.info(f"Installing {plugin.name}")
            self.install_plugin(plugin)
        plugins_path = os.path.join(self.min_dist.archive_path, "plugins")
        if os.path.isdir(plugins_path):
            self.installed_plugins = os.listdir(plugins_path)

    @abstractmethod
    def install_plugin(self, plugin: BuildComponent) -> None:
        install_script = ScriptFinder.find_install_script(plugin.name)
        install_command = " ".join(
            [
                "bash",
                install_script,
                "-v",
                self.build.version,
                "-p",
                self.build.platform,
                "-a",
                self.build.architecture,
                "-f",
                self.artifacts_dir,
                "-o",
                self.min_dist.archive_path,
            ]
        )
        self._execute(install_command)

    def package(self, dest: str) -> None:
        self.min_dist.build(self.bundle_recorder.package_name, dest)

    def _execute(self, command: str) -> None:
        logging.info(f'Executing "{command}" in {self.min_dist.archive_path}')
        subprocess.check_call(command, cwd=self.min_dist.archive_path, shell=True)

    def _copy_component(self, component: BuildComponent, component_type: str) -> str:
        rel_path = self.__get_rel_path(component, component_type)
        tmp_path = self.__copy_component_files(rel_path, self.tmp_dir.name)
        self.bundle_recorder.record_component(component, rel_path)
        return tmp_path

    def __get_rel_path(self, component: BuildComponent, component_type: str) -> str:
        return next(iter(component.artifacts.get(component_type, [])), None)

    def __copy_component_files(self, rel_path: str, dest: str) -> str:
        local_path = os.path.join(self.artifacts_dir, rel_path)
        dest_path = os.path.join(dest, os.path.basename(local_path))
        if os.path.isfile(local_path):
            # rel path provided, in this case we copy it into dest
            shutil.copyfile(local_path, dest_path)
            return os.path.join(dest, os.path.basename(local_path))
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), local_path)

    def __get_plugins(self, build_components: BuildComponents) -> List[BuildComponent]:
        return [c for c in build_components.values() if "plugins" in c.artifacts]

    def __get_min_dist(self, build_components: BuildComponents) -> Dist:
        min_bundle = next(iter([c for c in build_components.values() if "dist" in c.artifacts]), None)
        if min_bundle is None:
            raise ValueError('Missing min "dist" in input artifacts.')
        min_dist_path = self._copy_component(min_bundle, "dist")
        logging.info(f"Copied min bundle to {min_dist_path}.")
        min_path = f"{self.build.filename}-{self.build.version}".replace("-SNAPSHOT", "")
        min_dist = Dist.from_path(min_bundle.name, min_dist_path, min_path)
        logging.info(f"Extracting dist into {self.tmp_dir.name}.")
        min_dist.extract(self.tmp_dir.name)
        logging.info(f"Extracted dist into {self.tmp_dir.name}.")
        return min_dist
