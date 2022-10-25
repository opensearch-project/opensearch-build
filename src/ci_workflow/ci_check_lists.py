# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC
from typing import Any

from ci_workflow.ci_check_list_dist import CiCheckListDist
from ci_workflow.ci_check_list_source import CiCheckListSource
from ci_workflow.ci_check_list_source_ref import CiCheckListSourceRef
from ci_workflow.ci_target import CiTarget
from manifests.input_manifest import InputComponentFromDist, InputComponentFromSource


class CiCheckLists(ABC):
    @classmethod
    def from_component(self, component: Any, target: CiTarget) -> Any:
        if type(component) is InputComponentFromDist:
            return CiCheckListDist(component, target)
        elif type(component) is InputComponentFromSource:
            if len(component.checks) > 0:
                return CiCheckListSource(component, target)
            else:
                return CiCheckListSourceRef(component, target)
        else:
            raise ValueError(f"Invalid component type: {type(component)}")
