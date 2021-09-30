import logging


class TestResult:
    def __init__(self, component, config, status):
        self.component = component
        self.config = config
        self.status = status

    @property
    def __test_result(self):
        return 'PASS' if self.status == 0 else 'FAIL'

    def __str__(self):
        return f"{self.__test_result} Test for {self.component} {self.config} with status code {self.status}"  
    
    def __logger(self):
        return logging.info if self.status == 0 else logging.error

    def log(self):
        self.__logger(str(self))
