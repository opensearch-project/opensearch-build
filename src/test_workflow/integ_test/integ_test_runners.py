# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from test_workflow.integ_test.integ_test_runner_opensearch import IntegTestRunnerOpenSearch
from test_workflow.integ_test.integ_test_runner_opensearch_dashboards import IntegTestRunnerOpenSearchDashboards


class IntegTestRunners:
    def __klass(name):
        if name == "OpenSearch Dashboards":
            return IntegTestRunnerOpenSearchDashboards
        else:
            return IntegTestRunnerOpenSearch

    @classmethod
    def from_test_manifest(cls, args, test_manifest):
        return cls.__klass(test_manifest.name)(args, test_manifest)
