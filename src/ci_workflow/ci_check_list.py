# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
from abc import ABC, abstractmethod
from typing import Any

from ci_workflow.ci_target import CiTarget


class CiCheckList(ABC):
    def __init__(self, component: Any, target: CiTarget) -> None:
        self.component = component
        try:
            self.component_ref_is_sha1 = True if len(self.component.ref) == 40 and int(self.component.ref, 16) else False
            logging.debug("sha1 exists in ref")
        except AttributeError:
            logging.debug("sha1 not exist in ref")
        self.target = target

    @abstractmethod
    def checkout(self, work_dir: str) -> None:
        pass

    @abstractmethod
    def check(self) -> None:
        pass
