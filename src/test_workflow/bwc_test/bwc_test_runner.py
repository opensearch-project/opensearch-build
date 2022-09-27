# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import logging
import os
from pathlib import Path

from manifests.build_manifest import BuildComponent, BuildComponents
from manifests.test_manifest import TestComponent, TestManifest
from system.temporary_directory import TemporaryDirectory
from test_workflow.bwc_test.bwc_test_suite import BwcTestSuite
from test_workflow.test_args import TestArgs
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_result.test_suite_results import TestSuiteResults


class BwcTestRunner(abc.ABC):
    args: TestArgs
    test_manifest: TestManifest
    test_dir: str
    test_recorder: TestRecorder
    components: BuildComponents

    def __init__(self, args: TestArgs, test_manifest: TestManifest, components: BuildComponents) -> None:
        self.args = args
        self.test_manifest = test_manifest
        self.components = components

        self.tests_dir = os.path.join(os.getcwd(), "test-results")
        os.makedirs(self.tests_dir, exist_ok=True)
        self.test_recorder = TestRecorder(self.args.test_run_id, "bwc-test", self.tests_dir)

    def run(self) -> TestSuiteResults:
        with TemporaryDirectory(keep=self.args.keep, chdir=True) as work_dir:
            all_results = TestSuiteResults()
            for component in self.components.select(focus=self.args.components):
                if component.name in self.test_manifest.components:
                    test_config = self.test_manifest.components[component.name]
                    if test_config.bwc_test:
                        test_suite = self.__create_test_suite__(component, test_config, work_dir.path)
                        test_results = test_suite.execute_tests()
                        all_results.append(component.name, test_results)
                    else:
                        logging.info(f"Skipping bwc-tests for {component.name}, as it is currently not supported")
                else:
                    logging.info(f"Skipping bwc-tests for {component.name}, as it is currently not declared in the test manifest")

        return all_results

    @abc.abstractmethod
    def __create_test_suite__(self, component: BuildComponent, test_config: TestComponent, work_dir: Path) -> BwcTestSuite:
        pass
