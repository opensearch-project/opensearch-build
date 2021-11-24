# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from test_workflow.integ_test.service_opensearch import ServiceOpenSearch
from test_workflow.integ_test.service_opensearch_dashboards import ServiceOpenSearchDashboards
from test_workflow.test_cluster import ClusterServiceNotInitializedException, TestCluster
from test_workflow.test_recorder.test_recorder import TestRecorder


class LocalTestClusterOpenSearchDashboards(TestCluster):
    """
    Represents an on-box test cluster. This class runs OpenSearchService first and then OpenSearchServiceDashboards service.
    """

    def __init__(
        self,
        dependency_installer,
        work_dir,
        component_name,
        additional_cluster_config,
        bundle_manifest_opensearch,
        bundle_manifest_opensearch_dashboards,
        security_enabled,
        component_test_config,
        test_recorder: TestRecorder,
    ):
        self.manifest_opensearch = bundle_manifest_opensearch
        self.manifest_opensearch_dashboards = bundle_manifest_opensearch_dashboards

        self.work_dir = os.path.join(work_dir, "local-test-cluster")
        os.makedirs(self.work_dir, exist_ok=True)
        self.component_name = component_name
        self.security_enabled = security_enabled
        self.component_test_config = component_test_config
        self.additional_cluster_config = additional_cluster_config
        self.save_logs = test_recorder.local_cluster_logs
        self.dependency_installer = dependency_installer
        self.service_opensearch = None
        self.service_opensearch_dashboards = None

    def create_cluster(self):

        # Need to extra the test data part outside of Service. Here is a good example where we just run OpenSearch endpoint but do not run its test.
        # Some follow up comments of this https://github.com/opensearch-project/opensearch-build/pull/1128/files
        self.service_opensearch = ServiceOpenSearch(
            self.manifest_opensearch,
            {},
            self.component_test_config,
            {},
            self.security_enabled,
            self.dependency_installer,
            self.save_logs,
            self.work_dir)

        self.service_opensearch.start()
        self.service_opensearch.wait_for_service()

        self.service_opensearch_dashboards = ServiceOpenSearchDashboards(
            self.manifest_opensearch_dashboards,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            self.security_enabled,
            self.dependency_installer,
            self.save_logs,
            self.work_dir)

        self.service_opensearch_dashboards.start()
        self.service_opensearch_dashboards.wait_for_service()

    def endpoint(self):
        return "localhost"

    def port(self):
        return 5601

    def destroy(self):
        if not self.service_opensearch or not self.service_opensearch_dashboards:
            raise ClusterServiceNotInitializedException()

        self.service_opensearch.terminate()
        self.service_opensearch_dashboards.terminate()
