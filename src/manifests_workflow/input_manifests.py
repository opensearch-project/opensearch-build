# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import os
import re
from abc import abstractmethod

from manifests.input_manifest import InputManifest
from manifests.manifests import Manifests


class InputManifests(Manifests):
    def __init__(self):
        super().__init__(InputManifest, self.files())

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
