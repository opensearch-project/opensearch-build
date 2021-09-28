#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import sys

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestManifest
from system import console
from system.temporary_directory import TemporaryDirectory
from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.integ_test_suite import IntegTestSuite
from test_workflow.test_args import TestArgs


def pull_build_repo(work_dir):
    logging.info("Pulling opensearch-build")
    GitRepository(
        "https://github.com/opensearch-project/opensearch-build.git",
        "main",
        os.path.join(work_dir, "opensearch-build"),
    )


def main():
    args = TestArgs()
    console.configure(level=args.logging_level)
    test_manifest_path = os.path.join(os.path.dirname(__file__), 'test_workflow/config/test_manifest.yml')
    test_manifest = TestManifest.from_path(test_manifest_path)
    integ_test_config = dict()
    for component in test_manifest.components:
        if component.integ_test is not None:
            integ_test_config[component.name] = component
    with TemporaryDirectory(keep=args.keep) as work_dir:
        logging.info("Switching to temporary work_dir: " + work_dir)
        os.chdir(work_dir)
        bundle_manifest = BundleManifest.from_s3(
            args.s3_bucket, args.build_id, args.opensearch_version, args.architecture, work_dir)
        build_manifest = BuildManifest.from_s3(
            args.s3_bucket, args.build_id, args.opensearch_version, args.architecture, work_dir)
        pull_build_repo(work_dir)
        DependencyInstaller(build_manifest.build).install_all_maven_dependencies()
        failed_components = dict()
        passed_components = dict()
        for component in bundle_manifest.components:
            if component.name in integ_test_config.keys():
                test_suite = IntegTestSuite(
                    component,
                    integ_test_config[component.name],
                    bundle_manifest,
                    build_manifest,
                    work_dir,
                    args.s3_bucket
                )
                status, security = test_suite.execute()
                if status != 0:
                    failed_components[component.name] = [status, security]
                else:
                    passed_components[component.name] = [status, security]
            else:
                logging.info(
                    "Skipping tests for %s, as it is currently not supported"
                    % component.name
                )

        if passed_components:
            for component, result in passed_components.items():
                logging.info(f'PASS: Integration Test for {component} {result[1]} with status code {result[0]}')

        if failed_components:
            for component, result in failed_components.items():
                logging.error(f'FAIL: Integration Test for {component} {result[1]} with status code {result[0]}')
            sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
