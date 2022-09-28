# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from manifests.test_manifest import TestManifest
from test_workflow.bwc_test.bwc_test_runner import BwcTestRunner
from test_workflow.bwc_test.bwc_test_runner_opensearch import BwcTestRunnerOpenSearch
from test_workflow.bwc_test.bwc_test_runner_opensearch_dashboards import BwcTestRunnerOpenSearchDashboards
from test_workflow.test_args import TestArgs


class BwcTestRunners:
    RUNNERS = {
        "OpenSearch": BwcTestRunnerOpenSearch,
        "OpenSearch Dashboards": BwcTestRunnerOpenSearchDashboards
    }

    @classmethod
    def from_test_manifest(cls, args: TestArgs, test_manifest: TestManifest) -> BwcTestRunner:
        return cls.RUNNERS[test_manifest.name](args, test_manifest)
