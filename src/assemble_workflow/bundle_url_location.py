# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from urllib.parse import urljoin

from assemble_workflow.bundle_location import BundleLocation


class BundleUrlLocation(BundleLocation):
    def __init__(self, path: str, filename: str) -> None:
        super().__init__(path, filename)

    def join(self, *args: str) -> str:
        sub_path = "/".join(args)
        return urljoin(self.path + "/", sub_path)
