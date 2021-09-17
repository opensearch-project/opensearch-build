#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess
import sys

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestManifest
from system import console
from system.temporary_directory import TemporaryDirectory
from test_workflow.integ_test.integ_test_suite import IntegTestSuite
from test_workflow.test_args import TestArgs

# TODO: 1. log test related logging into a log file. Output only workflow logs on shell.
# TODO: 2. Move common functions to utils.py

COMMON_DEPENDENCIES = ["OpenSearch", "common-utils", "job-scheduler", "alerting"]


# TODO: replace with DependencyProvider - https://github.com/opensearch-project/opensearch-build/issues/283
def pull_common_dependencies(work_dir, build_manifest):
    logging.info("Pulling common dependencies for integration tests")
    logging.info("Pulling opensearch-build")
    os.chdir(work_dir)
    GitRepository(
        "https://github.com/opensearch-project/opensearch-build.git",
        "main",
        os.path.join(work_dir, "opensearch-build"),
    )
    for component in build_manifest.components:
        if component.name in COMMON_DEPENDENCIES:
            logging.info("Pulling " + component.name)
            GitRepository(
                component.repository,
                component.commit_id,
                os.path.join(work_dir, 'dependencies', component.name),
            )


# TODO: replace with DependencyProvider - https://github.com/opensearch-project/opensearch-build/issues/283
def sync_dependencies_to_maven_local(work_dir, manifest_build_ver):
    dependencies_dir = os.path.join(work_dir, 'dependencies')
    opensearch_dir = os.path.join(dependencies_dir, 'OpenSearch')
    os.chdir(opensearch_dir)
    deps_script = os.path.join(
        work_dir,
        "opensearch-build/tools/standard-test/integtest_dependencies_opensearch.sh",
    )
    subprocess.check_output(
        f"{deps_script} opensearch {manifest_build_ver}",
        cwd=opensearch_dir,
        shell=True
    )
    common_utils_dir = os.path.join(dependencies_dir, 'common-utils')
    os.chdir(common_utils_dir)
    subprocess.check_output(
        f"{deps_script} common-utils {manifest_build_ver}",
        cwd=common_utils_dir,
        shell=True
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
        pull_common_dependencies(work_dir, build_manifest)
        sync_dependencies_to_maven_local(work_dir, build_manifest.build.version)
        for component in bundle_manifest.components:
            if component.name in integ_test_config.keys():
                test_suite = IntegTestSuite(
                    component,
                    integ_test_config[component.name],
                    bundle_manifest,
                    work_dir,
                    args.s3_bucket
                )
                test_suite.execute()
            else:
                logging.info(
                    "Skipping tests for %s, as it is currently not supported"
                    % component.name
                )


if __name__ == "__main__":
    sys.exit(main())
