# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import concurrent.futures
import logging
import os
import shutil
import urllib

import validators  # type:ignore


class DependencyInstaller(abc.ABC):
    """
    Provides a dependency installer for the test suites.
    """

    def __init__(self, root_url, build_manifest, bundle_manifest):
        self.root_url = root_url
        self.build_manifest = build_manifest
        self.bundle_manifest = bundle_manifest

    def download_dist(self, dest):
        local_path = os.path.realpath(os.path.join(dest, os.path.basename(self.bundle_manifest.build.location)))
        return self.download_or_copy(self.bundle_manifest.build.location, local_path)

    def __source_dest(self, path, category, dest):
        source = "/".join([self.root_url, category, self.build_manifest.build.filename, path])
        dest = os.path.realpath(os.path.join(dest, "/".join(path.split("/")[1:])))
        return (source, dest)

    def download(self, paths, category, dest):
        logging.info(f"Downloading to {dest} ...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for result in executor.map(
                lambda args: self.download_or_copy(*args),
                    map(lambda path: self.__source_dest(path, category, dest),
                        paths)
            ):
                logging.debug(f"Written {result}")

    def download_or_copy(self, source, dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if validators.url(source):
            logging.info(f"Downloading {source} into {dest} ...")
            urllib.request.urlretrieve(source, dest)
        else:
            logging.info(f"Copying {source} into {dest} ...")
            source = os.path.realpath(source)
            shutil.copyfile(os.path.realpath(source), dest)
        return dest
