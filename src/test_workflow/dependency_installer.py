# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import concurrent.futures
import logging
import os
import pathlib
import shutil
import urllib
from typing import List, Tuple

import validators  # type:ignore

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest


class DependencyInstaller(abc.ABC):
    root_url: str
    build_manifest: BuildManifest
    bundle_manifest: BundleManifest

    """
    Provides a dependency installer for the test suites.
    """

    def __init__(self, root_url: str, build_manifest: BuildManifest, bundle_manifest: BundleManifest) -> None:
        self.root_url = root_url
        self.build_manifest = build_manifest
        self.bundle_manifest = bundle_manifest

    def download_dist(self, dest: str) -> str:
        local_path = os.path.realpath(os.path.join(dest, os.path.basename(self.bundle_manifest.build.location)))
        return self.download_or_copy(self.bundle_manifest.build.location, local_path)

    def __source_dest(self, path: str, category: str, dest: str) -> Tuple[str, str]:
        source = os.path.join(self.root_url, category, self.build_manifest.build.filename, path)
        dest = os.path.realpath(os.path.join(dest, os.path.join(*pathlib.Path(path).parts[1:])))
        return (source, dest)

    def download(self, paths: List[str], category: str, dest: str) -> None:
        logging.info(f"Downloading to {dest} ...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            for result in executor.map(
                lambda args: self.download_or_copy(*args),
                    map(lambda path: self.__source_dest(path, category, dest),
                        paths)
            ):
                logging.debug(f"Written {result}")

    def download_or_copy(self, source: str, dest: str) -> str:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        # Required to make sure validators.url is checking an actual url with '/'
        # else '\\' will fail the check even if it is a valid url format
        # Ex: https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.4.0/6452/windows/x64/zip\builds\opensearch\maven\org\opensearch\client\client-benchmarks\maven-metadata.xml
        source_url = source.replace('\\', '/')
        if validators.url(source_url):
            logging.info(f"Downloading {source_url} into {dest} ...")
            urllib.request.urlretrieve(source_url, dest)
        else:
            logging.info(f"Copying {source} into {dest} ...")
            source = os.path.realpath(source)
            shutil.copyfile(os.path.realpath(source), dest)
        return dest
