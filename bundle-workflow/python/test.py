#!/usr/bin/env python

import os
import argparse
from manifests.bundle_manifest import BundleManifest
from git.git_repository import GitRepository
from test_workflow.local_test_cluster import LocalTestCluster
from test_workflow.integ_test_suite import IntegTestSuite
from test_workflow.test_recorder import TestRecorder
from paths.script_finder import ScriptFinder
from system.temporary_directory import TemporaryDirectory

parser = argparse.ArgumentParser(description = "Test an OpenSearch Bundle")
parser.add_argument('manifest', type = argparse.FileType('r'), help = "Manifest file.")
parser.add_argument('--keep', dest = 'keep', action='store_true', help = "Do not delete the working temporary directory.")
args = parser.parse_args()

manifest = BundleManifest.from_file(args.manifest)
script_finder = ScriptFinder()
test_recorder = TestRecorder(os.path.dirname(args.manifest.name))

with TemporaryDirectory(keep = args.keep) as work_dir:
    os.chdir(work_dir)

    # Spin up a test cluster with security
    # TODO: Refactor this into a TestRun class so we can run with-security and without-security without cut-and-pasting a bunch of code
    cluster = LocalTestCluster(work_dir, manifest, True)
    try:
        cluster.create()

        # For each component, check out the git repo and run `integtest.sh`
        for component in manifest.components:
            print(f'Testing {component.name}')
            repo = GitRepository(component.repository, component.commit_id, os.path.join(work_dir, component.name))
            test_suite = IntegTestSuite(component.name, repo, script_finder, test_recorder)
            test_suite.execute(cluster, True)
    finally:
        cluster.destroy(test_recorder)

    # TODO: Store test results, send notification.
