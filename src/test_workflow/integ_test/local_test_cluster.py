# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess
import time

import psutil  # type: ignore
import requests
import yaml

from paths.tree_walker import walk
from test_workflow.test_cluster import ClusterCreationException, TestCluster
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
        self.process = None
        self.save_logs = test_recorder.local_cluster_logs
        self.dependency_installer = dependency_installer

    def create_cluster(self):
        self.download()
        self.stdout = open("stdout.txt", "w")
        self.stderr = open("stderr.txt", "w")
        self.install_dir = f"opensearch-{self.manifest.build.version}"
        if not self.security_enabled:
            self.disable_security(self.install_dir)
        if self.additional_cluster_config is not None:
            self.__add_plugin_specific_config(
                self.additional_cluster_config,
                os.path.join(self.install_dir, "config", "opensearch.yml")
            )
        logging.info(f"Running {os.path.join(self.install_dir, 'opensearch-tar-install.sh')}")
        self.process = subprocess.Popen(
            "./opensearch-tar-install.sh",
            cwd=self.install_dir,
            shell=True,
            stdout=self.stdout,
            stderr=self.stderr
        )
        logging.info(f"Started OpenSearch with parent PID {self.process.pid}")
        self.wait_for_service()

    def endpoint(self):
        return "localhost"

    def port(self):
        return 9200

    def destroy(self):
        if self.process is None:
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
                if self.stdout:
                    logging.info("- stdout:")
                    with open(os.path.join(self.work_dir, self.stdout.name), "r") as stdout:
                        logging.info(stdout.read())
                if self.stderr:
                    logging.info("- stderr:")
                    with open(os.path.join(self.work_dir, self.stderr.name), "r") as stderr:
                        logging.info(stderr.read())

            time.sleep(10)
        raise ClusterCreationException("Cluster is not available after 10 attempts")

    def terminate_process(self):
        parent = psutil.Process(self.process.pid)
        logging.debug("Checking for child processes")
        child_processes = parent.children(recursive=True)
        for child in child_processes:
            logging.debug(f"Found child process with pid {child.pid}")
            if child.pid != self.process.pid:
                logging.debug(f"Sending SIGKILL to {child.pid} ")
                child.kill()
        logging.info(f"Sending SIGTERM to PID {self.process.pid}")
        self.process.terminate()
        try:
            logging.info("Waiting for process to terminate")
            self.process.wait(10)
        except subprocess.TimeoutExpired:
            logging.info("Process did not terminate after 10 seconds. Sending SIGKILL")
            self.process.kill()
            try:
                logging.info("Waiting for process to terminate")
                self.process.wait(10)
            except subprocess.TimeoutExpired:
                logging.info("Process failed to terminate even after SIGKILL")
                raise
        finally:
            logging.info(f"Process terminated with exit code {self.process.returncode}")
            if self.stdout:
                with open(os.path.join(self.work_dir, self.stdout.name), "r") as stdout:
                    self.local_cluster_stdout = stdout.read()
                    self.stdout.close()
                    self.stdout = None
            if self.stderr:
                with open(os.path.join(self.work_dir, self.stderr.name), "r") as stderr:
                    self.local_cluster_stderr = stderr.read()
                self.stderr.close()
                self.stderr = None
            self.return_code = self.process.returncode
            self.process = None
