# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import List

from manifests.bundle_manifest import BundleManifest
from test_workflow.dependency_installer_opensearch import DependencyInstallerOpenSearch
from test_workflow.dependency_installer_opensearch_dashboards import DependencyInstallerOpenSearchDashboards
from test_workflow.integ_test.service import Service
from test_workflow.integ_test.service_opensearch import ServiceOpenSearch
from test_workflow.integ_test.service_opensearch_dashboards import ServiceOpenSearchDashboards
from test_workflow.test_cluster import TestCluster
from test_workflow.test_recorder.test_recorder import TestRecorder


class LocalTestClusterOpenSearchDashboards(TestCluster):
    manifest_opensearch: BundleManifest
    manifest_opensearch_dashboards: BundleManifest
    service_opensearch: ServiceOpenSearch
    service_opensearch_dashboards: ServiceOpenSearchDashboards

    """
    Represents an on-box test cluster. This class runs OpenSearchService first and then OpenSearchServiceDashboards service.
    """

    def __init__(
        self,
        dependency_installer_opensearch: DependencyInstallerOpenSearch,
        dependency_installer_opensearch_dashboards: DependencyInstallerOpenSearchDashboards,
        work_dir: str,
        component_name: str,
        additional_cluster_config: dict,
        bundle_manifest_opensearch: BundleManifest,
        bundle_manifest_opensearch_dashboards: BundleManifest,
        security_enabled: bool,
        component_test_config: str,
        test_recorder: TestRecorder,
    ) -> None:
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

        self.dependency_installer_opensearch = dependency_installer_opensearch
        self.dependency_installer_opensearch_dashboards = dependency_installer_opensearch_dashboards

        self.service_opensearch = ServiceOpenSearch(
            self.manifest_opensearch.build.version,
            self.manifest_opensearch.build.distribution,
            {},
            self.security_enabled,
            self.dependency_installer_opensearch,
            self.work_dir)

        self.service_opensearch_dashboards = ServiceOpenSearchDashboards(
            self.manifest_opensearch_dashboards.build.version,
            self.manifest_opensearch_dashboards.build.distribution,
            self.additional_cluster_config,
            self.security_enabled,
            self.dependency_installer_opensearch_dashboards,
            self.work_dir)

    @property
    def endpoint(self) -> str:
        return "localhost"

    @property
    def port(self) -> int:
        return 5601

    @property
    def service(self) -> Service:
        return self.service_opensearch_dashboards

    @property
    def dependencies(self) -> List[Service]:
        return [
            self.service_opensearch
        ]
