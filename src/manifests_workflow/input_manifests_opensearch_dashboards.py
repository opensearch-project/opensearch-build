# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
from typing import List, Type, Union

from manifests_workflow.component_opensearch import ComponentOpenSearch
from manifests_workflow.component_opensearch_dashboards_min import ComponentOpenSearchDashboardsMin
from manifests_workflow.component_opensearch_min import ComponentOpenSearchMin
from manifests_workflow.input_manifests import InputManifests


class InputManifestsOpenSearchDashboards(InputManifests):
    def __init__(self) -> None:
        super().__init__("OpenSearch Dashboards")

    @classmethod
    def files(self, name: str = "opensearch-dashboards") -> List:
        return InputManifests.files(name)

    def update(self, min_klass: Union[Type[ComponentOpenSearchMin], Type[ComponentOpenSearchDashboardsMin]] =
               ComponentOpenSearchDashboardsMin, component_klass: Type[ComponentOpenSearch] = None,
               keep: bool = False) -> None:
        super().update(min_klass=ComponentOpenSearchDashboardsMin, component_klass=None, keep=keep)
