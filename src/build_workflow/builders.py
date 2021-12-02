# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC

from build_workflow.builder_from_dist import BuilderFromDist
from build_workflow.builder_from_source import BuilderFromSource
from manifests.input_manifest import InputManifest


class Builders(ABC):
    @classmethod
    def builder_from(self, component, target):
        if type(component) is InputManifest.ComponentFromDist:
            return BuilderFromDist(component, target)
        elif type(component) is InputManifest.ComponentFromSource:
            return BuilderFromSource(component, target)
        else:
            raise ValueError(f"Invalid component type: {type(component)}")
