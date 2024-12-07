# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

import yaml

from manifests.component_manifest import Components
from manifests.test_manifest import TestManifest
from system.temporary_directory import TemporaryDirectory
from test_workflow.smoke_test.smoke_test_cluster_opensearch import SmokeTestClusterOpenSearch
from test_workflow.test_args import TestArgs
from test_workflow.test_recorder.test_recorder import TestRecorder


class SmokeTestRunner(abc.ABC):
    args: TestArgs
    test_manifest: TestManifest
    tests_dir: str
    test_recorder: TestRecorder
    components: Components

    def __init__(self, args: TestArgs, test_manifest: TestManifest) -> None:
        self.args = args
        self.test_manifest = test_manifest
        self.tests_dir = os.path.join(os.getcwd(), "test-results")
        os.makedirs(self.tests_dir, exist_ok=True)
        self.test_recorder = TestRecorder(self.args.test_run_id, "smoke-test", self.tests_dir, args.base_path)
        self.save_log = self.test_recorder.test_results_logs
        self.version = ""

    def start_test(self, work_dir: Path) -> Any:
        pass

    def extract_paths_from_yaml(self, component: str, version: str) -> Any:
        base_path = os.path.dirname(os.path.abspath(__file__))
        paths = [
            os.path.join(base_path, "smoke_tests_spec", f"{version.split('.')[0]}.x", f"{component}.yml"),
            os.path.join(base_path, "smoke_tests_spec", "default", f"{component}.yml")
        ]
        for file_path in paths:
            if os.path.exists(file_path):
                logging.info(f"Component spec for {component} with path {file_path} is found.")
                with open(file_path, 'r') as file:
                    data = yaml.safe_load(file)  # Load the YAML content
                # Extract paths
                paths = data.get('paths', {})
                return paths
        logging.error("No spec found.")
        sys.exit(1)

    def convert_parameter_json(self, data: list) -> str:
        return "\n".join(json.dumps(item) for item in data) + "\n" if data else ""

    # Essential of initiate the testing phase. This function is called by the run_smoke_test.py
    def run(self) -> Any:
        with TemporaryDirectory(keep=self.args.keep, chdir=True) as work_dir:

            logging.info("Initiating smoke tests.")
            test_cluster = SmokeTestClusterOpenSearch(self.args, os.path.join(work_dir.path), self.test_recorder)
            self.version = test_cluster.cluster_version()
            test_cluster.__start_cluster__(os.path.join(work_dir.path))
            is_cluster_ready = False
            for i in range(10):
                logging.info(f"Attempt {i} of 10 to check cluster.")
                if test_cluster.__check_cluster_ready__():
                    is_cluster_ready = True
                    break
                time.sleep(10)
            try:
                if is_cluster_ready:
                    results_data = self.start_test(work_dir.path)
                else:
                    logging.info("Cluster is not ready after 10 attempts.")
            finally:
                logging.info("Terminating and uninstalling the cluster.")
                test_cluster.__uninstall__()
        return results_data
