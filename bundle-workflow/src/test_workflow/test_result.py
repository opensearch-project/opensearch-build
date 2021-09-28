import logging


class TestResult:
    def __init__(self):
        self.final_result = list()

    def append_result(self, component, config, status):
        self.final_result.append((component, config, status))

    def generate_summary_report(self):
        test_failed = False
        for component, config, status in self.final_result:
            if status != 0:
                test_failed = True
                logging.error(f"FAIL: Integration Test for {component} {config} with status code {status}")
            else:
                logging.info(f"PASS: Integration Test for {component} {config} with status code {status}")
        return test_failed
