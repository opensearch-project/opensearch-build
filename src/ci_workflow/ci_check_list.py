# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod


class CiCheckList(ABC):
    def __init__(self, component, target):
        self.component = component
        self.target = target

    @abstractmethod
    def checkout(self, work_dir):
        pass

    @abstractmethod
    def check(self):
        pass
