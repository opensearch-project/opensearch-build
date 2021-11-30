# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod
from typing import Any
from git.git_repository import GitRepository

from manifests_workflow.component import Component


class CiCheck(ABC):
    def __init__(self, component: Component, target: None, args: Any=None) -> None:
        self.component = component
        self.target = target
        self.args = args

    @abstractmethod
    def check(self) -> None:
        pass


class CiCheckDist(CiCheck):
    pass


class CiCheckSource(CiCheck):
    def __init__(self, component: Component, git_repo: GitRepository, target: None, args: Any=None) -> None:
        super().__init__(component, target, args)
        self.git_repo = git_repo
