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

from system.zip_file import ZipFile


class Dist(ABC):
    def __init__(self, name: str, path: str) -> None:
        self.name = name
        self.path = path

    @abstractmethod
    def __extract__(self, dest: str) -> None:
        pass

    @abstractmethod
    def __build__(self, name: str, dest: str) -> None:
        pass

    def extract(self, dest: str) -> str:
        self.__extract__(dest)

        # OpenSearch & Dashboard tars will include only a single folder at the top level of the tar.

        for file in os.scandir(dest):
            if file.is_dir():
                self.archive_path = file.path
                return self.archive_path

        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(dest, "*"))

    def build(self, name: str, dest: str) -> None:
        self.__build__(name, dest)
        path = os.path.join(dest, name)
        shutil.copyfile(name, path)
        logging.info(f"Published {path}.")

    @classmethod
    def from_path(cls, name: str, path: str) -> 'Dist':
        ext = os.path.splitext(path)[1]
        if ext == ".gz":
            return DistTar(name, path)
        elif ext == ".zip":
            return DistZip(name, path)
        else:
            raise ValueError(f'Invalid min "dist" extension in input artifacts: {ext} ({path}).')


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


class DistTar(Dist):
    def __extract__(self, dest: str) -> None:
        with tarfile.open(self.path, "r:gz") as tar:
            tar.extractall(dest)

    def __build__(self, name: str, dest: str) -> None:
        with tarfile.open(name, "w:gz") as tar:
            tar.add(self.archive_path, arcname=os.path.basename(self.archive_path))
