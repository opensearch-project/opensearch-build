#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from manifests.bundle_manifest import BundleManifest
from system.temporary_directory import TemporaryDirectory
from test_workflow.bwc_test_suite import BwcTestSuite
from test_workflow.integ_test_workflow.integ_test_suite import IntegTestSuite
from test_workflow.local_test_cluster import LocalTestCluster
from test_workflow.test_args import TestArgs
from test_workflow.test_component import TestComponent
from test_workflow.test_recorder import TestRecorder

args = TestArgs()
manifest = BundleManifest.from_file(args.manifest)
test_recorder = TestRecorder(os.path.dirname(manifest.name))


def integ_test_suite():
    with TemporaryDirectory(keep=args.keep) as work_dir:
        os.chdir(work_dir)

        # Spin up a test cluster
        cluster = LocalTestCluster(manifest)
        cluster.create()

        # For each component, check out the git repo and run `integtest.sh`
        try:
            for component in manifest.components:
                print(component.name)
                test_component = TestComponent(
                    component.repository, component.commit_id
                )
                repo = test_component.checkout(os.path.join(work_dir, component.name))
                test_suite = IntegTestSuite(component.name, repo)
                test_suite.execute(cluster)
        finally:
            cluster.destroy()

        # TODO: Store test results, send notification.


def bwc_test_suite():
    test_suite = BwcTestSuite(manifest, args.component, args.keep)
    test_suite.execute()


integ_test_suite()
bwc_test_suite()
