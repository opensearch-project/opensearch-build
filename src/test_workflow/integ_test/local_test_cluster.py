# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


from test_workflow.integ_test.service_opensearch import ServiceOpenSearch
from test_workflow.test_cluster import TestCluster
from test_workflow.test_recorder.test_recorder import TestRecorder


class LocalTestCluster(TestCluster):
    """
    Represents an on-box test cluster. This class downloads a bundle (from a BundleManifest) and runs it as a background process.
    """

    def __init__(
        self,
        dependency_installer,
        work_dir,
        component_name,
        additional_cluster_config,
        bundle_manifest,
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

        self.manifest = bundle_manifest
        self.dependency_installer = dependency_installer

        self.service_opensearch = ServiceOpenSearch(
            self.manifest.build.version,
            self.additional_cluster_config,
            self.security_enabled,
            self.dependency_installer,
            self.work_dir
        )

    @property
    def service(self):
        return self.service_opensearch

    @property
    def dependencies(self):
        return []

    def endpoint(self):
        return "localhost"

    def port(self):
        return 9200
