# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import logging
from typing import Callable


class TestResult:
    component: str
    config: dict
    status: int

    def __init__(self, component: str, config: dict, status: int) -> None:
        self.component = component
        self.config = config
        self.status = status

    @property
    def __test_result(self) -> str:
        return "PASS" if self.status == 0 else "FAIL"

    def __str__(self) -> str:
        return "| {:20s} | {:20s} | {:5s} | {:4d} |".format(self.component, self.config, self.__test_result, self.status)

    def __logger(self) -> Callable:
        return logging.info if self.status == 0 else logging.error

    def log(self, result: str) -> None:
        logger = self.__logger()
        logger(result)

    @property
    def failed(self) -> bool:
        return True if self.status != 0 else False


TestResult.__test__ = False  # type:ignore
