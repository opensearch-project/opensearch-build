# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from manifests_workflow.component_opensearch_dashboards_min import ComponentOpenSearchDashboardsMin
from manifests_workflow.input_manifests import InputManifests


class InputManifestsOpenSearchDashboards(InputManifests):
    def __init__(self):
        super().__init__("OpenSearch Dashboards")

    @classmethod
    def files(self):
        return InputManifests.files("opensearch-dashboards")

    def update(self, keep=False):
        super().update(min_klass=ComponentOpenSearchDashboardsMin, component_klass=None, keep=keep)
