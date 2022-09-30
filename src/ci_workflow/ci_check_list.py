# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod
from typing import Any

from ci_workflow.ci_target import CiTarget


class CiCheckList(ABC):
    def __init__(self, component: Any, target: CiTarget) -> None:
        self.component = component
        self.target = target

    @abstractmethod
    def checkout(self, work_dir: str) -> None:
        pass

    @abstractmethod
    def check(self) -> None:
        pass
