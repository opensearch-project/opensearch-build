# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from urllib.parse import urljoin

from assemble_workflow.bundle_location import BundleLocation


class BundleUrlLocation(BundleLocation):
    def __init__(self, path: str, filename: str, distribution: str) -> None:
        super().__init__(path, filename, distribution)

    def join(self, *args: str) -> str:
        sub_path = "/".join(args)

        # Make sure \ is replaced with / for valid url
        # We will only make change here as the location can be either local or url
        # Thus keep \ if it is a local path
        return urljoin(self.path + "/", sub_path.replace("\\", "/"))
