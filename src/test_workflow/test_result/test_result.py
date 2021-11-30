import logging
from types import FunctionType

from manifests_workflow.component import Component


class TestResult:
    def __init__(self, component: Component, config, status) -> None:
        self.component = component
        self.config = config
        self.status = status

    @property
    def __test_result(self) -> str:
        return "PASS" if self.status == 0 else "FAIL"

    def __str__(self) -> str:
        return "| {:20s} | {:20s} | {:5s} | {:4d} |".format(self.component, self.config, self.__test_result, self.status)

    def __logger(self) -> FunctionType:
        return logging.info if self.status == 0 else logging.error

    def log(self, result: str) -> None:
        log = self.__logger()
        log(result)

    @property
    def failed(self) -> bool:
        return True if self.status != 0 else False


TestResult.__test__ = False  # type:ignore
