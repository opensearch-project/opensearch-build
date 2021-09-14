# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod


class CiCheck(ABC):
    def __init__(self, component, git_repo, target):
        self.component = component
        self.git_repo = git_repo
        self.target = target

    @abstractmethod
    def check(self):
        pass
