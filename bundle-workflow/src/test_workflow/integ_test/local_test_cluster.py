# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess
import time
import urllib.request

import requests

from paths.tree_walker import walk
from test_workflow.test_cluster import ClusterCreationException, TestCluster


class LocalTestCluster(TestCluster):
    """
    Represents an on-box test cluster. This class downloads a bundle (from a BundleManifest) and runs it as a background process.
    """

    def __init__(self, work_dir, bundle_manifest, component_name, component_config, test_recorder):
        self.manifest = bundle_manifest
        self.work_dir = os.path.join(work_dir, "local-test-cluster")
        os.makedirs(self.work_dir, exist_ok=True)
        self.component_config = component_config
        self.component_name = component_name
        self.test_recorder = test_recorder
        self.security = None
        self.process = None

    def create_cluster(self):
        self.download()
        self.stdout = open("stdout.txt", "w")
        self.stderr = open("stderr.txt", "w")
        self.install_dir = f"opensearch-{self.manifest.build.version}"
        self.security = self._is_security_enabled(self.component_config)
        if not self.security:
            self.disable_security(self.install_dir)
        self.process = subprocess.Popen(
            "./opensearch-tar-install.sh",
            cwd=self.install_dir,
            shell=True,
            stdout=self.stdout,
            stderr=self.stderr,
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
        logs_files = walk(os.path.join(self.work_dir, self.install_dir, "logs"))
        self.test_recorder.record_local_cluster_logs(self.component_name,
                                                     self.component_config,
                                                     self.local_cluster_stdout,
                                                     self.local_cluster_stderr,
                                                     logs_files)

    def url(self, path=""):
        return f'{"https" if self.security else "http"}://{self.endpoint()}:{self.port()}{path}'

    def download(self):
        logging.info(f"Creating local test cluster in {self.work_dir}")
        os.chdir(self.work_dir)
        logging.info(f"Downloading bundle from {self.manifest.build.location}")
        urllib.request.urlretrieve(self.manifest.build.location, "bundle.tgz")
        logging.info(f'Downloaded bundle to {os.path.realpath("bundle.tgz")}')
        logging.info("Unpacking")
        subprocess.check_call("tar -xzf bundle.tgz", shell=True)
        logging.info("Unpacked")

    def _is_security_enabled(self, config):
        # TODO: Separate this logic in function once we have test-configs defined
        if config == "with-security":
            return True
        else:
            return False

    def disable_security(self, dir):
        subprocess.check_call(
            f'echo "plugins.security.disabled: true" >> {os.path.join(dir, "config", "opensearch.yml")}',
            shell=True,
        )

    def wait_for_service(self):
        logging.info("Waiting for service to become available")
        url = self.url("/_cluster/health")

        for attempt in range(10):
            try:
                logging.info(f"Pinging {url} attempt {attempt}")
                response = requests.get(url, verify=False, auth=("admin", "admin"))
                logging.info(f"{response.status_code}: {response.text}")
                if response.status_code == 200 and '"status":"green"' in response.text:
                    logging.info("Cluster is green")
                    return
            except requests.exceptions.ConnectionError:
                logging.info("Service not available yet")
            time.sleep(10)
        raise ClusterCreationException("Cluster is not green after 10 attempts")

    def terminate_process(self):
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
            stdout = open(os.path.join(os.path.realpath(self.work_dir), self.stdout.name), "r")
            stderr = open(os.path.join(os.path.realpath(self.work_dir), self.stderr.name), "r")
            self.local_cluster_stdout = stdout.read()
            self.local_cluster_stderr = stderr.read()
            self.stdout.close()
            self.stderr.close()
            self.process = None
