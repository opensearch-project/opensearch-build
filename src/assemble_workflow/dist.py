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


class Dist(ABC):
    def __init__(self, name, path):
        self.name = name
        self.path = path

    @abstractmethod
    def __extract__(self, dest):
        pass

    def extract(self, dest):
        self.__extract__(dest)

        # OpenSearch & Dashboard tars will include only a single folder at the top level of the tar.

        for file in os.scandir(dest):
            if file.is_dir():
                self.archive_path = file.path
                return self.archive_path

        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), os.path.join(dest, "*"))

    def build(self, name, dest):
        self.__build__(name, dest)
        path = os.path.join(dest, name)
        shutil.copyfile(name, path)
        logging.info(f"Published {path}.")

    @classmethod
    def from_path(cls, name, path):
        ext = os.path.splitext(path)[1]
        if ext == ".gz":
            return DistTar(name, path)
        elif ext == ".zip":
            return DistZip(name, path)
        else:
            raise ValueError(f'Invalid min "dist" extension in input artifacts: {ext} ({path}).')


class DistZip(Dist):
    def __extract__(self, dest):
        with zipfile.ZipFile(self.path, "r") as zip:
            zip.extractall(dest)

    def __build__(self, name, dest):
        with zipfile.ZipFile(name, "w", zipfile.ZIP_DEFLATED) as zip:
            rootlen = len(self.archive_path) + 1
            for base, dirs, files in os.walk(self.archive_path):
                for file in files:
                    fn = os.path.join(base, file)
                    zip.write(fn, fn[rootlen:])


class DistTar(Dist):
    def __extract__(self, dest):
        with tarfile.open(self.path, "r") as tar:
            tar.extractall(dest)

    def __build__(self, name, dest):
        with tarfile.open(name, "w:gz") as tar:
            tar.add(self.archive_path, arcname=os.path.basename(self.archive_path))
