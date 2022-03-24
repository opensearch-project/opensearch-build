# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import errno
import logging
import os
import shutil
import tarfile
import zipfile
from abc import ABC, abstractmethod

from assemble_workflow.bundle_rpm import BundleRpm
from manifests.build_manifest import BuildManifest
from system.zip_file import ZipFile


class Dist(ABC):
    def __init__(self, name: str, path: str, min_path: str, build_cls: BuildManifest.Build) -> None:
        self.build_cls = build_cls
        self.name = name
        self.filename = name.lower()
        self.path = path
        self.min_path = min_path

    @abstractmethod
    def __extract__(self, dest: str) -> None:
        pass

    @abstractmethod
    def __build__(self, name: str, dest: str) -> None:
        pass

    def find_min_archive_path(self, dest: str) -> str:
        '''
        Return the single folder that contains the main files of {name}.
        This folder is normally in the format of {filename}-{exact or bc version}.

        Ex: opensearch-1.3.0 or opensearch-dashboards-1.3.0

        Adding a check of whether {filename} is in folder name is to ensure
        that only folders in above format are returned.

        In tar there is only 1 top level folders after extraction.
        But in rpm there are multiple folders such as var / usr / opensearch-1.3.0 ......

        This is to ensure corrent folder is found, instead of simply choosing the 1st in the list.
        '''

        for file in os.scandir(dest):
            if self.filename in file.name and file.is_dir():
                self.archive_path = file.path
                return self.archive_path

        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(dest, "*"))

    def rename_archive_path(self, path: str) -> str:
        '''
        Rename the single folder at the top level of the tar that contains the min distribution to match current version.
        For example, when OpenSearch 1.1.1 is built using the 1.1.0 artifact, we rename opensearch-1.1.0 to opensearch-1.1.1.
        '''
        current_name = os.path.basename(path)
        target_name = self.min_path
        if current_name != target_name:
            logging.info(f"Renaming {path} to {target_name}.")
            target_path = os.path.join(os.path.dirname(path), target_name)
            os.rename(path, target_path)
            return target_path
        else:
            return path

    def extract(self, dest: str) -> str:
        self.__extract__(dest)
        self.archive_path = self.rename_archive_path(
            self.find_min_archive_path(dest)
        )
        return self.archive_path

    def build(self, name: str, dest: str) -> None:
        self.__build__(name, dest)
        path = os.path.join(dest, name)
        shutil.copyfile(name, path)
        logging.info(f"Published {path}.")


class DistTar(Dist):
    def __extract__(self, dest: str) -> None:
        with tarfile.open(self.path, "r:gz") as tar:
            tar.extractall(dest)

    def __build__(self, name: str, dest: str) -> None:
        with tarfile.open(name, "w:gz") as tar:
            tar.add(self.archive_path, arcname=os.path.basename(self.archive_path))


class DistZip(Dist):
    def __extract__(self, dest: str) -> None:
        with ZipFile(self.path, "r") as zip:
            zip.extractall(dest)

    def __build__(self, name: str, dest: str) -> None:
        with ZipFile(name, "w", zipfile.ZIP_DEFLATED) as zip:
            rootlen = len(self.archive_path) + 1
            for base, _, files in os.walk(self.archive_path):
                for file in files:
                    fn = os.path.join(base, file)
                    zip.write(fn, fn[rootlen:])


class DistRpm(Dist):

    def __extract__(self, dest: str) -> None:
        BundleRpm(self.filename, self.path, self.min_path).extract(dest)

    def __build__(self, name: str, dest: str) -> None:
        BundleRpm(self.filename, self.path, self.min_path).build(name, dest, self.archive_path, self.build_cls)
