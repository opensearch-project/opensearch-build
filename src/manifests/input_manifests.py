# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import os
import re

from manifests.input_manifest import InputManifest
from manifests.manifests import Manifests


class InputManifests(Manifests):
    def __init__(self) -> None:
        files = glob.glob(os.path.join(self.manifests_path, "**/opensearch-*.yml"))
        # there's an opensearch-1.0.0-maven.yml that we want to skip
        files = [f for f in files if re.search(r"[\\/]opensearch-([0-9.]*)\.yml$", f)]
        super().__init__(InputManifest, files)
