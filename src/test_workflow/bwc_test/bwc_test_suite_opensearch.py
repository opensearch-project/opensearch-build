# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from test_workflow.bwc_test.bwc_test_suite import BwcTestSuite


class BwcTestSuiteOpenSearch(BwcTestSuite):

    def __init__(
        self,
        work_dir,
        component,
        test_config,
        test_recorder,
        manifest
    ):

        super().__init__(
            work_dir,
            component,
            test_config,
            test_recorder,
            manifest
        )

    # TODO: enable OpenSearch scripts to accept more arguments
    def get_cmd(self, script, security, manifest_build_location):
        return script

    @property
    def test_artifact_files(self):
        return {
            "opensearch-bwc-test": os.path.join(self.repo_work_dir, "build", "reports", "tests", "bwcTest")
        }
