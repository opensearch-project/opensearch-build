# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from assemble_workflow.bundle_location import BundleLocation


class BundleFileLocation(BundleLocation):
    def __init__(self, path: str, filename: str) -> None:
        super().__init__(path, filename)

    def join(self, *args: str) -> str:
        return os.path.join(self.path, *args)
