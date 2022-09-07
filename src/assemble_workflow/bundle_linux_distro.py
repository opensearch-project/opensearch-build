# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil
import subprocess

from manifests.build_manifest import BuildManifest


class BundleLinuxDistro:

    def __init__(self, filename: str, package_path: str, min_path: str) -> None:
        self.filename = filename
        self.package_path = package_path
        self.min_path = min_path

    def extract(self, min_source_path: str, min_dest_path: str, min_config_path: str) -> None:
        # Move core folder destination so plugin install can proceed
        logging.info(f"Move {min_source_path} to {min_dest_path} for plugin installation")
        shutil.move(min_source_path, min_dest_path)

        # Multiple modifications and env vars setups before install plugins
        # As bin/opensearch-env is different between archive and package
        # https://github.com/opensearch-project/OpenSearch/issues/2092
        os.environ[f"{self.filename.upper()}_PATH_CONF"] = min_config_path
