import os
import sys
import tempfile
import urllib.request
from test_workflow.manifest import BundleManifest
from test_workflow.test_cluster import LocalTestCluster
from test_workflow.git import GitRepository
from test_workflow.integ_test import IntegTestSuite

if (len(sys.argv) < 2):
    print("Usage: tester.py /path/to/manifest")
    exit(1)

with tempfile.TemporaryDirectory() as work_dir:
    os.chdir(work_dir)

    # Download the manifest
    with urllib.request.urlopen(sys.argv[1]) as response:
        text = response.read()
        manifest = BundleManifest.from_text(text)

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
