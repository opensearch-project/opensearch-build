# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from abc import ABC, abstractmethod

from build_workflow.build_target import BuildTarget


class BuildArtifactCheck(ABC):
    class BuildArtifactInvalidError(Exception):
        def __init__(self, path: str, message: str) -> None:
            self.path = path
            super().__init__(f"Artifact {os.path.basename(path)} is invalid. {message}")

    def __init__(self, target: BuildTarget) -> None:
        self.target = target

    @abstractmethod
    def check(self, path: str) -> None:
        pass
