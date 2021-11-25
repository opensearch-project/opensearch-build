# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from test_workflow.integ_test.service_opensearch import ServiceOpenSearch
from test_workflow.test_cluster import ClusterServiceNotInitializedException, TestCluster
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_recorder.test_result_data import TestResultData


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
        self.manifest = bundle_manifest
        self.work_dir = os.path.join(work_dir, "local-test-cluster")
        os.makedirs(self.work_dir, exist_ok=True)
        self.component_name = component_name
        self.security_enabled = security_enabled
        self.component_test_config = component_test_config
        self.additional_cluster_config = additional_cluster_config
        self.save_logs = test_recorder.local_cluster_logs
        self.dependency_installer = dependency_installer
        self.service_opensearch = None

    def create_cluster(self):
        self.service_opensearch = ServiceOpenSearch(
            self.manifest.build.version,
            self.additional_cluster_config,
            self.security_enabled,
            self.dependency_installer,
            self.work_dir)

        self.service_opensearch.start()
        self.service_opensearch.wait_for_service()

    def endpoint(self):
        return "localhost"

    def port(self):
        return 9200

    def destroy(self):
        if not self.service_opensearch:
            raise ClusterServiceNotInitializedException()

        self.return_code, self.stdout_data, self.stderr_data, self.log_files = self.service_opensearch.terminate()

        self.__save_test_result_data()

    def __save_test_result_data(self):
        test_result_data = TestResultData(
            self.component_name, self.component_test_config, self.return_code, self.stdout_data, self.stderr_data, self.log_files
        )
        self.save_logs.save_test_result_data(test_result_data)
