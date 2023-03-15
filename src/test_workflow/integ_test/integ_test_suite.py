# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import abc
import logging
from pathlib import Path
from typing import Any, Dict

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.test_recorder.log_recorder import LogRecorder
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_result.test_component_results import TestComponentResults


class IntegTestSuite(abc.ABC):
    work_dir: Path
    component: Any
    test_config: Any
    test_recorder: TestRecorder
    dependency_installer: DependencyInstaller
    bundle_manifest: BundleManifest
    build_manifest: BuildManifest
    save_logs: LogRecorder
    additional_cluster_config: dict

    """
    Kicks off integration tests for a component based on test configurations provided in
    test_support_matrix.yml
    """

    def __init__(
        self,
        work_dir: Path,
        component: Any,
        test_config: Any,
        test_recorder: TestRecorder,
        dependency_installer: DependencyInstaller,
        bundle_manifest: BundleManifest,
        build_manifest: BuildManifest
    ) -> None:
        self.work_dir = work_dir
        self.component = component
        self.test_config = test_config
        self.test_recorder = test_recorder

        self.dependency_installer = dependency_installer
        self.bundle_manifest = bundle_manifest
        self.build_manifest = build_manifest

        self.save_logs = test_recorder.test_results_logs
        self.additional_cluster_config = None

    @abc.abstractmethod
    def execute_tests(self) -> TestComponentResults:
        pass

    @abc.abstractmethod
    def multi_execute_integtest_sh(self, cluster_endpoints: list, security: bool, test_config: str) -> int:
        pass

    def is_security_enabled(self, config: str) -> bool:
        if config in ["with-security", "without-security"]:
            return True if config == "with-security" else False
        else:
            raise InvalidTestConfigError("Unsupported test config: " + config)

    def pretty_print_message(self, message: str) -> None:
        logging.info("===============================================")
        logging.info(message)
        logging.info("===============================================")

    @property
    @abc.abstractmethod
    def test_artifact_files(self) -> Dict[str, str]:
        pass


class InvalidTestConfigError(Exception):
    pass
