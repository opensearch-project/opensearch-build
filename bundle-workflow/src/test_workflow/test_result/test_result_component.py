from sortedcontainers import SortedDict  # type: ignore


class TestResultsComponent(SortedDict):
    def __init__(self):
        super(TestResultsComponent, self).__init__()

    def __append__(self, result):
        self.__setitem__(result.config, result)

    def append(self, result):
        self.__append__(result)

    def log(self):
        for result in self.values():
            result.log(str(result))

    def test_status(self):
        test_failed = False
        for result in self.values():
            if result.status != 0:
                test_failed = True
        return test_failed
