# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
from abc import ABC, abstractmethod
from typing import Any

from ci_workflow.ci_args import CiArgs


class CiManifest(ABC):
    def __init__(self, manifest: Any, args: CiArgs) -> None:
        self.manifest = manifest
        self.args = args

    def check(self) -> None:
        try:
            self.__check__()
        except:
            logging.error("CI Manifest check failed")
            raise

    @abstractmethod
    def __check__(self) -> None:
        pass
