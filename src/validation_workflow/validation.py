# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from abc import ABC, abstractmethod
from typing import Any

from validation_workflow.validation_args import ValidationArgs


class Validation(ABC):
    """
    Abstract class for all types of artifact validation
    """

    def __init__(self, args: ValidationArgs) -> None:
        super().__init__()
        self.args = args

    def run(self) -> Any:
        try:
            return self.download_artifacts() and self.installation() and self.start_cluster() and self.validation() and self.cleanup()
        except Exception:
            return False

    @abstractmethod
    def download_artifacts(self) -> bool:
        pass

    @abstractmethod
    def installation(self) -> bool:
        pass

    @abstractmethod
    def start_cluster(self) -> bool:
        pass

    @abstractmethod
    def validation(self) -> bool:
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        pass
