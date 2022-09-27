# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from sortedcontainers import SortedDict

from test_workflow.test_result.test_result import TestResult  # type: ignore


class TestComponentResults(SortedDict):
    def __init__(self) -> None:
        super(TestComponentResults, self).__init__()

    def __append__(self, result: TestResult) -> None:
        self.__setitem__(result.config, result)

    def append(self, result: TestResult) -> None:
        self.__append__(result)

    def log(self) -> None:
        for result in self.values():
            result.log(str(result))

    @property
    def failed(self) -> bool:
        for result in self.values():
            failed = result.failed
            if failed:
                return True
        return False


TestComponentResults.__test__ = False  # type:ignore
