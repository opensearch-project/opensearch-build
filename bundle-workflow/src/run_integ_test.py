#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import argparse
import os
import subprocess
import sys

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestManifest
from system.temporary_directory import TemporaryDirectory
from test_workflow.integ_test_suite import IntegTestSuite

# TODO: 1. log test related logging into a log file. Output only workflow logs on shell.
# TODO: 2. Move common functions to utils.py


COMMON_DEPENDENCIES = ["OpenSearch", "common-utils", "job-scheduler", "alerting"]


def parse_arguments():
    parser = argparse.ArgumentParser(description="Test an OpenSearch Bundle")
    parser.add_argument(
        "--bundle-manifest", type=argparse.FileType("r"), help="Bundle Manifest file."
    )
    parser.add_argument(
        "--build-manifest", type=argparse.FileType("r"), help="Build Manifest file."
    )
    parser.add_argument(
        "--test-manifest", type=argparse.FileType("r"), help="Test Manifest file."
    )
    parser.add_argument(
        "--keep",
        dest="keep",
        action="store_true",
        help="Do not delete the working temporary directory.",
    )
    args = parser.parse_args()
    return args


# TODO: replace with DependencyProvider - https://github.com/opensearch-project/opensearch-build/issues/283
def pull_common_dependencies(work_dir, build_manifest):
    print("Pulling common dependencies for integration tests")
    print("Pulling opensearch-build")
    os.chdir(work_dir)
    GitRepository(
        "https://github.com/opensearch-project/opensearch-build.git",
        "main",
        os.path.join(work_dir, "opensearch-build"),
    )
    for component in build_manifest.components:
        if component.name in COMMON_DEPENDENCIES:
            print("Pulling " + component.name)
            GitRepository(
                component.repository,
                component.commit_id,
                os.path.join(work_dir, component.name),
            )


# TODO: replace with DependencyProvider - https://github.com/opensearch-project/opensearch-build/issues/283
def sync_dependencies_to_maven_local(work_dir, manifest_build_ver):
    os.chdir(work_dir + "/OpenSearch")
    deps_script = os.path.join(
        work_dir,
        "opensearch-build/tools/standard-test/integtest_dependencies_opensearch.sh",
    )
    subprocess.run(
        f"{deps_script} opensearch {manifest_build_ver}",
        shell=True,
        check=True,
        capture_output=True,
    )
    os.chdir(work_dir + "/common-utils")
    subprocess.run(
        f"{deps_script} common-utils {manifest_build_ver}",
        shell=True,
        check=True,
        capture_output=True,
    )


def main():
    args = parse_arguments()
    bundle_manifest = BundleManifest.from_file(args.bundle_manifest)
    build_manifest = BuildManifest.from_file(args.build_manifest)
    test_manifest = TestManifest.from_file(args.test_manifest)
    integ_test_config = dict()
    for component in test_manifest.components:
        if component.integ_test is not None:
            integ_test_config[component.name] = component
    with TemporaryDirectory(keep=args.keep) as work_dir:
        print("Switching to temporary work_dir: " + work_dir)
        os.chdir(work_dir)
        pull_common_dependencies(work_dir, build_manifest)
        sync_dependencies_to_maven_local(work_dir, build_manifest.build.version)
        for component in bundle_manifest.components:
            if component.name in integ_test_config.keys():
                test_suite = IntegTestSuite(
                    component,
                    integ_test_config[component.name],
                    bundle_manifest,
                    work_dir,
                )
                test_suite.execute()
            else:
                print(
                    "Skipping tests for %s, as it is currently not supported"
                    % component.name
                )


if __name__ == "__main__":
    sys.exit(main())
