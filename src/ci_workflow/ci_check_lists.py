# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC

from ci_workflow.ci_check_list_dist import CiCheckListDist
from ci_workflow.ci_check_list_source import CiCheckListSource
from manifests.input_manifest import InputComponentFromDist, InputComponentFromSource


class CiCheckLists(ABC):
    @classmethod
    def from_component(self, component, target):
        if type(component) is InputComponentFromDist:
            return CiCheckListDist(component, target)
        elif type(component) is InputComponentFromSource:
            return CiCheckListSource(component, target)
        else:
            raise ValueError(f"Invalid component type: {type(component)}")
