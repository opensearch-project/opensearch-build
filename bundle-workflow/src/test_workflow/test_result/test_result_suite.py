from sortedcontainers import SortedDict  # type: ignore


class TestResultsSuite(SortedDict):
    def __init__(self):
        super(TestResultsSuite, self).__init__()

    def __append__(self, component, test_result_component):
        self.__setitem__(component, test_result_component)

    def append(self, component, test_result_component):
        self.__append__(component, test_result_component)

    def log(self):
        for result in self.values():
            result.log()

    def status(self):
        test_failed = False
        for result in self.values():
            test_failed = result.test_status()
        return test_failed
