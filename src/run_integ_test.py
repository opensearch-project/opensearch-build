#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import sys

from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestManifest
from system import console
from system.temporary_directory import TemporaryDirectory
from test_workflow.dependency_installer_opensearch import DependencyInstallerOpenSearch
from test_workflow.integ_test.integ_test_suite_opensearch import IntegTestSuiteOpenSearch
from test_workflow.test_args import TestArgs
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_result.test_suite_results import TestSuiteResults


def main():
    args = TestArgs()
    console.configure(level=args.logging_level)
    test_manifest_path = os.path.join(os.path.dirname(__file__), "test_workflow", "config", "opensearch", "test_manifest.yml")
    test_manifest = TestManifest.from_path(test_manifest_path)
    bundle_manifest = BundleManifest.from_urlpath("/".join([args.path.rstrip("/"), "dist/opensearch/manifest.yml"]))
    build_manifest = BuildManifest.from_urlpath("/".join([args.path.rstrip("/"), "builds/opensearch/manifest.yml"]))
    dependency_installer = DependencyInstallerOpenSearch(args.path, build_manifest, bundle_manifest)
    tests_dir = os.path.join(os.getcwd(), "test-results")
    os.makedirs(tests_dir, exist_ok=True)
    with TemporaryDirectory(keep=args.keep, chdir=True) as work_dir:
        test_recorder = TestRecorder(args.test_run_id, "integ-test", tests_dir)
        dependency_installer.install_maven_dependencies()
        all_results = TestSuiteResults()
        for component in bundle_manifest.components.select(focus=args.component):
            if component.name in test_manifest.components:
                test_config = test_manifest.components[component.name]
                if test_config.integ_test:
                    test_suite = IntegTestSuiteOpenSearch(
                        dependency_installer,
                        component,
                        test_config,
                        bundle_manifest,
                        build_manifest,
                        work_dir.name,
                        test_recorder
                    )
                    test_results = test_suite.execute_tests()
                    all_results.append(component.name, test_results)
                else:
                    logging.info(f"Skipping integ-tests for {component.name}, as it is currently not supported")
            else:
                logging.info(f"Skipping integ-tests for {component.name}, as it is currently not declared in the test manifest")

        all_results.log()

        if all_results.failed():
            sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
