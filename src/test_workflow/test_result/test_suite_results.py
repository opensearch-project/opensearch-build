from sortedcontainers import SortedDict

from test_workflow.test_result.test_component_results import TestComponentResults  # type: ignore


class TestSuiteResults(SortedDict):
    def __init__(self) -> None:
        super(TestSuiteResults, self).__init__()

    def __append__(self, component: str, test_result_component: TestComponentResults) -> None:
        self.__setitem__(component, test_result_component)

    def append(self, component: str, test_result_component: TestComponentResults) -> None:
        self.__append__(component, test_result_component)

    def log(self) -> None:
        for result in self.values():
            result.log()

    def failed(self) -> bool:
        return any(result.failed for result in self.values())


TestSuiteResults.__test__ = False  # type:ignore
