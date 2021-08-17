#!/usr/bin/env python

import os
import tempfile
import argparse
import pathlib
from manifests.bundle_manifest import BundleManifest
from git.git_repository import GitRepository
from test_workflow.test_cluster import LocalTestCluster
from test_workflow.integ_test_suite import IntegTestSuite

parser = argparse.ArgumentParser(description = "Test an OpenSearch Bundle")
parser.add_argument('manifest', type = argparse.FileType('r'), help="Manifest file.")
parser.add_argument('--workdir', type = pathlib.Path, help="Specify a working directory. If this is not specified then a temporary directory will be used. This option is mostly useful for debugging - it will leave the contents of the directory after the tool finishes, whereas a temporary directory will be automatically deleted.")
args = parser.parse_args()

manifest = BundleManifest.from_file(args.manifest)
with tempfile.TemporaryDirectory() as temp_work_dir:
    if args.workdir is None:
        work_dir = temp_work_dir
    else:
        work_dir = args.workdir
        os.makedirs(work_dir, exist_ok = True)

    os.chdir(work_dir)

    # Spin up a test cluster
    cluster = LocalTestCluster(manifest)
    cluster.create()

    # For each component, check out the git repo and run `integtest.sh`
    try:
        for component in manifest.components:
            print(component.name)
            repo = GitRepository(component.repository, component.commit_id, os.path.join(work_dir, component.name))
            test_suite = IntegTestSuite(component.name, repo)
            test_suite.execute(cluster)
    finally:
        cluster.destroy()

    # TODO: Store test results, send notification.
