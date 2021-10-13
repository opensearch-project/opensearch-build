# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import logging
import os
import re
from abc import abstractmethod

from manifests.input_manifest import InputManifest
from manifests.manifests import Manifests


class InputManifests(Manifests):
    def __init__(self, name):
        self.name = name
        self.prefix = name.lower().replace(" ", "-")
        super().__init__(InputManifest, InputManifests.files(self.prefix))

    @classmethod
    def manifests_path(self):
        return os.path.realpath(
            os.path.join(os.path.dirname(__file__), "../../manifests")
        )

    @classmethod
    def files(self, name):
        results = []
        for filename in glob.glob(
            os.path.join(self.manifests_path(), f"**/{name}-*.yml")
        ):
            # avoids the -maven manifest
            match = re.search(rf"^{name}-([0-9.]*).yml$", os.path.basename(filename))
            if match:
                results.append(filename)
        return results

    @abstractmethod
    def update(self, keep=False):
        pass

    def write_manifest(self, version, components=[]):
        logging.info(f"Creating new version: {version}")
        data = {
            "schema-version": "1.0",
            "build": {"name": self.name, "version": version},
            "components": [],
        }
        for component in components:
            logging.info(f" Adding {component.name}")
            data["components"].append(component.to_dict())

        manifest = InputManifest(data)
        manifest_dir = os.path.join(self.manifests_path(), version)
        os.makedirs(manifest_dir, exist_ok=True)
        manifest_path = os.path.join(manifest_dir, f"{self.prefix}-{version}.yml")
        manifest.to_file(manifest_path)
        logging.info(f"Wrote {manifest_path}")
