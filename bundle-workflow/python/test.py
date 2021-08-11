#!/usr/bin/env python

import os
import tempfile
import argparse
from manifests.bundle_manifest import BundleManifest
from test_workflow.test_cluster import LocalTestCluster
from test_workflow.git import GitRepository
from test_workflow.integ_test import IntegTestSuite

parser = argparse.ArgumentParser(description = "Test an OpenSearch Bundle")
parser.add_argument('manifest', type = argparse.FileType('r'), help="Manifest file.")
args = parser.parse_args()

manifest = BundleManifest.from_file(args.manifest)

with tempfile.TemporaryDirectory() as work_dir:
    os.chdir(work_dir)

    # Spin up a test cluster
    cluster = LocalTestCluster(manifest.bundle_location)

    # For each component, check out the git repo and run `integtest.sh`
    for component in manifest.components():
        print(component.name())
        repo = GitRepository(component.repository_url(), component.commit_id())
        test_suite = IntegTestSuite(component.name(), repo)
        test_suite.execute(cluster)

    cluster.destroy()

    # TODO: Store test results, send notification.
