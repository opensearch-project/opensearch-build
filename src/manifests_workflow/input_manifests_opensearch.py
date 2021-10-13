# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from manifests_workflow.component_opensearch import ComponentOpenSearch
from manifests_workflow.component_opensearch_min import ComponentOpenSearchMin
from manifests_workflow.input_manifests import InputManifests


class InputManifestsOpenSearch(InputManifests):
    def __init__(self):
        super().__init__("OpenSearch")

    @classmethod
    def files(self):
        return InputManifests.files("opensearch")

    def update(self, keep=False):
        super().update(
            min_klass=ComponentOpenSearchMin,
            component_klass=ComponentOpenSearch,
            keep=keep,
        )
