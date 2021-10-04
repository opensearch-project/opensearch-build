from sortedcontainers import SortedDict  # type: ignore


class TestComponentResults(SortedDict):
    def __init__(self):
        super(TestComponentResults, self).__init__()

    def __append__(self, result):
        self.__setitem__(result.config, result)

    def append(self, result):
        self.__append__(result)

    def log(self):
        for result in self.values():
            result.log(str(result))

    @property
    def failed(self):
        for result in self.values():
            failed = result.failed
            if failed:
                return True
        return False


TestComponentResults.__test__ = False  # type:ignore
