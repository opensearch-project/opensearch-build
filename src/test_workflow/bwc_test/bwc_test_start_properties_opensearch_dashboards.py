# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from test_workflow.bwc_test.bwc_test_start_properties import BwcTestStartProperties


class BwcTestStartPropertiesOpenSearchDashboards(BwcTestStartProperties):
    def __init__(self, path):
        super().__init__(path, "builds/opensearch-dashboards/manifest.yml", "dist/opensearch-dashboards/manifest.yml")
