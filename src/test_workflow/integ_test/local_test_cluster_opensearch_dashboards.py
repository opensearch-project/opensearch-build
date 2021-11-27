# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from test_workflow.integ_test.service_opensearch import ServiceOpenSearch
from test_workflow.integ_test.service_opensearch_dashboards import ServiceOpenSearchDashboards
from test_workflow.test_cluster import TestCluster
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
        super().__init__(
            work_dir,
            component_name,
            component_test_config,
            security_enabled,
            additional_cluster_config,
            test_recorder.local_cluster_logs
        )

        self.manifest_opensearch = bundle_manifest_opensearch
        self.manifest_opensearch_dashboards = bundle_manifest_opensearch_dashboards

        self.dependency_installer = dependency_installer

        self.service_opensearch = ServiceOpenSearch(
            self.manifest_opensearch.build.version,
            {},
            self.security_enabled,
            self.dependency_installer,
            self.work_dir)

        build = self.manifest_opensearch_dashboards.build

        self.service_opensearch_dashboards = ServiceOpenSearchDashboards(
            build.version,
            build.platform,
            build.architecture,
            self.additional_cluster_config,
            self.security_enabled,
            self.dependency_installer,
            self.work_dir)

    def port(self):
        return 5601

    def service(self):
        return [
            self.service_opensearch_dashboards,
        ]

    def dependencies(self):
        return [
            self.service_opensearch,
        ]
