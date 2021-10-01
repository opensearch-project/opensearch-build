from sortedcontainers import SortedDict  # type: ignore


class TestSuiteResults(SortedDict):
    def __init__(self):
        super(TestSuiteResults, self).__init__()

    def __append__(self, component, test_result_component):
        self.__setitem__(component, test_result_component)

    def append(self, component, test_result_component):
        self.__append__(component, test_result_component)

    def log(self):
        for result in self.values():
            result.log()

    def status(self):
        for result in self.values():
            test_failed = result.failed
            if test_failed:
                return True
        return False


TestSuiteResults.__test__ = False  # type:ignore
