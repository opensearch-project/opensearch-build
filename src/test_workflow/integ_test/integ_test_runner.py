# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import logging
import os

from system.temporary_directory import TemporaryDirectory
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_result.test_suite_results import TestSuiteResults


class IntegTestRunner(abc.ABC):
    def __init__(self, args, test_manifest):
        self.args = args
        self.test_manifest = test_manifest

        self.tests_dir = os.path.join(os.getcwd(), "test-results")
        os.makedirs(self.tests_dir, exist_ok=True)
        self.test_recorder = TestRecorder(self.args.test_run_id, "integ-test", self.tests_dir)

    def run(self):
        with TemporaryDirectory(keep=self.args.keep, chdir=True) as work_dir:

            all_results = TestSuiteResults()
            for component in self.components.select(focus=self.args.component):
                if component.name in self.test_manifest.components:
                    test_config = self.test_manifest.components[component.name]
                    if test_config.integ_test:
                        test_suite = self.__create_test_suite__(component, test_config, work_dir)
                        test_results = test_suite.execute_tests()
                        all_results.append(component.name, test_results)
                    else:
                        logging.info(f"Skipping integ-tests for {component.name}, as it is currently not supported")
                else:
                    logging.info(f"Skipping integ-tests for {component.name}, as it is currently not declared in the test manifest")

        return all_results
