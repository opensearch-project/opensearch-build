# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from assemble_workflow.bundle_file_location import BundleFileLocation
from assemble_workflow.bundle_location import BundleLocation
from assemble_workflow.bundle_url_location import BundleUrlLocation


class BundleLocations:

    @classmethod
    def from_path(cls, url_path: str, file_path: str, filename: str) -> BundleLocation:
        return BundleUrlLocation(url_path, filename) if url_path else BundleFileLocation(file_path, filename)
