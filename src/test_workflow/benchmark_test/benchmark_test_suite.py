# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess
from abc import ABC, abstractmethod
from typing import Any

from test_workflow.benchmark_test.benchmark_args import BenchmarkArgs


class BenchmarkTestSuite(ABC):
    def __init__(
            self,
            args: BenchmarkArgs,
            endpoint: Any = None,
            security: bool = False,
            password: str = ''
    ) -> None:
        self.endpoint = endpoint
        self.security = security
        self.args = args
        self.password = password

    @abstractmethod
    def form_command(self) -> str:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass

    def cleanup(self) -> None:
        subprocess.check_call(f"docker rm -f docker-container-{self.args.stack_suffix}", cwd=os.getcwd(), shell=True)
