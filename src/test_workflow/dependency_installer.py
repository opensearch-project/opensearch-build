# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil
import urllib

import validators  # type:ignore


class DependencyInstaller:
    """
    Provides a dependency installer for the test suites.
    """

    def __init__(self, root_url, build_manifest, bundle_manifest):
        self.root_url = root_url
        self.build_manifest = build_manifest
        self.bundle_manifest = bundle_manifest

    @property
    def maven_local_path(self):
        return os.path.join(os.path.expanduser("~"), ".m2", "repository")

    def install_maven_dependencies(self):
        for component in self.build_manifest.components.values():
            maven_artifacts = component.artifacts.get("maven", None)
            if maven_artifacts:
                self.download(maven_artifacts, "builds", self.maven_local_path)

    def install_build_dependencies(self, dependency_dict, dest):
        """
        Downloads the build dependencies from S3 and puts them on the given custom path
        for each dependency in the dependencies.

        :param dependencies: dictionary of dependency names with version for which the build artifacts need to be downloaded.
        Example: {'opensearch-job-scheduler':'1.1.0.0'}
        """
        os.makedirs(dest, exist_ok=True)
        for dependency, version in dependency_dict.items():
            path = f"{self.root_url}/builds/plugins/{dependency}-{version}.zip"
            local_path = os.path.join(dest, f"{dependency}-{version}.zip")
            self.__download_or_copy(path, local_path)

    def download_dist(self, dest):
        local_path = os.path.join(dest, os.path.basename(self.bundle_manifest.build.location))
        return self.__download_or_copy(self.bundle_manifest.build.location, local_path)

    def download(self, paths, category, dest):
        logging.info(f"Downloading to {dest} ...")
        for path in paths:
            url = "/".join([self.root_url, category, path])
            # paths are prefixed by category, remove
            local_path = os.path.join(dest, "/".join(path.split("/")[1:]))
            self.__download_or_copy(url, local_path)

    def __download_or_copy(self, source, dest):
        dest = os.path.realpath(dest)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if validators.url(source):
            logging.info(f"Downloading {source} into {dest} ...")
            urllib.request.urlretrieve(source, dest)
        else:
            logging.info(f"Copying {source} into {dest} ...")
            source = os.path.realpath(source)
            shutil.copyfile(os.path.realpath(source), dest)
        return dest
