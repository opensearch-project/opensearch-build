# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

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
        self.manifest = bundle_manifest
        self.work_dir = os.path.join(work_dir, "local-test-cluster")
        os.makedirs(self.work_dir, exist_ok=True)
        self.component_name = component_name
        self.security_enabled = security_enabled
        self.component_test_config = component_test_config
        self.additional_cluster_config = additional_cluster_config
        self.save_logs = test_recorder.local_cluster_logs
        self.dependency_installer = dependency_installer

    def create_cluster(self):
        self.service_opensearch = ServiceOpenSearch(
            self.manifest,
            self.component_name,
            self.component_test_config,
            self.additional_cluster_config,
            self.security_enabled,
            self.dependency_installer,
            self.save_logs,
            self.work_dir)

        self.service_opensearch.start()
        self.service_opensearch.wait_for_service()

    def endpoint(self):
        return "localhost"

    def port(self):
        return 9200

    def destroy(self):
<<<<<<< HEAD
        if not self.process_handler.started:
            logging.info("Local test cluster is not started")
            return
        self.terminate_process()
        log_files = walk(os.path.join(self.work_dir, self.install_dir, "logs"))
        test_result_data = TestResultData(
            self.component_name, self.component_test_config, self.return_code, self.local_cluster_stdout, self.local_cluster_stderr, log_files
        )
        self.save_logs.save_test_result_data(test_result_data)

    def url(self, path=""):
        return f'{"https" if self.security_enabled else "http"}://{self.endpoint()}:{self.port()}{path}'

    def download(self):
        logging.info(f"Creating local test cluster in {self.work_dir}")
        os.chdir(self.work_dir)
        logging.info("Downloading bundle")
        bundle_name = self.dependency_installer.download_dist(self.work_dir)
        logging.info(f"Downloaded bundle to {os.path.realpath(bundle_name)}")
        logging.info(f"Unpacking {bundle_name}")
        subprocess.check_call(f"tar -xzf {bundle_name}", shell=True)
        logging.info(f"Unpacked {bundle_name}")

    def disable_security(self, dir):
        subprocess.check_call(f'echo "plugins.security.disabled: true" >> {os.path.join(dir, "config", "opensearch.yml")}', shell=True)

    def __add_plugin_specific_config(self, additional_config: dict, file):
        with open(file, "a") as yamlfile:
            yamlfile.write(yaml.dump(additional_config))

    def wait_for_service(self):
        logging.info("Waiting for service to become available")
        url = self.url("/_cluster/health")

        for attempt in range(10):
            try:
                logging.info(f"Pinging {url} attempt {attempt}")
                response = requests.get(url, verify=False, auth=("admin", "admin"))
                logging.info(f"{response.status_code}: {response.text}")
                if response.status_code == 200 and ('"status":"green"' or '"status":"yellow"' in response.text):
                    logging.info("Service is available")
                    return
            except requests.exceptions.ConnectionError:
                logging.info("Service not available yet")
                logging.info("- stdout:")
                logging.info(self.process_handler.stdout_data)

                logging.info("- stderr:")
                logging.info(self.process_handler.stderr_data)

            time.sleep(10)
        raise ClusterCreationException("Cluster is not available after 10 attempts")

    def terminate_process(self):
        self.return_code = self.process_handler.terminate()
        self.local_cluster_stdout = self.process_handler.stdout_data
        self.local_cluster_stderr = self.process_handler.stderr_data
=======
        self.service_opensearch.terminate()
>>>>>>> Extract OpenSearch service related logic outside of LocalTestCluster
