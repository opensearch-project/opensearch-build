# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from abc import ABC, abstractmethod
from typing import Any

from build_workflow.build_recorder import BuildRecorder
from build_workflow.build_target import BuildTarget


class Builder(ABC):
    def __init__(self, component: Any, target: BuildTarget) -> None:
        self.output_path = "builds"
        self.component = component
        self.target = target

    @abstractmethod
    def checkout(self, work_dir: str) -> None:
        pass

    @abstractmethod
    def build(self, build_recorder: BuildRecorder) -> None:
        pass

    @abstractmethod
    def export_artifacts(self, build_recorder: BuildRecorder) -> None:
        pass
