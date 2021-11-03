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
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_result.test_suite_results import TestSuiteResults


def pull_build_repo(work_dir):
    logging.info("Pulling opensearch-build")
    with GitRepository("https://github.com/opensearch-project/opensearch-build.git", "main", os.path.join(work_dir, "opensearch-build")) as repo:
        logging.info(f"Checked out opensearch-build into {repo.dir}")


def main():
    args = TestArgs()
    console.configure(level=args.logging_level)

    test_manifest_path = os.path.join(os.path.dirname(__file__), "test_workflow", "config", "test_manifest.yml")
    test_manifest = TestManifest.from_path(test_manifest_path)
    with TemporaryDirectory(keep=args.keep, chdir=True) as work_dir:
        logging.info(f"Switching to temporary work_dir: {work_dir.name}")
        test_recorder = TestRecorder(args.test_run_id, "integ-test", work_dir.name)
        bundle_manifest = BundleManifest.from_s3(args.s3_bucket, args.build_id, args.opensearch_version, args.platform, args.architecture, work_dir.name)
        build_manifest = BuildManifest.from_s3(args.s3_bucket, args.build_id, args.opensearch_version, args.platform, args.architecture, work_dir.name)
        pull_build_repo(work_dir.name)
        DependencyInstaller(build_manifest.build).install_all_maven_dependencies()
        all_results = TestSuiteResults()
        for component in bundle_manifest.components.values():
            if component.name in test_manifest.components:
                test_config = test_manifest.components[component.name]
                if test_config.integ_test:
                    test_suite = IntegTestSuite(
                        component, test_config, bundle_manifest, build_manifest, work_dir.name, args.s3_bucket, test_recorder
                    )
                    test_results = test_suite.execute()
                    all_results.append(component.name, test_results)
            else:
                logging.info("Skipping tests for %s, as it is currently not supported" % component.name)

        all_results.log()

        if all_results.failed():
            sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
