# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from paths.tree_walker import walk
from test_workflow.integ_test.service_opensearch import ServiceOpenSearch
from test_workflow.integ_test.service_opensearch_dashboards import ServiceOpenSearchDashboards
from test_workflow.test_cluster import TestCluster
from test_workflow.test_recorder.test_recorder import TestRecorder
from test_workflow.test_recorder.test_result_data import TestResultData


class LocalTestClusterOpenSearchDashboards(TestCluster):
    """
    Represents an on-box test cluster. This class downloads a bundle (from a BundleManifest) and runs it as a background process.
    """

    def __init__(
        self,
        work_dir,
        component_name,
        additional_cluster_config,
        bundle_manifest,
        security_enabled,
        component_test_config,
        test_recorder: TestRecorder,
        s3_bucket_name=None,
    ):
        self.manifest = bundle_manifest
        self.work_dir = os.path.join(work_dir, "local-test-cluster")
        self.component_name = component_name
        self.security_enabled = security_enabled
        self.component_test_config = component_test_config
        self.bucket_name = s3_bucket_name
        self.additional_cluster_config = additional_cluster_config
        self.process = None
        self.save_logs = test_recorder.local_cluster_logs

        self.opensearch = ServiceOpenSearch(
            self.work_dir,
            self.component_name,
            self.additional_cluster_config,
            self.manifest,
            self.security_enabled,
            self.component_test_config,
            self.save_logs,
            self.bucket_name,
        )

        self.opensearch_dashboards = ServiceOpenSearchDashboards(
            self.work_dir,
            self.component_name,
            self.additional_cluster_config,
            self.manifest,
            self.security_enabled,
            self.component_test_config,
            self.save_logs,
            self.bucket_name,
        )

    def create_cluster(self):
        self.opensearch.start()
        self.opensearch_dashboards.start()

    def endpoint(self):
        return self.opensearch_dashboards.endpoint()

    def port(self):
        return self.opensearch_dashboards.port()

    def destroy(self):
        if self.process is None:
            logging.info("Local test cluster is not started")
            return
        self.opensearch.terminate_process()
        self.opensearch_dashboards.terminate_process()

        log_files = walk(os.path.join(self.work_dir, self.install_dir, "logs"))
        test_result_data = TestResultData(
            self.component_name,
            self.component_test_config,
            self.return_code,
            self.local_cluster_stdout,
            self.local_cluster_stderr,
            log_files,
        )
        self.save_logs.save_test_result_data(test_result_data)
