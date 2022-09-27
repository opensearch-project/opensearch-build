# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC

from build_workflow.build_target import BuildTarget
from build_workflow.builder import Builder
from build_workflow.builder_from_dist import BuilderFromDist
from build_workflow.builder_from_source import BuilderFromSource
from manifests.input_manifest import InputComponent, InputComponentFromDist, InputComponentFromSource


class Builders(ABC):
    @classmethod
    def builder_from(self, component: InputComponent, target: BuildTarget) -> Builder:
        if type(component) is InputComponentFromDist:
            return BuilderFromDist(component, target)
        elif type(component) is InputComponentFromSource:
            return BuilderFromSource(component, target)
        else:
            raise ValueError(f"Invalid component type: {type(component)}")
