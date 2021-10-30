# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod


class CiCheck(ABC):
    def __init__(self, component, target, args=None):
        self.component = component
        self.target = target
        self.args = args

    @abstractmethod
    def check(self):
        pass


class CiCheckDist(CiCheck):
    pass


class CiCheckSource(CiCheck):
    def __init__(self, component, git_repo, target, args=None):
        super().__init__(component, target, args)
        self.git_repo = git_repo
