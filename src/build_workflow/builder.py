# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod


class Builder(ABC):
    def __init__(self, component, target):
        self.output_path = "builds"
        self.component = component
        self.target = target

    @abstractmethod
    def checkout(self):
        pass

    @abstractmethod
    def build(self, build_recorder):
        pass

    @abstractmethod
    def export_artifacts(self, build_recorder):
        pass
