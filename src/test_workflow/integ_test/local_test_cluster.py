# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from typing import List

from manifests.bundle_manifest import BundleManifest
from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.service import Service
from test_workflow.integ_test.service_opensearch import ServiceOpenSearch
from test_workflow.test_cluster import TestCluster
from test_workflow.test_recorder.test_recorder import TestRecorder


class LocalTestCluster(TestCluster):
    manifest: BundleManifest
    service_opensearch: ServiceOpenSearch
    dependency_installer: DependencyInstaller

    """
    Represents an on-box test cluster. This class downloads a bundle (from a BundleManifest) and runs it as a background process.
    """

    def __init__(
        self,
        dependency_installer: DependencyInstaller,
        work_dir: str,
        component_name: str,
        additional_cluster_config: dict,
        bundle_manifest: BundleManifest,
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

        self.manifest = bundle_manifest
        self.dependency_installer = dependency_installer

        self.service_opensearch = ServiceOpenSearch(
            self.manifest.build.version,
            self.manifest.build.distribution,
            self.additional_cluster_config,
            self.security_enabled,
            self.dependency_installer,
            self.work_dir
        )

    @property
    def service(self) -> Service:
        return self.service_opensearch

    @property
    def dependencies(self) -> List[Service]:
        return []

    @property
    def port(self) -> int:
        return 9200
