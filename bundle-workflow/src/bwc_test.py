#!/usr/bin/env python
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import sys

from manifests.bundle_manifest import BundleManifest
from system.temporary_directory import TemporaryDirectory
from test_workflow.bwc_test_suite import BwcTestSuite
from test_workflow.test_args import TestArgs


def main():
    args = TestArgs()
    manifest = BundleManifest.from_file(args.manifest)
    with TemporaryDirectory(keep=args.keep) as work_dir:
        os.chdir(work_dir)
        # For each component, check out the git repo and run `bwctest.sh`
        for component in manifest.components:
            if args.component is None or args.component == component.name:
                # TODO: Store and report test results, send notification via {console_output}
                BwcTestSuite(manifest, component, work_dir).component_bwc_tests()


if __name__ == "__main__":
    sys.exit(main())
